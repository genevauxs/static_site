from textnode import TextNode
from htmlnode import HTMLNode
def main():
    testing = HTMLNode(props= {
        "href":"www.google.com"
    })
    print(testing.props_to_html())

main()