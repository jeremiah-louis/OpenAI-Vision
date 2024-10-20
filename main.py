from urllib.parse import urlparse
from converters.image_converters import FileToImageConverters
import logging
from handlers.redis_db_handler import RedisHandler
from handlers.vision_handler import OpenAi_llm

# Logging Configurations
logging.basicConfig(
    level=logging.DEBUG,
    filename="main.log",
    format="%(levelname)s:%(asctime)s:%(message)s",
)


def get_image_converter_and_redis_handler():
    image_converter = FileToImageConverters(
        pdf_directory="pdfs",
        pdf_image_storage_dir="pdf_images",
    )
    redis_handler = RedisHandler()
    openai_llm = OpenAi_llm()
    return image_converter, redis_handler, openai_llm


def get_file_extension_type(static_file_url) -> str:
    """Gets a url and extracts the file extension type from it."""
    # Parse the URL into its components (scheme, netloc, path, etc.) to allow easier extraction of the file path.
    parsed_static_file_url = urlparse(static_file_url)
    # Extract the file path component from the parsed URL.
    file_path = parsed_static_file_url.path
    if "." in file_path:
        # Gets the file extension type e.g pdf,jpg,pptx e.t.c
        file_extension_type = file_path.split("/")[-1].split(".")[-1].lower()
        return file_extension_type
    else:
        # Case where url does not contain a file extension name e.g "https://github.com/user-attachments/assets/8dcd4b40-6988-45f0-9141-21451ab52102" (Here we can see that the url contains a unique id instead)
        file_extension_type = ""
        return file_extension_type


def handle_various_static_file_types(static_file_url) -> None:
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
    # Unpacks the image_converter, redis_handler, and openai_llm objects
    image_converter, redis_handler, openai_llm = get_image_converter_and_redis_handler()
    # Creates a url from the resource uploaded
    resource_url = image_converter.upload_static_file_to_cloudinary("")
    # Generates a unique_id to be used as a key to identify image urls
    document_id = redis_handler.generate_unique_uuid(user_id="jerry")
    # Converts the pdf resource to images
    image_converter.pdf_to_image(resource_url=resource_url)
    # Uploads the images from loccal directory to cloudinary
    urls = image_converter.upload_images_to_cloudinary()
    # Stores the Cloudinary PDF-image URLs inside a redis db
    redis_handler.store_list_in_redis(urls=urls, document_id=document_id)
    # Retrieves the Cloudinary PDF-image URLs from the redis db
    vision_urls = redis_handler.retrieve_list_from_redis(document_id=document_id)
    # Uploads the urls to the vision model
    openai_llm.parse_url_to_vision_model(urls=vision_urls)


def handle_presentations():
    pass


def handle_word_documents():
    pass
