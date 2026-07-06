import os
import shutil
import sys

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive


dir_path_static = "./static"
dir_path_docs = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
basepath = "/" if sys.argv[1] is None else sys.argv[1]


def main() -> None:
    print(basepath)
    print("Deleting public directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_docs, basepath)

    print("Generating page...")
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_docs,
        basepath
    )

main()