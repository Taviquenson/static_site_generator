import unittest

from gencontent import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_eq(self):
        actual = extract_title("# This is a title")
        self.assertEqual(actual, "This is a title")

    def test_eq_double(self):
        actual = extract_title(
            """
# This is a title

# This is a second title that should be ignored
"""
        )
        self.assertEqual(actual, "This is a title")

    def test_eq_long(self):
        actual = extract_title(
            """
# title

this is a bunch

of text

- and
- a
- list
"""
        )
        self.assertEqual(actual, "title")

    def test_none(self):
        try:
            extract_title(
                """
no title
"""
            )
            self.fail("Should have raised an exception")
        except Exception as e:
            pass

    ''' extract_title '''
    def test_extract_title_basic(self):
        md = """# Title"""
        title = extract_title(md)
        self.assertEqual(title, "Title")

    def test_extract_title_multiple_lines(self):
        md = """

# Title


"""
        title = extract_title(md)
        self.assertEqual(title, "Title")

    def test_extract_title_exception(self):
        with self.assertRaises(ValueError):
            md = """## Title"""
            title = extract_title(md)
            print(md)

if __name__ == "__main__":
    unittest.main()
