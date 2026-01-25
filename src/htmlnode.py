class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        res = ''
        if self.props is None or len(self.props) == 0:
            return res
        for key, value in self.props.items():
            res = res + f' {key}="{value}"'
        return res
    
    def __repr__(self):
        return f"HTMLNode({self.tag!r}, {self.value!r}, {self.children!r}, {self.props!r})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value , props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value to convert to HTML")
        if self.tag is None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag!r}, {self.value!r}, {self.props!r})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent Node has no tag value.")
        if self.children is None:
            raise ValueError("Parent Node has no children.")
        res = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            res = res + child.to_html()
        res = res + f"</{self.tag}>"
        return res