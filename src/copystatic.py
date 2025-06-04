import os
import shutil

def copy_directory(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
        print(f"Created directory '{dest_dir}'")
    else:
        raise Exception("shutil.rmtree() failed to delete destination directory")

    if os.path.exists(src_dir):
        file_names = os.listdir(src_dir)
    else:
        raise ValueError("Invalid directory path")
    
    for file_name in file_names:
        new_path = os.path.join(src_dir, file_name)
        if os.path.isfile(new_path):
            # print(f"Copying file '{new_path}' into dir: {dest_dir}")
            shutil.copy(new_path, dest_dir)
        else: # was directory, so recurse
            next_dest_dir = os.path.join(dest_dir, file_name)
            # print(f"Recursing into dir: {new_path} and Copying to dir: {next_dest_dir}")
            copy_directory(new_path, next_dest_dir)
