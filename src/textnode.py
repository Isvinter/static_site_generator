from enum import Enum
from html_node import HtmlNode, LeafNode, ParentNode
import re
import os
import shutil
import re

class TextType(Enum):
    NORMAL_TEXT = "Normal text"
    BOLD_TEXT = "**Bold text**"
    ITALIC_TEXT = "_Italic text_"
    CODE_TEXT = "`Code text`"
    URL = "[anchor text](url)"
    IMAGES = "![alt text](url)"
    
class BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    UNORDERED_LIST = "Unordered list"
    ORDERED_LIST = "Ordered list"
    
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
    Extracts image URLs and alt text from markdown.
    Returns a list of tuples: [(alt_text, url), ...]
    """
    pattern = r'!\[(.*?)\]\((.*?)\)'  
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

def markdown_to_blocks(markdown):
    """
    Converts a markdown string into a list of TextNode objects.
    """
    # Split the markdown into lines
    lines = markdown.split("\n\n")
    
    blocks = []
    for line in lines:
        if line.strip():  # Skip empty lines
            blocks.append(text_to_textnodes(line))
    
    return blocks

def block_to_blocktype(block: str):
    """
    Converts a block of text into a BlockType.
    """
    if block.startswith("# "):
        return BlockType.HEADING
    elif block.startswith("## "):
        return BlockType.HEADING
    elif block.startswith("### "):
        return BlockType.HEADING
    elif block.startswith("#### "):
        return BlockType.HEADING
    elif block.startswith("##### "):
        return BlockType.HEADING
    elif block.startswith("###### "):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        return BlockType.ORDERED_LIST
    elif block.startswith("> "):
        return BlockType.QUOTE
    else:
        return BlockType.PARAGRAPH

def generate_children_from_textnodes(text_nodes):
    """
    Generates a list of HTMLNode objects from a list of TextNode objects.
    """
    children = []
    for node in text_nodes:
        if isinstance(node, TextNode):
            children.append(text_node_to_html_node(node))
        elif isinstance(node, HtmlNode):
            children.append(node)
        else:
            raise TypeError(f"Invalid node type: {type(node)}")
    return children

def markdown_to_html_node(markdown: str) -> ParentNode:
    # 1) Roh‑Blocks anhand doppelter Leerzeilen trennen
    raw_blocks = markdown.split("\n\n")
    html_nodes = []

    for raw in raw_blocks:
        if not raw.strip():
            continue

        # 2) Erstelle die Inline‑Nodes **direkt** aus dem ganzen raw‑Text
        block_type = block_to_blocktype(raw)

        if block_type == BlockType.UNORDERED_LIST:
            # raw ist der gesamte Listen-Block, z.B.
            # "- You can …\n- It can …\n- Disney …\n- It created …"
            lines = raw.split("\n")
            list_items = []
            for line in lines:
                # entferne das "- " vorne
                text = re.sub(r'^-\s*', '', line)
                # parsen wir jede Zeile einzeln auf Inline‑Markdown
                inline_nodes = text_to_textnodes(text)
                children    = generate_children_from_textnodes(inline_nodes)
                list_items.append(ParentNode(tag="li", children=children))
            html_nodes.append(ParentNode(tag="ul", children=list_items))


        elif block_type == BlockType.ORDERED_LIST:
            # raw ist hier der gesamte Block-String, z.B.
            # "1. Gandalf\n2. Bilbo\n3. Sam\n…"
            lines = raw.split("\n")
            list_items = []
            for line in lines:
                # entferne die Nummern-Markierung "1. ", "2. " etc.
                text = re.sub(r'^\d+\.\s*', '', line)
                # parsen wir jede Zeile einzeln auf Inline‑Markdown:
                inline_nodes = text_to_textnodes(text)
                children = generate_children_from_textnodes(inline_nodes)
                list_items.append(ParentNode(tag="li", children=children))
            html_nodes.append(ParentNode(tag="ol", children=list_items))


        elif block_type == BlockType.HEADING:
            # … wie gehabt, nur mit raw statt block[0].text …
            level = len(re.match(r'^(#+)', raw).group(1))
            text  = re.sub(r'^#+\s*', '', raw)
            inline = text_to_textnodes(text)
            children = generate_children_from_textnodes(inline)
            tag = f"h{level}" if 1 <= level <= 6 else "h1"
            html_nodes.append(ParentNode(tag=tag, children=children))

        elif block_type == BlockType.CODE:
            # pre‑Block: die erste Zeile inkl. Backticks
            # hier kannst du raw verwenden oder weiterhin block‑Nodes
            code_node = LeafNode(value=re.sub(r'```', '', raw), tag="code")
            html_nodes.append(ParentNode(tag="pre", children=[code_node]))

        elif block_type == BlockType.QUOTE:
            inline = text_to_textnodes(raw.lstrip("> ").replace("\n> ", "\n"))
            children = generate_children_from_textnodes(inline)
            html_nodes.append(ParentNode(tag="blockquote", children=children))

        else:  # Paragraph
            inline = text_to_textnodes(raw)
            children = generate_children_from_textnodes(inline)
            html_nodes.append(ParentNode(tag="p", children=children))

    return ParentNode(tag="div", children=html_nodes)

def extract_title_from_markdown(markdown):
    """
    Extracts the title from a markdown document.
    """
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title found in the markdown document")

def copy_all_content(source_folder: str, destination_folder: str):
    """copy all content from source_folder to destination_folder"""
    # Check if the source folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    # delete all content in destination folder
    for item in os.listdir(destination_folder):
        item_path = os.path.join(destination_folder, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)  # Use rmtree instead of rmdir
        else:
            os.remove(item_path)
    # copy all content from source folder to destination folder
    for item in os.listdir(source_folder):
        source_path = os.path.join(source_folder, item)
        destination_path = os.path.join(destination_folder, item)
        if os.path.isdir(source_path):
            copy_all_content(source_path, destination_path)
        else:
            with open(source_path, 'rb') as src_file:
                print(f"Copying {source_path} to {destination_path}")
                with open(destination_path, 'wb') as dest_file:
                    dest_file.write(src_file.read())
                    
def generate_page(content_path: str, template_path: str, output_path: str, basepath: str = ""):
    """
    Generates an HTML page using markdown content and an HTML template.
    Replaces {{ Title }}, {{ Content }} placeholders and rewrites absolute href/src
    so they work unter GitHub Pages.
    """
    try:
        # --- Einlesen ---
        with open(content_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()

        # --- Markdown→HTML ---
        try:
            title = extract_title_from_markdown(markdown_content)
        except:
            title = "My Static Site"
        html_node   = markdown_to_html_node(markdown_content)
        html_string = html_node.to_html()

        # --- Platzhalter ersetzen ---
        final_html  = re.sub(r"\{\{\s*Title\s*\}\}", title, template)
        final_html  = re.sub(r"\{\{\s*Content\s*\}\}", html_string, final_html)

        # --- href/src umschreiben ---
        if basepath:
            final_html = re.sub(
                r'(href|src)=["\']\/', 
                rf'\1="{basepath}/', 
                final_html
            )

        # --- Datei schreiben ---
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_html)

        print(f"Successfully generated {output_path}")

    except Exception as e:
        print(f"Error generating page: {e}")

        
        
def generate_pages_recursive(content_dir: str, template_path: str, dest_dir: str, basepath: str):
    if not os.path.exists(content_dir):
        raise ValueError(f"Content directory does not exist: {content_dir}")

    for root, _, files in os.walk(content_dir):
        for file in files:
            if not file.endswith('.md'):
                continue
            full_md     = os.path.join(root, file)
            rel_path    = os.path.relpath(full_md, content_dir)
            out_html    = os.path.join(dest_dir, os.path.splitext(rel_path)[0] + ".html")

            generate_page(full_md, template_path, out_html, basepath)
