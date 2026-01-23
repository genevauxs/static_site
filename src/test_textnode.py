import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()