import json
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, __import__("os").path.join(__import__("os").path.dirname(__file__), ".."))
import update_versions as uv


FAKE_RELEASE = {"tag_name": "v2.2.0", "assets": [
    {"name": "operaton-bpm-2.2.0.zip",
     "content_type": "application/zip",
     "browser_download_url": "https://example.com/operaton-bpm-2.2.0.zip"},
]}

FAKE_SBOM = {"components": [
    {"purl": "pkg:maven/org.slf4j/slf4j-simple@2.0.9?type=jar", "name": "slf4j-simple", "version": "2.0.9"},
    {"purl": "pkg:maven/jakarta.xml.bind/jakarta.xml.bind-api@4.0.2?type=jar", "name": "jakarta.xml.bind-api", "version": "4.0.2"},
]}


class TestGetLatestRelease(unittest.TestCase):
    @patch("update_versions._github_get")
    def test_strips_v_prefix(self, mock_get):
        mock_get.return_value = FAKE_RELEASE
        self.assertEqual(uv.get_latest_operaton_release(), "2.2.0")

    @patch("update_versions._github_get")
    def test_returns_tag_version(self, mock_get):
        mock_get.return_value = {"tag_name": "v1.5.3", "assets": []}
        self.assertEqual(uv.get_latest_operaton_release(), "1.5.3")


class TestGetVersionFromSbom(unittest.TestCase):
    def test_finds_existing_component(self):
        # purl has ?type=jar suffix — prefix matching must handle this
        version = uv.get_version_from_sbom(FAKE_SBOM, "org.slf4j", "slf4j-simple")
        self.assertEqual(version, "2.0.9")

    def test_returns_none_for_missing_component(self):
        version = uv.get_version_from_sbom(FAKE_SBOM, "com.example", "missing")
        self.assertIsNone(version)

    def test_returns_none_for_none_sbom(self):
        version = uv.get_version_from_sbom(None, "org.slf4j", "slf4j-simple")
        self.assertIsNone(version)


class TestResolveVersion(unittest.TestCase):
    def test_prefers_sbom_over_maven_central(self):
        version = uv.resolve_version(FAKE_SBOM, "org.slf4j", "slf4j-simple")
        self.assertEqual(version, "2.0.9")

    @patch("update_versions.get_version_from_maven_central")
    def test_falls_back_to_maven_central_when_not_in_sbom(self, mock_mc):
        mock_mc.return_value = "3.5.0"
        version = uv.resolve_version(FAKE_SBOM, "com.example", "missing")
        self.assertEqual(version, "3.5.0")
        mock_mc.assert_called_once_with("com.example", "missing")
