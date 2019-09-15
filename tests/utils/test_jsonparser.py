import json
import os.path
import unittest
from unittest.mock import patch

from instasave.utils import hook
from instasave.utils.jsonparser import parse_json


class TestJsonParser(unittest.TestCase):
    def setUp(self):
        data = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "test_data", "html"
        )

        with open(os.path.join(data, "graphimage_html.txt")) as f:
            self.graphimage = f.read()
        with open(os.path.join(data, "graphvideo_html.txt")) as f:
            self.graphvideo = f.read()
        with open(os.path.join(data, "graphsidecar_html.txt")) as f:
            self.graphsidecar = f.read()
        with open(os.path.join(data, "hashtag_html.txt")) as f:
            self.hashtag = f.read()
        with open(os.path.join(data, "username_html.txt")) as f:
            self.username = f.read()

        self.selector = "body > script:nth-child(6)"

    def test_parse_json_username(self):
        json_data = parse_json(
            self.username, self.selector, hook.private_profile
        )
        self.assertFalse(json_data)

    def test_parse_json_hashtag(self):
        json_data = parse_json(
            self.hashtag, self.selector, hook.hashtag_post_count
        )
        self.assertEqual(json_data, 105667)

    def test_parse_json_post_graphimage(self):
        json_data = parse_json(
            self.graphimage, self.selector, hook.shortcode_media
        )
        self.assertEqual(json_data["__typename"], "GraphImage")

    def test_parse_json_post_graphvideo(self):
        json_data = parse_json(
            self.graphvideo, self.selector, hook.shortcode_media
        )
        self.assertEqual(json_data["__typename"], "GraphVideo")

    def test_parse_json_post_graphsidecar(self):
        json_data = parse_json(
            self.graphsidecar, self.selector, hook.shortcode_media
        )
        self.assertEqual(json_data["__typename"], "GraphSidecar")
