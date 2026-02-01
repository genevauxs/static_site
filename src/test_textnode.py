import unittest

from textnode import TextNode, TextType
from functions import text_node_to_html_node, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_noteq(self):
        node1 = TextNode("This is a text node", TextType.IMAGE, "ABCD")
        node2 = TextNode("This is a text node", TextType.IMAGE, "abcd")
        self.assertNotEqual(node1, node2)
    
    def test_noteq2(self):
        node1 = TextNode("This is a text node", TextType.IMAGE, "ABCD")
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node1, node2)

    def test_inequality_different_text(self):
        node1 = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("Goodbye", TextType.TEXT)
        self.assertNotEqual(node1, node2)

    def test_equality_with_url(self):
        node1 = TextNode("Click me", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Click me", TextType.LINK, "https://boot.dev")
        self.assertEqual(node1, node2)

    def test_inequality_different_url(self):
        node1 = TextNode("Click me", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Click me", TextType.LINK, "https://example.com")
        self.assertNotEqual(node1, node2)

    def test_equality_when_url_is_none(self):
        node1 = TextNode("Plain text", TextType.TEXT, None)
        node2 = TextNode("Plain text", TextType.TEXT, None)
        self.assertEqual(node1, node2)

    def test_inequality_when_one_url_is_none(self):
        node1 = TextNode("Link text", TextType.LINK, None)
        node2 = TextNode("Link text", TextType.LINK, "https://boot.dev")
        self.assertNotEqual(node1, node2)

    def test_inequality_different_text_types_same_text(self):
        node1 = TextNode("Same text", TextType.TEXT)
        node2 = TextNode("Same text", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text2(self):
        node = TextNode("Bold Text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold Text")

    def test_link_different_url(self):
        node = TextNode("Docs", TextType.LINK, "https://docs.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Docs")
        self.assertEqual(html_node.props, {"href": "https://docs.example.com"})
    def test_image(self):
        node = TextNode("A cute bear", TextType.IMAGE, "https://example.com/bear.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/bear.png", "alt": "A cute bear"},
        )

    def test_no_delimiters_returns_same_text(self):
        node = TextNode("just plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "just plain text")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_single_bold_section(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_single_italic_section(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)

    def test_inline_code_section(self):
        node = TextNode("Use `code()` here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Use ")
        self.assertEqual(result[1].text, "code()")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " here")

    def test_non_text_nodes_untouched(self):
        node1 = TextNode("plain", TextType.TEXT)
        node2 = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1], node2)

    def test_raises_on_unclosed_delimiter(self):
        node = TextNode("This is **broken text", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

if __name__ == "__main__":
    unittest.main()