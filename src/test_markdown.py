import unittest
from markdown import split_nodes_delimiter
from textnode import TextNode, TextType

class TestMarkdown(unittest.TestCase):
    def test_code_in_text(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_bold_in_text(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_nodes(self):
        node_italic_in_text = TextNode("Text with a _italic block_ word", TextType.TEXT)
        node_text = TextNode("This is just text", TextType.TEXT)
        node_italic = TextNode("A whole italic block", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node_italic_in_text, node_text, node_italic], "_", TextType.ITALIC)
        expected = [
            TextNode("Text with a ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
            TextNode("This is just text", TextType.TEXT),
            TextNode("A whole italic block", TextType.ITALIC)
        ]
        self.assertEqual(new_nodes, expected)

    def test_incomplete_delimiter(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(ValueError):
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
    def test_one_block_in_text(self):
        node = TextNode("**bold block**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("bold block", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_starting_block_in_text(self):
        node = TextNode("`code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_ending_block_in_text(self):
        node = TextNode("This is text with a `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)