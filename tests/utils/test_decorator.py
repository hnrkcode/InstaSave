import io
import sys
import unittest

from instasave.utils import decorator


class TestDecorators(unittest.TestCase):
    def setUp(self):
        class Cls:
            def __init__(self, verbose):
                self.verbose = verbose

            @decorator.count_calls
            def func(self):
                pass

        def call_prints(calls, verbose):
            captured = io.StringIO()
            sys.stdout = captured
            for i in range(calls):
                Cls(verbose).func()
            sys.stdout = sys.__stdout__
            return captured.getvalue()

        self.output = call_prints

    def test_unique_filename(self):
        def func():
            return "generic_filename.jpg"

        filename = decorator.unique_filename(func)
        self.assertRegex(filename(), "^generic_filename_[0-9a-z]{20}.jpg$")

    def test_count_calls_verbose_off(self):
        calls = 5
        print_output = "." * calls
        self.assertEqual(self.output(calls, False), print_output)

    def test_count_calls_verbose_on(self):
        calls = 5
        print_output = "".join(
            [f"Post {post}\n" for post in range(1, calls + 1)]
        )
        self.assertEqual(self.output(calls, True), print_output)
