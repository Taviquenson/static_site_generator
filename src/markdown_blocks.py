from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = filter(lambda block: block != "", blocks)
    blocks = list(map(lambda block: block.strip(), filtered_blocks))
    return blocks # list of "block" strings


def block_to_block_type(block):
    if re.findall(r"^>.*", block) != []:
        is_quote = True
        lines = block.split("\n")
        for line in lines:
            if re.findall(r"^>.*", line) == []:
                is_quote = False
        if is_quote == True: # one or more lines did not begin with '>'
            return BlockType.QUOTE
    elif re.findall(r"^- .*", block) != []:
        is_u_list = True
        lines = block.split("\n")
        for line in lines:
            if re.findall(r"^- .*", line) == []:
                is_u_list = False
        if is_u_list == True: # one or more lines did not begin with '-'
            return BlockType.UNORDERED_LIST
    elif re.findall(r"^1. .*", block) != []:
        is_o_list = True
        lines = block.split("\n")
        for i in range (len(lines)):
            if re.findall(f"^{i+1}\. .*", lines[i]) == []:
                is_o_list = False
        if is_o_list == True: # one or more lines did not begin with '-'
            return BlockType.ORDERED_LIST
    
    # heading? match if block begins with 1-6 '#' characters and no more,
    # then has a space, then a non-whitespace character and then zero or 
    # more of any character after that
    elif re.findall(r"^#{1,6} .*", block) != []:
        return BlockType.HEADING
    
    # The [\s\S] set means include any:
    # \s: whitespace character (space,tab, newline, etc.)
    # \S: non-whitespace character
    elif re.findall(r"^\`\`\`[\s\S]*\`\`\`$", block) != []:
        return BlockType.CODE
    
    return BlockType.PARAGRAPH
