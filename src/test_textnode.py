import unittest

from textnode import TextNode, TextType


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
        

if __name__ == "__main__":
    unittest.main()