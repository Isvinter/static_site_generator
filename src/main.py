from textnode import *
import sys

#base_path = sys.argv[0]


def main():
    content_path = "content/"
    template_path = "templates.html"
    destination = "docs"
    repo_base = "/static_site_generator"   # genau Dein Repo‑Name!

    copy_all_content("static", destination)
    generate_pages_recursive(content_path, template_path, destination, repo_base)
    
if __name__ == "__main__":
    main()