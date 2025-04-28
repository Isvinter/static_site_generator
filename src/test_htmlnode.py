import unittest

from html_node import HtmlNode

class TestHtmlNode(unittest.TestCase):
    
    def test_eq(self):
        node = HtmlNode("This is a text node", "This is a text node", [], {"class": "text"})
        node2 = HtmlNode("This is a text node", "This is a text node", [], {"class": "text"})
        self.assertEqual(node, node2)
    
    def test_repr(self):
        node = HtmlNode("div", "This is a text node", [], {"class": "text"})
        expected_repr = "HtmlNode(tag=div, value=This is a text node, children=[], props={'class': 'text'})"
        self.assertEqual(repr(node), expected_repr)
        
    def test_eq_different_tag(self):
        node = HtmlNode("div", "This is a text node", [], {"class": "text"})    
        other_node = HtmlNode("span", "This is a text node", [], {"class": "text"})
        self.assertNotEqual(node, other_node)
    
    def test_eq_different_value(self):
        node = HtmlNode("div", "This is a text node", [], {"class": "text"})
        other_node = HtmlNode("div", "This is a different text node", [], {"class": "text"})
        self.assertNotEqual(node, other_node)
        
    def test_eq_different_children(self):
        node = HtmlNode("div", "This is a text node", ["child"], {"class": "text"})
        other_node = HtmlNode("div", "This is a text node", ["different_child"], {"class": "text"})
        self.assertNotEqual(node, other_node)
    
    