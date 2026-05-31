import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))
import update_versions as uv


FAKE_SBOM = {"components": [
    {"purl": "pkg:maven/org.slf4j/slf4j-simple@2.0.9?type=jar", "version": "2.0.9"},
    {"purl": "pkg:maven/jakarta.xml.bind/jakarta.xml.bind-api@4.0.2?type=jar", "version": "4.0.2"},
]}


class TestGetLatestRelease(unittest.TestCase):
    @patch("update_versions._github_get")
    def test_strips_v_prefix(self, mock_get):
        mock_get.return_value = {"tag_name": "v2.2.0", "assets": []}
        version, _ = uv.get_latest_operaton_release()
        self.assertEqual(version, "2.2.0")

    @patch("update_versions._github_get")
    def test_strips_v_prefix_single_digit(self, mock_get):
        mock_get.return_value = {"tag_name": "v1.5.3", "assets": []}
        version, _ = uv.get_latest_operaton_release()
        self.assertEqual(version, "1.5.3")

    @patch("update_versions._github_get")
    def test_returns_release_data(self, mock_get):
        fake_data = {"tag_name": "v2.2.0", "assets": [{"name": "test.zip"}]}
        mock_get.return_value = fake_data
        _, release_data = uv.get_latest_operaton_release()
        self.assertEqual(release_data["assets"][0]["name"], "test.zip")


class TestGetVersionFromSbom(unittest.TestCase):
    def test_finds_existing_component(self):
        self.assertEqual(uv.get_version_from_sbom(FAKE_SBOM, "org.slf4j", "slf4j-simple"), "2.0.9")

    def test_returns_none_for_missing(self):
        self.assertIsNone(uv.get_version_from_sbom(FAKE_SBOM, "com.example", "missing"))

    def test_returns_none_for_none_sbom(self):
        self.assertIsNone(uv.get_version_from_sbom(None, "org.slf4j", "slf4j-simple"))


class TestIsReleaseVersion(unittest.TestCase):
    def test_accepts_stable(self):
        for v in ("2.0.9", "1.0.0", "3.5.0", "10.2.1"):
            self.assertTrue(uv._is_release_version(v), v)

    def test_rejects_alpha(self):
        self.assertFalse(uv._is_release_version("2.0.0-alpha"))
        self.assertFalse(uv._is_release_version("2.0.0.alpha1"))

    def test_rejects_beta(self):
        self.assertFalse(uv._is_release_version("2.0.0-beta"))
        self.assertFalse(uv._is_release_version("2.0.0-beta2"))

    def test_rejects_rc(self):
        self.assertFalse(uv._is_release_version("2.0.0-RC1"))
        self.assertFalse(uv._is_release_version("2.0.0-rc2"))

    def test_rejects_milestone(self):
        self.assertFalse(uv._is_release_version("6.0.0-M1"))
        self.assertFalse(uv._is_release_version("6.0.0-M12"))


class TestGetVersionFromMavenCentral(unittest.TestCase):
    @patch("update_versions.urllib.request.urlopen")
    def test_skips_prerelease_versions(self, mock_urlopen):
        docs = [
            {"v": "6.0.0-M1"},
            {"v": "5.3.39"},
            {"v": "5.3.38"},
        ]
        payload = json.dumps({"response": {"docs": docs}}).encode()
        mock_urlopen.return_value.__enter__ = lambda s: s
        mock_urlopen.return_value.__exit__ = unittest.mock.MagicMock(return_value=False)
        mock_urlopen.return_value.read = lambda: payload
        result = uv.get_version_from_maven_central("org.springframework", "spring-core")
        self.assertEqual(result, "5.3.39")

    @patch("update_versions.urllib.request.urlopen")
    def test_raises_when_only_prereleases(self, mock_urlopen):
        docs = [{"v": "6.0.0-M1"}, {"v": "5.0.0-RC1"}]
        payload = json.dumps({"response": {"docs": docs}}).encode()
        mock_urlopen.return_value.__enter__ = lambda s: s
        mock_urlopen.return_value.__exit__ = unittest.mock.MagicMock(return_value=False)
        mock_urlopen.return_value.read = lambda: payload
        with self.assertRaises(RuntimeError):
            uv.get_version_from_maven_central("org.springframework", "spring-core")


class TestResolveVersion(unittest.TestCase):
    @patch("update_versions.get_version_from_maven_central")
    def test_prefers_sbom(self, mock_mc):
        self.assertEqual(uv.resolve_version(FAKE_SBOM, "org.slf4j", "slf4j-simple"), "2.0.9")
        mock_mc.assert_not_called()

    @patch("update_versions.get_version_from_maven_central")
    def test_falls_back_to_maven_central(self, mock_mc):
        mock_mc.return_value = "3.5.0"
        self.assertEqual(uv.resolve_version(FAKE_SBOM, "com.example", "missing"), "3.5.0")
        mock_mc.assert_called_once_with("com.example", "missing")


class TestApplyReplacements(unittest.TestCase):
    def _make_rep(self, desc, pattern_str, version):
        import re
        return uv.Replacement(desc, re.compile(pattern_str), version)

    def test_replaces_operaton_version(self):
        text = "<operaton.version>1.0.0</operaton.version>"
        rep = self._make_rep(
            "test",
            r"(<operaton\.version>)\d+\.\d+\.\d+(</operaton\.version>)",
            "2.2.0",
        )
        result, changes = uv._apply_replacements_to_text(text, [rep])
        self.assertEqual(result, "<operaton.version>2.2.0</operaton.version>")
        self.assertEqual(changes, ["test"])

    def test_no_change_when_already_current(self):
        text = "<operaton.version>2.2.0</operaton.version>"
        rep = self._make_rep(
            "test",
            r"(<operaton\.version>)\d+\.\d+\.\d+(</operaton\.version>)",
            "2.2.0",
        )
        result, changes = uv._apply_replacements_to_text(text, [rep])
        self.assertEqual(result, text)
        self.assertEqual(changes, [])

    def test_skips_archive_directory(self):
        """update_docs must not touch files under docs/get-started/archive/."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            archive = tmp_path / "docs" / "get-started" / "archive"
            archive.mkdir(parents=True)
            active = tmp_path / "docs" / "get-started"
            active.mkdir(parents=True, exist_ok=True)

            archive_file = archive / "old.md"
            archive_file.write_text("<operaton.version>1.0.0</operaton.version>")
            active_file = active / "index.md"
            active_file.write_text("<operaton.version>1.0.0</operaton.version>")

            import re
            reps = [uv.Replacement(
                "test",
                re.compile(r"(<operaton\.version>)\d+\.\d+\.\d+(</operaton\.version>)"),
                "2.2.0",
            )]

            orig_docs = uv.DOCS_DIR
            orig_archive = uv.ARCHIVE_DIR
            uv.DOCS_DIR = tmp_path / "docs"
            uv.ARCHIVE_DIR = tmp_path / "docs" / "get-started" / "archive"
            try:
                uv.update_docs(reps, dry_run=False)
            finally:
                uv.DOCS_DIR = orig_docs
                uv.ARCHIVE_DIR = orig_archive

            self.assertEqual(archive_file.read_text(), "<operaton.version>1.0.0</operaton.version>")
            self.assertEqual(active_file.read_text(), "<operaton.version>2.2.0</operaton.version>")
