from enum import Enum
from html_node import HtmlNode, LeafNode
import re


class TextType(Enum):
    NORMAL_TEXT = "Normal text"
    BOLD_TEXT = "**Bold text**"
    ITALIC_TEXT = "_Italic text_"
    CODE_TEXT = "`Code text`"
    URL = "[anchor text](url)"
    IMAGES = "![alt text](url)"
    
class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url =url
        
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode(text={self.text}, text_type={self.text_type.value}, url={self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.NORMAL_TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD_TEXT:
        return LeafNode(tag=None, value=f"<b>{text_node.text}</b>")
    elif text_node.text_type == TextType.ITALIC_TEXT:
        return LeafNode(tag=None, value=f"<i>{text_node.text}</i>")
    elif text_node.text_type == TextType.CODE_TEXT:
        return LeafNode(tag=None, value=f"<code>{text_node.text}</code>")
    elif text_node.text_type == TextType.URL:
        return LeafNode(tag=None, value=f'<a href="{text_node.url}">{text_node.text}</a>')
    elif text_node.text_type == TextType.IMAGES:
        return LeafNode(tag=None, value=f'<img src="{text_node.url}" alt="{text_node.text}">')
    else:
        raise ValueError(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter is None:
        raise TypeError("Delimiter cannot be None")
    if text_type is None:
        raise ValueError("Text type cannot be None")
        
    result = []
    for node in old_nodes:
        # Check if node is a valid type
        if not isinstance(node, (TextNode, HtmlNode)):
            raise TypeError(f"Invalid node type: {type(node)}")
            
        # If it's an HtmlNode, add it as-is
        if isinstance(node, HtmlNode):
            result.append(node)
            continue
            
        # Check if TextNode has valid text_type
        if not isinstance(node.text_type, TextType):
            raise ValueError(f"Invalid text type: {node.text_type}")
            
        # Split TextNode content and create new nodes
        words = node.text.split(delimiter)
        for word in words:
            if word:  # Only create nodes for non-empty strings
                result.append(TextNode(word, text_type))
                
    return result

def extract_markdown_images(text):
    """
    Extracts image URLs from the given text using a regex pattern.
    """
    pattern = r'!\[(.*?\)]\((.*?)\)'
    return re.findall(pattern, text)

def extract_markdown_links(text):
    """
    Extracts anchor text and URLs from the given text using a regex pattern.
    """
    pattern = r'\[(.*?)\]\((.*?)\)'
    return re.findall(pattern, text)

def split_nodes_images(old_nodes):
    """
    Splits nodes based on image URLs.
    """
    result = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.IMAGES:
            images = extract_markdown_images(node.text)
            for alt_text, url in images:
                result.append(TextNode(alt_text, TextType.IMAGES, url))
        else:
            result.append(node)
    return result

def split_nodes_link(old_nodes):
    """
    Splits nodes based on anchor text and URLs.
    """
    result = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.URL:
            links = extract_markdown_links(node.text)
            for anchor_text, url in links:
                result.append(TextNode(anchor_text, TextType.URL, url))
        else:
            result.append(node)
    return result

def text_to_textnodes(text):
    """
    Converts a markdown-flavoured text into a list of TextNode objects.
    Uses predefined extraction functions for links and images.
    """
    # Split the text into parts based on the delimiters
    parts = re.split(r'(\*\*.*?\*\*|_.*?_|`.*?`|\[.*?\]\(.*?\)|!\[.*?\]\(.*?\))', text)
    
    nodes = []
    for part in parts:
        if not part:  # Skip empty parts
            continue
            
        if part.startswith("**") and part.endswith("**"):
            nodes.append(TextNode(part[2:-2], TextType.BOLD_TEXT))
        elif part.startswith("_") and part.endswith("_"):
            nodes.append(TextNode(part[1:-1], TextType.ITALIC_TEXT))
        elif part.startswith("`") and part.endswith("`"):
            nodes.append(TextNode(part[1:-1], TextType.CODE_TEXT))
        elif part.startswith("!["):  # Image handling
            images = extract_markdown_images(part)
            if images:
                alt_text, url = images[0]  # Take first match
                nodes.append(TextNode(alt_text, TextType.IMAGES, url))
        elif part.startswith("["):  # Link handling
            links = extract_markdown_links(part)
            if links:
                anchor_text, url = links[0]  # Take first match
                nodes.append(TextNode(anchor_text, TextType.URL, url))
        else:
            nodes.append(TextNode(part, TextType.NORMAL_TEXT))
    
    return nodes




