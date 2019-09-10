import io
import sys
import unittest
from unittest.mock import patch

from instagram.post import PostScraper
from utils.helpers import HTTPHeaders
from utils.settings import USER_AGENT_FILE


class TestPostScraper(unittest.TestCase):
    def setUp(self):
        self.headers = HTTPHeaders(USER_AGENT_FILE).headers
        self.scraper = PostScraper(self.headers)
        self.verbose_scraper = PostScraper(self.headers, verbose=True)

        self.graphvideo = {
            "entry_data": {
                "PostPage": [
                    {
                        "graphql": {
                            "shortcode_media": {
                                "__typename": "GraphVideo",
                                "video_url": "GRAPH VIDEO URL",
                                "taken_at_timestamp": 1567007901,
                                "owner": {"username": "VIDEO USERNAME"},
                            }
                        }
                    }
                ]
            }
        }

        self.graphimage = {
            "entry_data": {
                "PostPage": [
                    {
                        "graphql": {
                            "shortcode_media": {
                                "__typename": "GraphImage",
                                "display_url": "GRAPH IMAGE URL",
                                "taken_at_timestamp": 1567007901,
                                "owner": {"username": "IMAGE USERNAME"},
                            }
                        }
                    }
                ]
            }
        }

        self.graphsidecar = {
            "entry_data": {
                "PostPage": [
                    {
                        "graphql": {
                            "shortcode_media": {
                                "__typename": "GraphSidecar",
                                "taken_at_timestamp": 1567007901,
                                "owner": {"username": "SIDECAR USERNAME"},
                                "edge_sidecar_to_children": {
                                    "edges": [
                                        {
                                            "node": {
                                                "__typename": "GraphVideo",
                                                "video_url": "GRAPH SIDECAR URL 1",
                                            }
                                        },
                                        {
                                            "node": {
                                                "__typename": "GraphVideo",
                                                "video_url": "GRAPH SIDECAR URL 2",
                                            }
                                        },
                                    ]
                                },
                            }
                        }
                    }
                ]
            }
        }

        self.html_code = (
            '<html><head> \
            <script type="text/javascript"></script>\
            <script type="text/javascript"></script> \
            <script type="text/javascript"></script> </head><body> \
            <script type="text/javascript">window._sharedData = '
            + str(self.graphimage).replace("'", '"')
            + ";</script> \
            </body></html>"
        )

    @patch("requests.get")
    def test_json_data(self, mock_requests):
        mock_requests.return_value = mock_requests.models.Response
        mock_requests.return_value.text = self.html_code
        got = self.scraper._json_data("someurl")
        self.assertEqual(got["owner"]["username"], "IMAGE USERNAME")

    @patch("instagram.post.PostScraper._json_data")
    def test_post_data_verbose_message(self, mock_json_data):
        mock_json_data.return_value = self.graphimage["entry_data"]["PostPage"][
            0
        ]["graphql"]["shortcode_media"]
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.verbose_scraper.post_data("someurl")
        sys.stdout = sys.__stdout__
        got = captured_output.getvalue()
        want = "Scrape data from one of IMAGE USERNAME's posts...\n"
        self.assertEqual(got, want)

    @patch("instagram.post.PostScraper._json_data")
    def test_post_data_graphimage(self, mock_json_data):
        mock_json_data.return_value = self.graphimage["entry_data"]["PostPage"][
            0
        ]["graphql"]["shortcode_media"]
        got = self.scraper.post_data("someurl")
        want = ("GRAPH IMAGE URL", "GraphImage")
        self.assertEqual(got, want)
        mock_json_data.assert_called_once()

    @patch("instagram.post.PostScraper._json_data")
    def test_post_data_graphvideo(self, mock_json_data):
        mock_json_data.return_value = self.graphvideo["entry_data"]["PostPage"][
            0
        ]["graphql"]["shortcode_media"]
        got = self.scraper.post_data("someurl")
        want = ("GRAPH VIDEO URL", "GraphVideo")
        self.assertEqual(got, want)
        mock_json_data.assert_called_once()

    @patch("instagram.post.PostScraper._json_data")
    def test_post_data_graphsidecar(self, mock_json_data):
        mock_json_data.return_value = self.graphsidecar["entry_data"][
            "PostPage"
        ][0]["graphql"]["shortcode_media"]
        got = self.scraper.post_data("someurl")
        want = (["GRAPH SIDECAR URL 1", "GRAPH SIDECAR URL 2"], "GraphSidecar")
        self.assertEqual(got, want)
        mock_json_data.assert_called_once()

    def test_get_username_graphvideo(self):
        self.scraper.data = self.graphvideo["entry_data"]["PostPage"][0][
            "graphql"
        ]["shortcode_media"]
        got = self.scraper.get_username()
        self.assertEqual(got, "VIDEO USERNAME")

    def test_get_username_graphimage(self):
        self.scraper.data = self.graphimage["entry_data"]["PostPage"][0][
            "graphql"
        ]["shortcode_media"]
        got = self.scraper.get_username()
        self.assertEqual(got, "IMAGE USERNAME")

    def test_get_username_graphsidecar(self):
        self.scraper.data = self.graphsidecar["entry_data"]["PostPage"][0][
            "graphql"
        ]["shortcode_media"]
        got = self.scraper.get_username()
        self.assertEqual(got, "SIDECAR USERNAME")

    def test_get_created_at_graphvide(self):
        self.scraper.data = self.graphvideo["entry_data"]["PostPage"][0][
            "graphql"
        ]["shortcode_media"]
        got = self.scraper.get_created_at()
        self.assertEqual(got, "_20190828155821")

    def test_get_created_at_graphimage(self):
        self.scraper.data = self.graphimage["entry_data"]["PostPage"][0][
            "graphql"
        ]["shortcode_media"]
        got = self.scraper.get_created_at()
        self.assertEqual(got, "_20190828155821")

    def test_get_created_at_graphsidecar(self):
        self.scraper.data = self.graphsidecar["entry_data"]["PostPage"][0][
            "graphql"
        ]["shortcode_media"]
        got = self.scraper.get_created_at()
        self.assertEqual(got, "_20190828155821")

    def test_get_type_graphimage(self):
        data = self.graphimage["entry_data"]["PostPage"][0]["graphql"][
            "shortcode_media"
        ]
        got = self.scraper._get_type(data)
        want = "GraphImage"
        self.assertEqual(got, want)

    def test_get_type_graphvideo(self):
        data = self.graphvideo["entry_data"]["PostPage"][0]["graphql"][
            "shortcode_media"
        ]
        got = self.scraper._get_type(data)
        want = "GraphVideo"
        self.assertEqual(got, want)

    def test_get_type_graphsidecar(self):
        data = self.graphsidecar["entry_data"]["PostPage"][0]["graphql"][
            "shortcode_media"
        ]
        got = self.scraper._get_type(data)
        want = "GraphSidecar"
        self.assertEqual(got, want)

    def test_get_type_raises_error(self):
        with self.assertRaises(KeyError):
            self.scraper._get_type(self.graphimage)

    def test_get_url_graphvideo(self):
        data = self.graphvideo["entry_data"]["PostPage"][0]["graphql"][
            "shortcode_media"
        ]
        got = self.scraper._get_url(data, "GraphVideo")
        want = "GRAPH VIDEO URL"
        self.assertEqual(got, want)

    def test_get_url_graphimage(self):
        data = self.graphimage["entry_data"]["PostPage"][0]["graphql"][
            "shortcode_media"
        ]
        got = self.scraper._get_url(data, "GraphImage")
        want = "GRAPH IMAGE URL"
        self.assertEqual(got, want)

    def test_get_url_graphsidecar(self):
        data = self.graphsidecar["entry_data"]["PostPage"][0]["graphql"][
            "shortcode_media"
        ]
        got = self.scraper._get_url(data, "GraphSidecar")
        want = ["GRAPH SIDECAR URL 1", "GRAPH SIDECAR URL 2"]
        self.assertEqual(got, want)


class TestDownloader(unittest.TestCase):
    pass
