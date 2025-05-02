import unittest

from textnode import *
from html_node import HtmlNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
        
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        expected_repr = "TextNode(text=This is a text node, text_type=**Bold text**, url=None)"
        self.assertEqual(repr(node), expected_repr)
        
    def test_eq_different_text(self):
        htis_node = TextNode("This is a text node", TextType.BOLD_TEXT)
        other_node = TextNode("This is a different text node", TextType.BOLD_TEXT)
        self.assertNotEqual(htis_node, other_node)
        
    def test_eq_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        other_node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        self.assertNotEqual(node, other_node)
    
    def test_eq_different_url(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT, "https://example.com")
        other_node = TextNode("This is a text node", TextType.BOLD_TEXT, "https://different.com")
        self.assertNotEqual(node, other_node)
        
    def test_eq_different_object(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        other_node = "This is not a TextNode"
        self.assertNotEqual(node, other_node)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_text_node_to_html_node(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "<b>This is a text node</b>")
    
    def test_text_node_to_html_node_with_url(self):
        node = TextNode("This is a text node", TextType.URL, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, '<a href="https://example.com">This is a text node</a>')
        
    def test_text_node_to_html_node_with_image(self):
        node = TextNode("This is a text node", TextType.IMAGES, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, '<img src="https://example.com/image.png" alt="This is a text node">')
        
    def test_text_node_to_html_node_with_invalid_type(self):
        node = TextNode("This is a text node", "Invalid type")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
            
    def test_split_nodes_delimiter(self):
        old_nodes = [
            TextNode("This is a text node", TextType.NORMAL_TEXT),
            TextNode("This is another text node", TextType.NORMAL_TEXT),
        ]
        delimiter = " "
        text_type = TextType.NORMAL_TEXT
        result = list(split_nodes_delimiter(old_nodes, delimiter, text_type))
        expected_result = [
            TextNode("This", text_type),
            TextNode("is", text_type),
            TextNode("a", text_type),
            TextNode("text", text_type),
            TextNode("node", text_type),
            TextNode("This", text_type),
            TextNode("is", text_type),
            TextNode("another", text_type),
            TextNode("text", text_type),
            TextNode("node", text_type),
        ]
        self.assertEqual(result, expected_result)
        
    def test_split_nodes_delimiter_with_non_text_node(self):
        old_nodes = [
            TextNode("This is a text node", TextType.NORMAL_TEXT),
            HtmlNode("div", "This is a div node", [], {"class": "text"}),
        ]
        delimiter = " "
        text_type = TextType.NORMAL_TEXT
        result = list(split_nodes_delimiter(old_nodes, delimiter, text_type))
        expected_result = [
            TextNode("This", text_type),
            TextNode("is", text_type),
            TextNode("a", text_type),
            TextNode("text", text_type),
            TextNode("node", text_type),
            HtmlNode("div", "This is a div node", [], {"class": "text"}),
        ]
        self.assertEqual(result, expected_result)
        
    def test_split_nodes_delimiter_with_no_nodes(self):
        old_nodes = []
        delimiter = " "
        text_type = TextType.NORMAL_TEXT
        result = list(split_nodes_delimiter(old_nodes, delimiter, text_type))
        expected_result = []
        self.assertEqual(result, expected_result)
        
    def test_split_nodes_delimiter_with_invalid_text_type(self):
        old_nodes = [
            TextNode("This is a text node", "Invalid type"),
        ]
        delimiter = " "
        text_type = "Invalid type"
        with self.assertRaises(ValueError):
            list(split_nodes_delimiter(old_nodes, delimiter, text_type))
            
    def test_split_nodes_delimiter_with_invalid_node(self):
        old_nodes = [
            TextNode("This is a text node", TextType.NORMAL_TEXT),
            "This is not a valid node",
        ]
        delimiter = " "
        text_type = TextType.NORMAL_TEXT
        with self.assertRaises(TypeError):
            list(split_nodes_delimiter(old_nodes, delimiter, text_type))
            
    def test_split_nodes_delimiter_with_invalid_delimiter(self):
        old_nodes = [
            TextNode("This is a text node", TextType.NORMAL_TEXT),
            TextNode("This is another text node", TextType.NORMAL_TEXT),
        ]
        delimiter = None
        text_type = TextType.NORMAL_TEXT
        with self.assertRaises(TypeError):
            list(split_nodes_delimiter(old_nodes, delimiter, text_type))
            
    def test_split_nodes_delimiter_with_invalid_text_type(self):
        old_nodes = [
            TextNode("This is a text node", TextType.NORMAL_TEXT),
            TextNode("This is another text node", TextType.NORMAL_TEXT),
        ]
        delimiter = " "
        text_type = None
        with self.assertRaises(ValueError):
            list(split_nodes_delimiter(old_nodes, delimiter, text_type))
            

def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

def test_extract_markdown_images_no_match(self):
    matches = extract_markdown_images(
        "This is text without an image"
    )
    self.assertListEqual([], matches)

def test_extract_markdown_images_invalid_url(self):
    with self.assertRaises(ValueError):
        extract_markdown_images(
            "This is text with an ![image](invalid_url)"
        )
def test_extract_markdown_images_no_text(self):
    matches = extract_markdown_images(
        ""
    )
    self.assertListEqual([], matches)

def test_extract_markdown_images_no_image(self):
    matches = extract_markdown_images(
        "This is text without an image"
    )
    self.assertListEqual([], matches)
    
def test_extract_markdown_links(self):
    matches = extract_markdown_links(
        "this is an url [example](www.example.com)"
        )
    self.assertListEqual([("example", "www.example.com")], matches)
    
def test_extract_markdown_links_no_match(self):
    matches = extract_markdown_links(
        "This is text without an url"
    )
    self.assertListEqual([], matches)
    
def test_extract_markdown_links_invalid_url(self):
    with self.assertRaises(ValueError):
        extract_markdown_links(
            "This is text with an [example](invalid_url)"
        )

def test_extract_markdown_links_no_text(self):
    matches = extract_markdown_links(
        ""
    )
    self.assertListEqual([], matches)
    
def test_extract_markdown_links_no_url(self):
    matches = extract_markdown_links(
        "This is text without an url"
    )
    self.assertListEqual([], matches)

def test_split_images(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_images([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )

def test_split_images_no_match(self):
    node = TextNode(
        "This is text without an image",
        TextType.TEXT,
    )
    new_nodes = split_nodes_images([node])
    self.assertListEqual([node], new_nodes)
        
def test_split_images_invalid_node(self):
    node = "This is not a valid node"
    with self.assertRaises(TypeError):
        split_nodes_images([node])

def test_split_images_no_nodes(self):
    nodes = []
    new_nodes = split_nodes_images(nodes)
    self.assertListEqual([], new_nodes)
    
def test_split_links(self):
    node = TextNode(
        "This is text with an [example](www.example.com) and another [second link](www.secondlink.com)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("example", TextType.URL, "www.example.com"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second link", TextType.URL, "www.secondlink.com"),
        ],
        new_nodes,
    )

def test_split_links_no_match(self):
    node = TextNode(
        "This is text without an url",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual([node], new_nodes)
    
def test_split_links_invalid_node(self):
    node = "This is not a valid node"
    with self.assertRaises(TypeError):
        split_nodes_link([node])

def test_split_links_no_nodes(self):
    nodes = []
    new_nodes = split_nodes_link(nodes)
    self.assertListEqual([], new_nodes)
    
def test_split_links_invalid_text_type(self):   
    node = TextNode(
        "This is text with an [example](www.example.com)",
        "Invalid type",
    )
    with self.assertRaises(ValueError):
        split_nodes_link([node])

def test_text_to_textnodes(self):
    text = "This is a text node"
    nodes = text_to_textnodes(text)
    self.assertEqual(len(nodes), 1)
    self.assertEqual(nodes[0].text, text)
    self.assertEqual(nodes[0].text_type, TextType.NORMAL_TEXT)
    
def test_text_to_textnodes_with_images(self):
    text = "This is a text node ![image](https://i.imgur.com/zjjcJKZ.png)"
    nodes = text_to_textnodes(text)
    self.assertEqual(len(nodes), 2)
    self.assertEqual(nodes[0].text, "This is a text node ")
    self.assertEqual(nodes[0].text_type, TextType.NORMAL_TEXT)
    self.assertEqual(nodes[1].text, "image")
    self.assertEqual(nodes[1].text_type, TextType.IMAGES)
    self.assertEqual(nodes[1].url, "https://i.imgur.com/zjjcJKZ.png")
    
def test_text_to_textnodes_with_links(self):
    text = "This is a text node [example](www.example.com)"
    nodes = text_to_textnodes(text)
    self.assertEqual(len(nodes), 2)
    self.assertEqual(nodes[0].text, "This is a text node ")
    self.assertEqual(nodes[0].text_type, TextType.NORMAL_TEXT)
    self.assertEqual(nodes[1].text, "example")
    self.assertEqual(nodes[1].text_type, TextType.URL)
    self.assertEqual(nodes[1].url, "www.example.com")
    
def test_text_to_textnodes_with_bold_text(self):
    text = "This is a **bold** text node"
    nodes = text_to_textnodes(text)
    self.assertEqual(len(nodes), 3)
    self.assertEqual(nodes[0].text, "This is a ")
    self.assertEqual(nodes[0].text_type, TextType.NORMAL_TEXT)
    self.assertEqual(nodes[1].text, "bold")
    self.assertEqual(nodes[1].text_type, TextType.BOLD_TEXT)
    self.assertEqual(nodes[2].text, " text node")
    self.assertEqual(nodes[2].text_type, TextType.NORMAL_TEXT)

def test_text_to_textnodes_with_italic_text(self):
    text = "This is a _italic_ text node"
    nodes = text_to_textnodes(text)
    self.assertEqual(len(nodes), 3)
    self.assertEqual(nodes[0].text, "This is a ")
    self.assertEqual(nodes[0].text_type, TextType.NORMAL_TEXT)
    self.assertEqual(nodes[1].text, "italic")
    self.assertEqual(nodes[1].text_type, TextType.ITALIC_TEXT)
    self.assertEqual(nodes[2].text, " text node")
    self.assertEqual(nodes[2].text_type, TextType.NORMAL_TEXT)
    
def test_text_to_textnodes_with_code_text(self):
    text = "This is a `code` text node"
    nodes = text_to_textnodes(text)
    self.assertEqual(len(nodes), 3)
    self.assertEqual(nodes[0].text, "This is a ")
    self.assertEqual(nodes[0].text_type, TextType.NORMAL_TEXT)
    self.assertEqual(nodes[1].text, "code")
    self.assertEqual(nodes[1].text_type, TextType.CODE_TEXT)
    self.assertEqual(nodes[2].text, " text node")
    self.assertEqual(nodes[2].text_type, TextType.NORMAL_TEXT)
    
def test_markdown_to_blocks(self):
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )
    
def test_markdown_to_blocks_empty_string(self):
    md = ""
    blocks = markdown_to_blocks(md)
    self.assertEqual(blocks, [])
    
def test_markdown_to_blocks_no_newline(self):
    md = "This is a single line of text"
    blocks = markdown_to_blocks(md)
    self.assertEqual(blocks, ["This is a single line of text"])
    
def test_block_to_blocktype(self):
    block = "# This is a heading"
    block_type = block_to_blocktype(block)
    self.assertEqual(block_type, BlockType.HEADING)
    
def test_block_to_blocktype_code(self):
    block = "```python\nprint('Hello, world!')\n```"
    block_type = block_to_blocktype(block)
    self.assertEqual(block_type, BlockType.CODE)
    
def test_block_to_blocktype_list(self):
    block = "- This is a list item"
    block_type = block_to_blocktype(block)
    self.assertEqual(block_type, BlockType.LIST)
    
def test_block_to_blocktype_no_match(self):
    block = "This is a normal text block"
    block_type = block_to_blocktype(block)
    self.assertEqual(block_type, BlockType.NORMAL_TEXT)
    
def test_block_to_blocktype_empty_string(self):
    block = ""
    block_type = block_to_blocktype(block)
    self.assertEqual(block_type, BlockType.NORMAL_TEXT)
    
def test_block_to_blocktype_invalid_type(self):
    block = 12345
    with self.assertRaises(TypeError):
        block_to_blocktype(block)

def test_block_to_blocktype_invalid_string(self):
    block = "This is a string without any special formatting"
    block_type = block_to_blocktype(block)
    self.assertEqual(block_type, BlockType.NORMAL_TEXT)
    
def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

def test_codeblock_with_language(self):
    md = """
```python
def hello_world():
    print("Hello, world!")
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        '<div><pre><code class="language-python">def hello_world():\n    print("Hello, world!")\n</code></pre></div>',
    )
    
def test_heading_block(self):
    md = """
# This is a heading
This is a paragraph
"""
    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        '<div><h1>This is a heading</h1><p>This is a paragraph</p></div>',
    )

def test_unordered_list(self):
    md = """
- Item 1
- Item 2
- Item 3
"""
    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        '<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>',
    )
    
def test_ordered_list(self):
    md = """
1. Item 1
2. Item 2
3. Item 3
"""
    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        '<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>',
    )
    
def test_quote_block(self):
    md = """
> This is a quote
> This is another line of the quote
"""
    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        '<div><blockquote>This is a quote\nThis is another line of the quote</blockquote></div>',
    )
def test_invalid_markdown(self):
    md = """
This is an invalid markdown
"""
    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        '<div><p>This is an invalid markdown</p></div>',
    )
    
def test_extract_title_from_markdown(self):
    md = """
# This is a title
This is a paragraph
"""
    title = extract_title_from_markdown(md)
    self.assertEqual(title, "This is a title")
    
def test_extract_title_from_markdown_no_title(self):
    md = """
This is a paragraph
"""
    title = extract_title_from_markdown(md)
    self.assertEqual(title, None)

def test_extract_title_from_markdown_empty_string(self):
    md = ""
    title = extract_title_from_markdown(md)
    self.assertEqual(title, None)
    
def test_extract_title_from_markdown_no_paragraph(self):
    md = """
# This is a title
"""
    title = extract_title_from_markdown(md)
    self.assertEqual(title, "This is a title")


if __name__ == "__main__":
    unittest.main()