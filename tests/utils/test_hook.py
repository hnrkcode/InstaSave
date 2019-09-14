import json
import os.path
import unittest
from unittest.mock import patch

from utils import hook

DATA = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "test_data", "json"
)


class TestHooks(unittest.TestCase):
    def test_private_profile_returns_true(self):
        with open(os.path.join(DATA, "private.json")) as f:
            private_account = json.loads(f.read())
        self.assertTrue(hook.private_profile(private_account))

    def test_private_profile_returns_false(self):
        with open(os.path.join(DATA, "public.json")) as f:
            public_account = json.loads(f.read())
        self.assertFalse(hook.private_profile(public_account))

    def test_hashtag_post_count_return_number(self):
        with open(os.path.join(DATA, "hashtag.json")) as f:
            hashtag_page = json.loads(f.read())
        self.assertEqual(hook.hashtag_post_count(hashtag_page), 21380914)

    def test_hashtag_post_count_return_integer_type(self):
        with open(os.path.join(DATA, "hashtag.json")) as f:
            hashtag_page = json.loads(f.read())
        self.assertIsInstance(hook.hashtag_post_count(hashtag_page), int)

    def test_user_post_count_return_number(self):
        with open(os.path.join(DATA, "public.json")) as f:
            user_page = json.loads(f.read())
        self.assertEqual(hook.user_post_count(user_page), 6026)

    def test_user_post_count_return_integer_type(self):
        with open(os.path.join(DATA, "public.json")) as f:
            user_page = json.loads(f.read())
        self.assertIsInstance(hook.user_post_count(user_page), int)

    def test_shortcode_media_return_post_type(self):
        with open(os.path.join(DATA, "graphimage.json")) as f:
            post_page = json.loads(f.read())
        post = hook.shortcode_media(post_page)
        self.assertEqual(post["__typename"], "GraphImage")

    def test_shortcode_media_return_shortcode(self):
        with open(os.path.join(DATA, "graphimage.json")) as f:
            post_page = json.loads(f.read())
        post = hook.shortcode_media(post_page)
        self.assertEqual(post["shortcode"], "B0RA4kfgX71")

    def test_shortcode_media_return_username(self):
        with open(os.path.join(DATA, "graphimage.json")) as f:
            post_page = json.loads(f.read())
        post = hook.shortcode_media(post_page)
        self.assertEqual(post["owner"]["username"], "instagram")

    def test_shortcode_media_return_timestamp(self):
        with open(os.path.join(DATA, "graphimage.json")) as f:
            post_page = json.loads(f.read())
        post = hook.shortcode_media(post_page)
        self.assertIsInstance(post["taken_at_timestamp"], int)
