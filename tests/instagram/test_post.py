import unittest
from unittest.mock import patch
from instagram.post import PostScraper
from utils.settings import USER_AGENT_FILE
from utils.helpers import HTTPHeaders

class TestPostScraper(unittest.TestCase):

    def setUp(self):
        self.scraper = PostScraper(HTTPHeaders(USER_AGENT_FILE).headers)
        self.graphvideo = {
            "entry_data": {
                "PostPage": [{
                    "graphql": {
                        "shortcode_media": {
                            "__typename": "GraphVideo",
                            "video_url": "GRAPH VIDEO URL",
                            }
                        }
                    }]
                }
            }
        self.graphimage = {
            "entry_data": {
                "PostPage": [{
                    "graphql": {
                        "shortcode_media": {
                            "__typename": "GraphImage",
                            "display_url": "GRAPH IMAGE URL",
                            }
                        }
                    }]
                }
            }
        self.graphsidecar = {
            "entry_data": {
                "PostPage": [{
                    "graphql": {
                        "shortcode_media": {
                            "__typename": "GraphSidecar",
                            "edge_sidecar_to_children": {
                                "edges": [{
                                    "node": {
                                        "__typename": "GraphVideo",
                                        "video_url": "GRAPH SIDECAR URL 1",
                                    }
                                }, {
                                    "node": {
                                        "__typename": "GraphVideo",
                                        "video_url": "GRAPH SIDECAR URL 2",
                                    }
                                }]
                            }
                        }
                    }
                }]
            }
        }

    @patch("instagram.post.PostScraper._json_data")
    def test_post_data_graphimage(self, mock_json_data):
        mock_json_data.return_value = self.graphimage["entry_data"] \
            ["PostPage"][0]["graphql"]["shortcode_media"]
        got = self.scraper.post_data("someurl")
        want = ("GRAPH IMAGE URL", "GraphImage")
        self.assertEqual(got, want)
        mock_json_data.assert_called_once()

    @patch("instagram.post.PostScraper._json_data")
    def test_post_data_graphvideo(self, mock_json_data):
        mock_json_data.return_value = self.graphvideo["entry_data"] \
            ["PostPage"][0]["graphql"]["shortcode_media"]
        got = self.scraper.post_data("someurl")
        want = ("GRAPH VIDEO URL", "GraphVideo")
        self.assertEqual(got, want)
        mock_json_data.assert_called_once()

    @patch("instagram.post.PostScraper._json_data")
    def test_post_data_graphsidecar(self, mock_json_data):
        mock_json_data.return_value = self.graphsidecar["entry_data"] \
            ["PostPage"][0]["graphql"]["shortcode_media"]
        got = self.scraper.post_data("someurl")
        want = (["GRAPH SIDECAR URL 1", "GRAPH SIDECAR URL 2"], "GraphSidecar")
        self.assertEqual(got, want)
        mock_json_data.assert_called_once()

    # TODO: write test for this method later.
    # def test_json_data(self):
    #     pass

    def test_get_type_graphimage(self):
        data = self.graphimage["entry_data"] \
            ["PostPage"][0]["graphql"]["shortcode_media"]
        got = self.scraper._get_type(data)
        want = "GraphImage"
        self.assertEqual(got, want)

    def test_get_type_graphvideo(self):
        data = self.graphvideo["entry_data"] \
            ["PostPage"][0]["graphql"]["shortcode_media"]
        got = self.scraper._get_type(data)
        want = "GraphVideo"
        self.assertEqual(got, want)

    def test_get_type_graphsidecar(self):
        data = self.graphsidecar["entry_data"] \
            ["PostPage"][0]["graphql"]["shortcode_media"]
        got = self.scraper._get_type(data)
        want = "GraphSidecar"
        self.assertEqual(got, want)

    def test_get_type_raises_error(self):
        with self.assertRaises(KeyError):
            self.scraper._get_type(self.graphimage)

    def test_get_url_graphvideo(self):
        data = self.graphvideo["entry_data"] \
            ["PostPage"][0]["graphql"]["shortcode_media"]
        got = self.scraper._get_url(data, "GraphVideo")
        want = "GRAPH VIDEO URL"
        self.assertEqual(got, want)

    def test_get_url_graphimage(self):
        data = self.graphimage["entry_data"] \
            ["PostPage"][0]["graphql"]["shortcode_media"]
        got = self.scraper._get_url(data, "GraphImage")
        want = "GRAPH IMAGE URL"
        self.assertEqual(got, want)

    def test_get_url_graphsidecar(self):
        data = self.graphsidecar["entry_data"] \
            ["PostPage"][0]["graphql"]["shortcode_media"]
        got = self.scraper._get_url(data, "GraphSidecar")
        want = ["GRAPH SIDECAR URL 1", "GRAPH SIDECAR URL 2"]
        self.assertEqual(got, want)

class TestDownloader(unittest.TestCase):
    pass
