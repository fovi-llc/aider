import unittest
from your_refactoring_module import extract_method  # Replace with actual import

class TestExtractMethod(unittest.TestCase):

    def test_extract_method(self):
        # Setup: Define a code block and the expected result after extraction
        code_block = """
def some_function():
    a = 1
    b = 2
    c = a + b  # This should be extracted into a new method
    return c
"""
        expected_result = """
def some_function():
    return new_method()

def new_method():
    a = 1
    b = 2
    return a + b
"""

        # Exercise: Call the extract method functionality
        result = extract_method(code_block, 'new_method', lines_to_extract=(3, 3))

        # Verify: Check if the result matches the expected result
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
