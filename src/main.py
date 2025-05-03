from textnode import *
import sys


def main():

    repo_base = sys.argv[1] if len(sys.argv) > 1 else ""
    
    source_folder      = "static"
    destination_folder = "docs"
    content_path       = "content/"
    template_path      = "templates.html"

    copy_all_content(source_folder, destination_folder)

    # gib repo_base an die rekursive Funktion weiter!
    generate_pages_recursive(content_path, template_path, destination_folder, repo_base)
    
if __name__ == "__main__":
    main()