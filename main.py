from urllib.parse import urlparse
from image_converters import FileToImageConverters
import logging
import os

# Logging Configurations
logging.basicConfig(
    level=logging.DEBUG,
    filename="main.log",
    format="%(levelname)s:%(asctime)s:%(message)s",
)

# A function that accepts the data in form of "doc/docx", "pptx", "pdf", "websites".
# Uploads and stores the static assets on the cloud
# Uses the cloud storage version ("url") to feed the chat completions api
image_converter = FileToImageConverters(
    pptx_input_path="powerpoints",
    pptx_output_path="pptx_to_pdfs",
    pdf_directory="pdfs",
    pptx_image_storage_dir="pptx_images",
    pdf_image_storage_dir="pdf_images",
)
resource_url = image_converter.upload_static_file_to_cloudinary(
    file_name="Sample PPTX.pptx"
)


def get_file_extension_type(static_file_url) -> str:
    """Gets a url and extracts the file extension type from it."""
    # clean up url to expose the file name
    parsed_static_file_url = urlparse(static_file_url)
    file_path = parsed_static_file_url.path
    if "." in file_path:
        # Gets the file extension type e.g pdf,jpg,pptx e.t.c
        file_extension_type = file_path.split("/")[-1].split(".")[-1].lower()
        return file_extension_type
    else:
        # Case where url does not contain a file extension name e.g "https://github.com/user-attachments/assets/8dcd4b40-6988-45f0-9141-21451ab52102" (Here we can see that the url contains a unique id instead)
        file_extension_type = ""
        return file_extension_type


def handle_various_static_file_types(static_file_url: str) -> None:
    file_extension = get_file_extension_type(static_file_url)

    # Execute the various functions based on file extension
    if file_extension == "pdf":
        handle_pdfs()
    elif file_extension == "pptx":
        handle_presentations()
    elif file_extension == "docx":
        handle_word_documents()
    elif file_extension == "":
        "No file extension was found"
    else:
        f"unsupported file type {file_extension}"


def handle_pdfs():
    pass


def handle_presentations():
    pass
    # # Converts the pptx files to images
    # pptx_to_img = image_converter.pptx_to_image(pptx_filename="Sample PPTX.pptx")
    # # Stores the images in cloudinary
    # img_urls = image_converter.upload_images_to_cloudinary()
    # print(img_urls)


def handle_word_documents():
    pass


logging.debug(get_file_extension_type(static_file_url=resource_url))
