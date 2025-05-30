class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag # string - tag name (e.g. "p", "a", "h1", etc.)
        self.value = value # string - value of the tag (e.g. the text inside a paragraph)
        self.children =children # list of HTMLNode objects
        self.props = props # dict of the attributes of the tag
    
    '''
    An HTMLNode without a tag will just render as raw text
    An HTMLNode without a value will be assumed to have children
    An HTMLNode without children will be assumed to have a value
    An HTMLNode without props simply won't have any attributes
    '''

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
        # Child classes will override this method to render themselves as HTML.

    def props_to_html(self):
        if self.props is None:
            return ""
        result = ""
        for prop in self.props:
            result += f' {prop}="{self.props[prop]}"'
        return result
    
    ''' Print tag, value, children, and props '''
    def __repr__(self):
        # title = "HTMLNode representation:\n"
        # ptag = f'Tag:{self.tag}\n'
        # pvalue =f'Value:{self.value}\n'
        # pchildren = f'Children:{self.children}\n'
        # pprops = f'Properties:{self.props}\n'
        # return title + ptag + pvalue + pchildren + pprops
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        # Notes:
        # 'props=None' is important because a LeafNode should require only 2 parameters
        # Just write 'None' in the Children parameter of the parent constructor because
        # a LeadNode has no children. Could write 'children=None' but then you have to
        # write 'props=props' and make it all look less clear

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        
        # Used to have an extra 'if-tree' but removed it since now not having properties
        # in a node returns an empty string "", so now this line works cases, with and
        # without properties in the HTMLNode 
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag.")
        if self.children is None:
            raise ValueError("All parent nodes must have children.")

        concat_str = ''
        for child in self.children:
            concat_str += f'{child.to_html()}'
        return f'<{self.tag}>{concat_str}</{self.tag}>'
