import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode(props= {
            "href": "https://www.google.com",
            })
        node2 = HTMLNode(props= {
            "href": "https://www.google.com",
            })
        self.assertEqual(node1.props_to_html(), node2.props_to_html())

    def test_noteq(self):
        node1 = HTMLNode(props= {
            "href": "https://www.google.com",
            "target": "_blanks",
            })
        node2 = HTMLNode(props= {
            "href": "https://www.google.com",
            "target": "_blank",
            })
        self.assertNotEqual(node1.props_to_html, node2.props_to_html)

    def test_noteq2(self):
        node1 = HTMLNode(props= {
            "href": "https://www.google.com",
            "target": "_blanks",
            })
        node2 = HTMLNode(props= {})
        self.assertNotEqual(node1.props_to_html, node2.props_to_html)
    
    def test_noteq3(self):
        node1 = HTMLNode(props= {
            "href": "https://www.google.com",
            "target": "_blanks",
            })
        node2 = HTMLNode(props= {
            "href": "https://www.google.com",
            " target": "_blank",
            })
        self.assertNotEqual(node1.props_to_html, node2.props_to_html)