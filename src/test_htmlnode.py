import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_leaf_no_value_raises(self):
        from src.htmlnode import LeafNode
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    def test_leaf_raw_text_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_empty_string_value(self):
        node = LeafNode("span", "")
        self.assertEqual(node.to_html(), "<span></span>")
    
    def test_leaf_multiple_props(self):
        node = LeafNode("a", "Click", {"href": "https://example.com", "target": "_blank"})
        html = node.to_html()
        self.assertIn('<a ', html)
        self.assertIn('href="https://example.com"', html)
        self.assertIn('target="_blank"', html)
        self.assertIn(">Click</a>", html)

    def test_leaf_props_non_string_values(self):
        node = LeafNode("input", "", {"type": "number", "value": 10})
        html = node.to_html()
        self.assertIn('value="10"', html)

    def test_leaf_empty_tag_treated_as_tag(self):
        node = LeafNode("", "hi")
        self.assertEqual(node.to_html(), "<>hi</>")
    
    def test_leaf_repr_has_no_children(self):
        node = LeafNode("p", "Hello", {"class": "greeting"})
        r = repr(node)
        self.assertIn("LeafNode", r)
        self.assertIn("p", r)
        self.assertIn("Hello", r)
        self.assertNotIn("children", r.lower())
    
    def test_props_to_html_none(self):
        node = HTMLNode("p")
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_basic(self):
        node = HTMLNode("a", props={"href": "https://example.com", "target": "_blank"})
        props_str = node.props_to_html()
        self.assertTrue(props_str.startswith(" "))
        self.assertIn('href="https://example.com"', props_str)
        self.assertIn('target="_blank"', props_str)

    def test_htmlnode_value_and_children_conflict(self):
        from src.htmlnode import HTMLNode, LeafNode
        child = LeafNode(None, "child")
        node = HTMLNode("p", value="parent", children=[child])
        with self.assertRaises(Exception):
            node.to_html()

    def test_htmlnode_repr_children_count(self):
        from src.htmlnode import HTMLNode, LeafNode
        child = LeafNode("span", "x")
        node = HTMLNode("div", children=[child])
        r = repr(node)
        self.assertIn("div", r)
        self.assertIn("leafnode", r.lower())

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

    def test_parentnode_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold"),
                LeafNode(None, " and "),
                LeafNode("i", "italic"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold</b> and <i>italic</i></p>",
        )

    def test_parentnode_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode(None, "content")],
            {"class": "box", "id": "main"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="box" id="main">content</div>',
        )

    def test_parentnode_nested_parents(self):
        inner = ParentNode(
            "span",
            [LeafNode("b", "inside")],
        )
        outer = ParentNode(
            "div",
            [inner],
        )
        self.assertEqual(
            outer.to_html(),
            "<div><span><b>inside</b></span></div>",
        )

    def test_parentnode_child_is_parentnode(self):
        child = ParentNode(
            "ul",
            [
                LeafNode("li", "one"),
                LeafNode("li", "two"),
            ],
        )
        parent = ParentNode("div", [child])
        self.assertEqual(
            parent.to_html(),
            "<div><ul><li>one</li><li>two</li></ul></div>",
        )

    def test_parentnode_raises_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode(None, "hi")]).to_html()

    def test_parentnode_raises_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()
            
    def test_parentnode_three_levels_deep(self):
        grandchild = LeafNode("b", "deep")
        child = ParentNode("span", [grandchild])
        parent = ParentNode("div", [child])
        self.assertEqual(
            parent.to_html(),
            "<div><span><b>deep</b></span></div>",
        )

    def test_parentnode_four_levels_mixed_leaf_and_parent(self):
        deepest = LeafNode(None, "core")
        level3 = ParentNode("em", [deepest])
        level2 = ParentNode("span", [LeafNode(None, "start "), level3])
        level1 = ParentNode("div", [level2, LeafNode(None, " end")])
        self.assertEqual(
            level1.to_html(),
            "<div><span>start <em>core</em></span> end</div>",
        )

    def test_parentnode_siblings_with_nested_children(self):
        left = ParentNode(
            "span",
            [
                LeafNode("i", "left-1"),
                LeafNode(None, " & "),
                LeafNode("b", "left-2"),
            ],
        )
        right = ParentNode(
            "span",
            [
                LeafNode(None, "right-1 "),
                ParentNode("u", [LeafNode(None, "right-2")]),
            ],
        )
        root = ParentNode("div", [left, right])
        self.assertEqual(
            root.to_html(),
            "<div><span><i>left-1</i> & <b>left-2</b></span>"
            "<span>right-1 <u>right-2</u></span></div>",
        )

    def test_parentnode_nested_list_structure(self):
        li1 = LeafNode("li", "first")
        li2 = LeafNode("li", "second")
        inner_ul = ParentNode("ul", [li1, li2])

        li_outer = ParentNode("li", [LeafNode(None, "outer "), inner_ul])
        outer_ul = ParentNode("ul", [li_outer])

        self.assertEqual(
            outer_ul.to_html(),
            "<ul><li>outer <ul><li>first</li><li>second</li></ul></li></ul>",
        )

    def test_parentnode_deep_chain_single_child_each_level(self):
        # div > span > em > strong > "text"
        level4 = ParentNode("strong", [LeafNode(None, "text")])
        level3 = ParentNode("em", [level4])
        level2 = ParentNode("span", [level3])
        level1 = ParentNode("div", [level2])

        self.assertEqual(
            level1.to_html(),
            "<div><span><em><strong>text</strong></em></span></div>",
        )