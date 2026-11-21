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

    def test_rejects_hyphenated_qualifier_digits(self):
        # maven-compiler-plugin publishes prereleases as "4.0.0-beta-4",
        # not "4.0.0-beta4" - the qualifier and its digits are separated
        # by their own hyphen.
        self.assertFalse(uv._is_release_version("4.0.0-beta-4"))
        self.assertFalse(uv._is_release_version("2.0.0-alpha-1"))

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


CONTAINER_VERSIONS = {"tomcat": "11.0.29", "wildfly": "41.0.1.Final", "spring-boot": "4.1.3", "quarkus": "3.40.1.2"}


class TestContainerDocLinks(unittest.TestCase):
    def test_parse_pom_properties(self):
        pom = "<properties>\n<version.tomcat>11.0.29</version.tomcat>\n<version.wildfly> 41.0.1.Final </version.wildfly>\n</properties>"
        self.assertEqual(uv.parse_pom_properties(pom), {"version.tomcat": "11.0.29", "version.wildfly": "41.0.1.Final"})

    @patch("update_versions._github_get")
    def test_get_container_versions_merges_root_and_parent_pom(self, mock_get):
        import base64
        poms = {
            "pom.xml": "<version.quarkus>3.40.1.2</version.quarkus><version.spring-boot>4.1.3</version.spring-boot>",
            "parent/pom.xml": "<version.wildfly>41.0.1.Final</version.wildfly><version.tomcat>11.0.29</version.tomcat>",
        }
        mock_get.side_effect = lambda path: {"content": base64.b64encode(
            poms[path.split("/contents/")[1].split("?")[0]].encode()).decode()}
        self.assertEqual(uv.get_container_versions("v2.2.2"), CONTAINER_VERSIONS)

    @patch("update_versions._github_get")
    def test_get_container_versions_fails_on_missing_property(self, mock_get):
        mock_get.return_value = {"content": ""}
        with self.assertRaises(RuntimeError):
            uv.get_container_versions("v2.2.2")

    def test_replaces_version_segments(self):
        text = (
            "https://tomcat.apache.org/tomcat-9.0-doc/config/valve.html\n"
            "https://docs.wildfly.org/23/Admin_Guide.html\n"
            "https://docs.spring.io/spring-boot/3.5/reference/web/servlet.html\n"
            "https://docs.spring.io/spring-boot/3.5.0/api/java/x.html\n"
            "https://quarkus.io/version/3.27/guides/rest\n"
            "https://docs.spring.io/spring-boot/appendix/application-properties/index.html\n"
        )
        updated, changes = uv._apply_replacements_to_text(
            text, uv._build_container_doc_replacements(CONTAINER_VERSIONS))
        self.assertEqual(updated, (
            "https://tomcat.apache.org/tomcat-11.0-doc/config/valve.html\n"
            "https://docs.wildfly.org/41/Admin_Guide.html\n"
            "https://docs.spring.io/spring-boot/4.1/reference/web/servlet.html\n"
            "https://docs.spring.io/spring-boot/4.1/api/java/x.html\n"
            "https://quarkus.io/version/3.40/guides/rest\n"
            "https://docs.spring.io/spring-boot/appendix/application-properties/index.html\n"
        ))
        self.assertEqual(len(changes), 4)

    def test_replaces_supported_container_list_items(self):
        text = "* Apache Tomcat 10.1\n* WildFly Application Server 33\n* Apache Tomcat\nApache Tomcat 9.0 is old.\n"
        updated, _ = uv._apply_replacements_to_text(
            text, uv._build_container_doc_replacements(CONTAINER_VERSIONS))
        self.assertEqual(updated,
                         "* Apache Tomcat 11.0\n* WildFly Application Server 41\n* Apache Tomcat\nApache Tomcat 9.0 is old.\n")

    def test_container_doc_files_exist(self):
        self.assertTrue(all(f.exists() for f in uv.CONTAINER_DOC_FILES))


DATABASE_POM = """
<properties><version.h2>2.5.252</version.h2></properties>
<profiles>
  <profile><id>db2</id><properties><database.tc.url>operatondb2:12.1.2.0</database.tc.url></properties></profile>
  <profile><id>db2-115</id><properties><version.db2>11.5</version.db2></properties></profile>
  <profile><id>mariadb</id><properties><database.tc.url>operatonmariadb:10.11</database.tc.url></properties></profile>
  <profile><id>mysql</id><properties><database.tc.url>operatonmysql:8.4</database.tc.url></properties></profile>
  <profile><id>oracle</id><properties><database.tc.url>operatonoracle:21-faststart</database.tc.url></properties></profile>
  <profile><id>postgresql</id><properties><database.tc.url>operatonpostgresql:14</database.tc.url></properties></profile>
  <profile><id>sqlserver</id><properties><database.tc.url>operatonsqlserver:2022-latest</database.tc.url></properties></profile>
  <profile><id>sqlserver-2017</id><properties><database.tc.url>operatonsqlserver:2017</database.tc.url></properties></profile>
</profiles>
"""
DATABASE_VERSIONS = {"mysql": "8.4", "mariadb": "10.11", "oracle": "21c", "db2": "12.1",
                     "postgresql": "14", "sqlserver": "2022", "h2": "2.5"}


class TestSupportedDatabases(unittest.TestCase):
    def test_parse_database_versions(self):
        self.assertEqual(uv.parse_database_versions(DATABASE_POM), DATABASE_VERSIONS)

    def test_oracle_23_is_26ai(self):
        pom = DATABASE_POM.replace("operatonoracle:21-faststart", "operatonoracle:23-faststart")
        self.assertEqual(uv.parse_database_versions(pom)["oracle"], "26ai")

    def test_parse_fails_on_missing_profile(self):
        with self.assertRaises(RuntimeError):
            uv.parse_database_versions(DATABASE_POM.replace("<id>mariadb</id>", "<id>maria</id>"))

    def test_adds_missing_versions_and_keeps_others(self):
        text = ("* MySQL 8.0\n* MariaDB 10.11\n* Oracle 19c / 26ai\n"
                "* IBM DB2 11.5 (excluding IBM z/OS)\n* PostgreSQL 14 / 15 / 16\n"
                "* Amazon Aurora PostgreSQL compatible with PostgreSQL 14 / 15\n"
                "* Microsoft SQL Server 2017 / 2019 / 2022 (see note)\n* H2 2.3 (not recommended)\n")
        updated, changes = uv.update_database_versions_text(text, DATABASE_VERSIONS)
        self.assertEqual(updated, (
            "* MySQL 8.0 / 8.4\n* MariaDB 10.11\n* Oracle 19c / 21c / 26ai\n"
            "* IBM DB2 11.5 / 12.1 (excluding IBM z/OS)\n* PostgreSQL 14 / 15 / 16\n"
            "* Amazon Aurora PostgreSQL compatible with PostgreSQL 14 / 15\n"
            "* Microsoft SQL Server 2017 / 2019 / 2022 (see note)\n* H2 2.5 (not recommended)\n"))
        self.assertEqual(changes, ["mysql 8.4", "oracle 21c", "db2 12.1", "h2 2.5"])

    def test_ignores_end_of_support_notes(self):
        text = "* IBM DB2 11.5: 30 April 2027\n* Microsoft SQL Server 2017: 12 October 2027\n* Oracle 19c: 31 December 2029\n"
        self.assertEqual(uv.update_database_versions_text(text, DATABASE_VERSIONS), (text, []))
