from textnode import *
import sys

base_path = sys.argv[0]


def main():
    # Example usage
    source_folder = "static"
    destination_folder = "docs"
    
    content_path = "/Users/stephanzeibig/boot_dev_course/static_site_generator/content/"
    template_path = "/Users/stephanzeibig/boot_dev_course/static_site_generator/templates.html"

    # Copy all content from source folder to destination folder
    copy_all_content(source_folder, destination_folder)
    
    # Generate a single page
    generate_page(base_path, template_path, destination_folder)
    # Generate pages recursively
    generate_pages_recursive(base_path, template_path, destination_folder)
    
if __name__ == "__main__":
    main()