import os
from markdown_blocks import markdown_to_html_node

''' pulls h1 header from Markdown file and returns it as a string '''
def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            no_hashtag_line = line.replace("#", "")
            return no_hashtag_line.strip()
    raise ValueError("Mardowns must have an h1 heading.")

'''  '''
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    md_file = open(from_path, "r")
    md_str = md_file.read()
    # print(md_str)
    html_template_file = open(template_path, "r")
    html_template_str = html_template_file.read()

    page_html_node = markdown_to_html_node(md_str)
    page_html_str = page_html_node.to_html()
    title_str = extract_title(md_str)

    # replace placeholders in template html
    html_final_str = html_template_str.replace("{{ Title }}", title_str).replace("{{ Content }}", page_html_str)
    # print(html_final_str)

    # get path before file name
    directory_path = os.path.dirname(dest_path)
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
        print(f"Created directory '{directory_path}'")

    if os.path.exists(directory_path):
        # html_final_path = os.path.join(dest_path, "index.html")
        with open(dest_path, 'w') as file: # file is closed after 'with' block
            file.write(html_final_str)
    else:
        raise Exception("No destination directory to copy the html file was found")

    md_file.close()
    html_template_file.close()