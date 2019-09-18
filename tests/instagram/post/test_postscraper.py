import json
import os.path
import unittest
from unittest.mock import patch

from instasave.instagram.post import PostScraper
from instasave.utils import hook
from instasave.web.client import HTTPHeaders

HTML = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "test_data",
    "html",
)

JSON = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "test_data",
    "json",
)


class TestPostScraper(unittest.TestCase):
    def setUp(self):
        headers = HTTPHeaders().headers
        self.scraper = PostScraper(headers)

    @patch("requests.get")
    def test_property_graphimage(self, mock_requests):
        with open(os.path.join(HTML, "graphimage_html.txt")) as f:
            mock_requests.return_value.text = f.read()
        self.scraper.post_data("posturltographimage")
        self.assertEqual(self.scraper.username, "instagram")
        self.assertEqual(self.scraper.shortcode, "B2UUzbyAMrD")
        self.assertEqual(self.scraper.created_at, "20190912161807")
        mock_requests.assert_called_once()

    @patch("requests.get")
    def test_property_graphvideo(self, mock_requests):
        with open(os.path.join(HTML, "graphvideo_html.txt")) as f:
            mock_requests.return_value.text = f.read()
        self.scraper.post_data("posturltographvideo")
        self.assertEqual(self.scraper.username, "instagram")
        self.assertEqual(self.scraper.shortcode, "B2MmijPgt_B")
        self.assertEqual(self.scraper.created_at, "20190909162043")
        mock_requests.assert_called_once()

    @patch("requests.get")
    def test_property_graphsidecar(self, mock_requests):
        with open(os.path.join(HTML, "graphsidecar_html.txt")) as f:
            mock_requests.return_value.text = f.read()
        self.scraper.post_data("posturltographsidecar")
        self.assertEqual(self.scraper.username, "instagram")
        self.assertEqual(self.scraper.shortcode, "B0ObD8SA0Sq")
        self.assertEqual(self.scraper.created_at, "20190722161435")
        mock_requests.assert_called_once()

    @patch("requests.get")
    def test_post_data_return_graphimage(self, mock_requests):
        with open(os.path.join(HTML, "graphimage_html.txt")) as f:
            mock_requests.return_value.text = f.read()

        url, type = self.scraper.post_data("posturltographimage")
        self.assertRegex(url, r"^http[s]?://[a-zA-Z0-9_\-\./?=&]+$")
        self.assertEqual(type, "GraphImage")
        mock_requests.assert_called_once()

    @patch("requests.get")
    def test_post_data_return_graphvideo(self, mock_requests):
        with open(os.path.join(HTML, "graphvideo_html.txt")) as f:
            mock_requests.return_value.text = f.read()

        url, type = self.scraper.post_data("posturltographvideo")
        self.assertRegex(url, r"^http[s]?://[a-zA-Z0-9_\-\./?=&]+$")
        self.assertEqual(type, "GraphVideo")
        mock_requests.assert_called_once()

    @patch("requests.get")
    def test_post_data_return_graphsidecar(self, mock_requests):
        with open(os.path.join(HTML, "graphsidecar_html.txt")) as f:
            mock_requests.return_value.text = f.read()

        urls, type = self.scraper.post_data("posturltographsidecar")
        for url in urls:
            self.assertRegex(url, r"^http[s]?://[a-zA-Z0-9_\-\./?=&]+$")
        self.assertEqual(type, "GraphSidecar")
        mock_requests.assert_called_once()

    def test_get_type_returns_graphimage(self):
        with open(os.path.join(JSON, "graphimage_json.txt")) as f:
            json_data = json.loads(f.read(), object_hook=hook.shortcode_media)
        self.assertEqual(self.scraper._get_type(json_data), "GraphImage")

    def test_get_type_returns_graphvideo(self):
        with open(os.path.join(JSON, "graphvideo_json.txt")) as f:
            json_data = json.loads(f.read(), object_hook=hook.shortcode_media)
        self.assertEqual(self.scraper._get_type(json_data), "GraphVideo")

    def test_get_type_returns_graphsidecar(self):
        with open(os.path.join(JSON, "graphsidecar_json.txt")) as f:
            json_data = json.loads(f.read(), object_hook=hook.shortcode_media)
        self.assertEqual(self.scraper._get_type(json_data), "GraphSidecar")

    def test_get_url_returns_graphimage_display_url(self):
        with open(os.path.join(JSON, "graphimage_json.txt")) as f:
            json_data = json.loads(f.read(), object_hook=hook.shortcode_media)
        self.assertRegex(
            self.scraper._get_url(json_data, "GraphImage"),
            r"^http[s]?://[a-zA-Z0-9_\-\./?=&]+$",
        )

    def test_get_url_returns_graphvideo_video_url(self):
        with open(os.path.join(JSON, "graphvideo_json.txt")) as f:
            json_data = json.loads(f.read(), object_hook=hook.shortcode_media)
        self.assertRegex(
            self.scraper._get_url(json_data, "GraphVideo"),
            r"^http[s]?://[a-zA-Z0-9_\-\./?=&]+$",
        )

    def test_get_url_returns_graphsidecar_urls(self):
        with open(os.path.join(JSON, "graphsidecar_json.txt")) as f:
            json_data = json.loads(f.read(), object_hook=hook.shortcode_media)
        urls = self.scraper._get_url(json_data, "GraphSidecar")
        for url in urls:
            self.assertRegex(url, r"^http[s]?://[a-zA-Z0-9_\-\./?=&]+$")
