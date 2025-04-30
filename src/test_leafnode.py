import unittest

from html_node import LeafNode

def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
def test_leaf_to_html_div(self):
    node1 = LeafNode("div", "Hello, world!")
    node2 = LeafNode("div", "Hello, world!")
    self.assertEqual(node1.to_html(), "<div>Hello, world!</div>")
    self.assertEqual(node1, node2)
    
def test_leaf_to_html_no_tag(self):
    node = LeafNode("Hello, world!")
    self.assertEqual(node.to_html(), "Hello, world!")
