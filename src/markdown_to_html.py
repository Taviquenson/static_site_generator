from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from markdown_blocks import *
from textnode import text_node_to_html_node, TextNode, TextType

''' converts a full markdown document into a single parent HTMLNode'''
def markdown_to_html_node(markdown):
    html_blocks = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)      
        match block_type:
            case BlockType.PARAGRAPH:
                htmlnodes = text_to_children(block.replace("\n", " "))
                # print(f"\nhtmlnodes before appending to html_blocks:\n{htmlnodes}")
                html_blocks.append(ParentNode("p", htmlnodes))
            case BlockType.HEADING:
                count_hashes = block.count("#")
                htmlnodes = text_to_children(block.replace("#", "").strip())
                # obtain number of # character to get the tag right html tag
                html_blocks.append(ParentNode(f"h{count_hashes}", htmlnodes))
            case BlockType.CODE: # Special case
                # should not do any inline markdown parsing of its children
                lines = block.split("\n")
                filtered_lines = list(filter(lambda line: not ("```" in line), lines))
                # block_trimmed = block.replace("```", "")
                filtered_lines[-1] = filtered_lines[-1] + "\n"
                new_block = "\n".join(filtered_lines)
                htmlnode = TextNode(new_block, TextType.CODE)
                code_block_node = text_node_to_html_node(htmlnode)
                # goes 1st into a ParentNode tag 'code', 2nd into ParentNoce tag 'pre'
                html_blocks.append(ParentNode("pre", [code_block_node]))
            case BlockType.QUOTE:
                lines = block.split("\n")
                clean_lines = list(map(lambda line: line.replace(">", "").strip(), lines))
                one_line_quote = " ".join(clean_lines)
                htmlnodes = text_to_children(one_line_quote)
                html_blocks.append(ParentNode("blockquote", htmlnodes))
            case BlockType.ULIST:
                html_list_nodes = []
                for line in block.split("\n"):
                    htmlnodes = text_to_children(line.replace("- ", ""))
                    html_list_nodes.append(ParentNode("li", htmlnodes))
                html_blocks.append(ParentNode("ul", html_list_nodes))
            case BlockType.OLIST:
                html_list_nodes = []
                lines = block.split("\n")
                for i in range(0,len(lines)):
                    htmlnodes = text_to_children(lines[i].replace(f"{i+1}. ", ""))
                    html_list_nodes.append(ParentNode("li", htmlnodes))
                html_blocks.append(ParentNode("ol", html_list_nodes))
            case _:
                raise ValueError("invalid block type")
    # contains child HTMLNode objects representing the nested elements
    parent_HTMLNode = ParentNode("div", html_blocks)
    return parent_HTMLNode


''' takes a string of text (block) and returns a list of HTMLNodes '''
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes
