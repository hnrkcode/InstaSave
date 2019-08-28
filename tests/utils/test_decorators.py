import unittest
from unittest.mock import patch
from utils.decorators import start_at_shortcode_media

class TestDecorators(unittest.TestCase):

    def setUp(self):
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

    def test_start_at_shortcode_media_graphimage(self):
        def data_func():
            return self.graphimage
        data = start_at_shortcode_media(data_func)
        got = data()
        self.assertEqual(got["__typename"], "GraphImage")
        self.assertEqual(got["display_url"], "GRAPH IMAGE URL")

    def test_start_at_shortcode_media_graphvideo(self):
        def data_func():
            return self.graphvideo
        data = start_at_shortcode_media(data_func)
        got = data()
        self.assertEqual(got["__typename"], "GraphVideo")
        self.assertEqual(got["video_url"], "GRAPH VIDEO URL")

    def test_start_at_shortcode_media_graphsidecar(self):
        def data_func():
            return self.graphsidecar
        data = start_at_shortcode_media(data_func)
        got = data()
        self.assertEqual(got["__typename"], "GraphSidecar")
        self.assertEqual(got["edge_sidecar_to_children"]["edges"] \
            [0]["node"]["__typename"], "GraphVideo")
