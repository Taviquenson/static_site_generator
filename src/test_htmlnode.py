import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_zero_prop(self):
        node_empty = HTMLNode()
        response = node_empty.props_to_html()
        expected = ""
        self.assertEqual(response, expected)

    def test_props_to_html_one_prop(self):
        node_empty = HTMLNode(props={"href":"www.second.com"})
        response = node_empty.props_to_html()
        expected = ' href="www.second.com"'
        self.assertEqual(response, expected)

    def test_props_to_html_two_prop(self):
        node_empty = HTMLNode(props={"href":"www.third.com", "target":"_blank"})
        response = node_empty.props_to_html()
        expected = ' href="www.third.com" target="_blank"'
        self.assertEqual(response, expected)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected)
    
    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "The Heading One", {"href": "https://www.google.com", "target": "_blank"})
        expected = '<h1 href="https://www.google.com" target="_blank">The Heading One</h1>'
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_multiple_children(self):
        child_node_1 = LeafNode("b", "Bold text")
        child_node_2 = LeafNode(None, "Normal text")
        parent_node = ParentNode("p", [child_node_1, child_node_2])
        self.assertEqual(parent_node.to_html(), "<p><b>Bold text</b>Normal text</p>")

    def test_to_html_multiple_grandchildren(self):
        grandchild_node_1 = LeafNode("b", "grandchild")
        grandchild_node_2 = LeafNode(None, "grandchild 2")
        child_node = ParentNode("span", [grandchild_node_1, grandchild_node_2])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b>grandchild 2</span></div>",
        )

    def test_to_html_multiple_children_and_grandchildren(self):
        grandchild_node_1 = LeafNode("b", "grandchild")
        grandchild_node_2 = LeafNode(None, "grandchild 2")
        grandchild_node_3 = LeafNode("i", "grandchild 3")
        grandchild_node_4 = LeafNode(None, "grandchild 4")
        child_node_1 = ParentNode("span", [grandchild_node_1, grandchild_node_2])
        child_node_2 = ParentNode("p", [grandchild_node_3, grandchild_node_4])
        parent_node = ParentNode("div", [child_node_1, child_node_2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b>grandchild 2</span><p><i>grandchild 3</i>grandchild 4</p></div>",
        )

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
        
    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

if __name__ == "__main__":
    unittest.main()
