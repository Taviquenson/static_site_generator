import unittest
from markdown_blocks import *

class TestMarkdownToHTML(unittest.TestCase):
    ''' mardown_to_blocks() '''
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_single_block(self):
        md = """
This is **bolded** paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
            ],
        )
        
    def test_markdown_to_blocks_empty(self):
        md = """"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,[])

    def test_markdown_to_blocks_empty_blocks(self):
        md = """
This is **bolded** paragraph





- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "- This is a list\n- with items",
            ],
        )
    

    ''' block_to_block_type() '''
    def test_block_to_block_type_paragraph(self):
        block = "This is **bolded** paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_h1(self):
        block = "# This is h1 heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)
    
    def test_block_to_block_type_h3(self):
        block = "### This is h3 heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_h1_wrong(self):
        block = "#This is h1 heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_h7_wrong(self):
        block = "####### This unsupported h7 heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_code_one_line(self):
        block = "```This is code single line```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)
    
    def test_block_to_block_type_code_multiple_lines(self):
        block = '''```for line in lines:
    result = do_something(line)
    do_something_else(result)```'''
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_code_wrong(self):
        block = "```This is code single line``"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        block = ">This is a quote\n> with 2 lines"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_quote_wrong(self):
        block = ">This is a quote\nwith 2 lines"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_u_list(self):
        block = "- This is a list\n- with items"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
    
    def test_block_to_block_type_u_list_wrong(self):
        block = "- This is a list\n with items"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_o_list(self):
        block = "1. This is a list\n2. with items"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_o_list_wrong(self):
        block = "1. This is a list\n3. with items"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    