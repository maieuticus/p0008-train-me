"""Verify that the installed package can be imported."""

import unittest
import app


class PackageTest(unittest.TestCase):
    def test_importable(self):
        self.assertEqual(app.__name__, "app")
        self.assertIsNotNone(app.__file__, "The installed package must not be an empty namespace.")
