from textnode import *


def main():
    # Example usage
    source_folder = "static"
    destination_folder = "public"
    destination_file_path = "public/index.html"
    
    content_path = "/Users/stephanzeibig/boot_dev_course/static_site_generator/content/index.md"
    template_path = "/Users/stephanzeibig/boot_dev_course/static_site_generator/templates.html"

    # Copy all content from source folder to destination folder
    copy_all_content(source_folder, destination_folder)
    
    generate_page(content_path, template_path, destination_file_path)
    
if __name__ == "__main__":
    main()