from textnode import TextNode,TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type.value not in TextType:
        raise Exception(f"{text_node.text_type.value} is not a valid TextType.")
    match text_node.text_type.value:
        case "text":
            return LeafNode(None, text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "link":
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case "image":
            return LeafNode("img", "", {"src":text_node.url,
                                        "alt": text_node.text})


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        # Skip non-plain-text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        # Even number of parts means an opening delimiter without a closing one
        if len(parts) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")

        for i, part in enumerate(parts):
            if part == "":
                continue

            if i % 2 == 0:  # outside delimiters
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:          # inside delimiters
                new_nodes.append(TextNode(part, text_type))

    return new_nodes