from textnode import *
import os, shutil, sys

from copystatic import copy_directory
from gencontent import generate_pages_recursive


dir_path_static = "./static"
dir_path_docs = "./docs"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    if len(sys.argv) > 1:
        # print("Arguments:", sys.argv[1:])
        basepath = sys.argv[1]
    else:
        basepath = "/"

    print("Deleting public or docs directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    print("Copying static files to public directory...")
    copy_directory(dir_path_static, dir_path_docs)

    print("Generating website...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_docs, basepath)


if __name__ == "__main__":
    main()