from textnode import *
import sys

#base_path = sys.argv[0]


def main():
    source_folder      = "static"
    destination_folder = "docs"
    content_path       = "content/"
    template_path      = "templates.html"

    # DER WICHTIGE TEIL:
    # setze basepath auf den GitHub-Pages-Pfad:
    repo_base = "/static_site_generator"

    copy_all_content(source_folder, destination_folder)
    generate_pages_recursive(content_path, template_path, destination_folder, repo_base)
    
if __name__ == "__main__":
    main()