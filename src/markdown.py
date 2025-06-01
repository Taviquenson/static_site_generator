import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # We only attempt to split "text" type objects (not bold, italic, code, etc)
        # This is because we don't care about nested inline elements
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            words = node.text.split(delimiter) # get list of words
            # The odd indexes of words are the ones enclosed by the delimiter because
            # even if first words have delimiter, split() returns "" at index 0
            
            # form the TextNodes
            for i in range(len(words)):
                # Edge case of no enclosing delimiter. Remember, if there is just one word
                # enclosed by delimiters, as in **bold**, split() will return the list
                # [ "", bold, ""]
                if len(words) % 2 == 0: #list is even, there was no closing delimiter
                    raise ValueError("Invalid Markdown, formatted section not closed")
                # Edge case of the delimited word being the first word or last word,
                # meaning split() created an empty string at the beginning or the end
                if words[i] == "":
                    continue
                # The odd indexes of words are the ones enclosed by the
                # delimiter because e.g. even if first word had delimiter,
                # split() returns "" at index 0
                if i % 2 == 0: # regular TextType
                    new_nodes.append(TextNode(words[i], TextType.TEXT))
                else: # special TextType
                    new_nodes.append(TextNode(words[i], text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in  old_nodes:
        # get the list of tuples that look like (alt_text, image)
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue

        original_text = node.text

        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1],))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in  old_nodes:
        # get the list of tuples that look like (alt_text, link)
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue

        original_text = node.text

        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    # returns matches for 2 groups along the string in a list of tuples
    # matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text) # first regex idea
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text) # more robust regex
    return matches # list of tuples [(alt_text, link), ...]

def extract_markdown_links(text):
    # returns matches for 2 groups along the string in a list of tuples
    # matches = re.findall(r"\[(.*?)\]\((.*?)\)", text) # first regex idea
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text) # more robust regex
    return matches # list of tuples [(link_text, link), ...]

# Regexes ([^\[\]]*) and ([^\(\)]*) are about including characters other than '[' and ']' in
# the first group and other than '(' and ')' in the second group
# e.g. anything inside brackets of [^] means "match any character that is not in the set"
#      Thus, in [^\[\]] both characters '[' and ']' won't get matched

# In regex (?<!!), means "negtive look behind applied to character '!' "
# Negative look behind specifies a group that can not match before the main expression
# (if it matches, the result is discarded)
# Basically, if there is a '!' before the rest of the matched pattern, the result is discarded