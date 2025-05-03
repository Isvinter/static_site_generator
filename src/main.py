import sys
import os
from textnode import *

def main():
    # --- basepath einlesen & normalisieren ---
    repo_base = sys.argv[1] if len(sys.argv) > 1 else ""
    repo_base = repo_base.strip("/")          # keine führenden/folgenden Slashes
    repo_base = f"/{repo_base}" if repo_base else ""
    print(f"▶️ main.py: Normalized repo_base = '{repo_base}'")

    source_folder      = "static"
    destination_folder = "docs"
    content_path       = "content/"
    template_path      = "templates.html"

    copy_all_content(source_folder, destination_folder)
    generate_pages_recursive(content_path, template_path, destination_folder, repo_base)

if __name__ == "__main__":
    main()
