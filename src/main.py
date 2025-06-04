from textnode import *
import os, shutil

def main():
    # text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    # print(text_node)

    copy_directory("static", "public")


def copy_directory(src_dir, dest_dir):
    # 1. Delete all contents of destination directory
    try:
        # Attempt to remove the directory
        shutil.rmtree(dest_dir)
        print(f"Directory '{dest_dir}' successfully removed.")
    except FileNotFoundError:
        print(f"Directory '{dest_dir}' not found.")
    except PermissionError:
        print(f"Error: Permission denied to remove '{dest_dir}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    # 2. Copy all files and subdirectories, nested files, etc
    # 2.1 Log the path of each copied file
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
        print(f"Created directory '{dest_dir}'")
    else:
        raise Exception(f"shutil.rmtree() failed to delete destination directory")

    if os.path.exists(src_dir):
        file_names = os.listdir(src_dir)
    else:
        raise ValueError("Invalid directory path")
    
    # print(f"Found files {file_names} in dir: {src_dir}")

    for file_name in file_names:
        new_path = os.path.join(src_dir, file_name)
        if os.path.isfile(new_path):
            # print(f"Copying file '{new_path}' into dir: {dest_dir}")
            shutil.copy(new_path, dest_dir)
        else: # was directory, so recurse
            next_dest_dir = os.path.join(dest_dir, file_name)
            # print(f"Recursing into dir: {new_path} and Copying to dir: {next_dest_dir}")
            copy_directory(new_path, next_dest_dir)
            

if __name__ == "__main__":
    main()