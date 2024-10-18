# import module
from pdf2image import convert_from_bytes
import logging
import os
import requests
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time

load_dotenv()
cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
api_key = os.getenv("CLOUDINARY_API_KEY")
api_secret = os.getenv("CLOUDINARY_API_SECRET")

# Logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    filename="image_converters.log",
    format="%(levelname)s:%(asctime)s:%(message)s",
)
# Configuration
cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret,
    secure=True,
)


class FileToImageConverters:

    def __init__(
        self,
        pdf_directory: str,
        pdf_image_storage_dir: str,
    ) -> None:
        self.pdf_directory = pdf_directory
        self.pdf_image_storage_dir = pdf_image_storage_dir

    def upload_static_file_to_cloudinary(self, file_name: str):
        """
        Uploads a single file stored in a temporary directory to cloudinary, and deletes the folder from the local machine after.
        Static files include pdfs
        """
        static_file_directory: str = os.path.join(self.pdf_directory, file_name)
        if os.path.exists(static_file_directory):
            try:
                resource_url = cloudinary.uploader.upload(
                    static_file_directory,
                    resource_type="raw",
                )
            except Exception as e:
                print(e)
            else:
                # os.remove(os.path.join(self.pdf_directory, file_name))
                return resource_url["url"]

    # Store Pdf with convert_from_path function
    def pdf_to_image(self, resource_url) -> None:
        """Converts pdf files into images"""
        # Download the pdf file
        response = requests.get(resource_url)
        # Get the content of the pdf as bytes
        pdf_bytes = response.content
        # Convert bytes to images
        images = convert_from_bytes(pdf_bytes)
        for i, image in enumerate(images):
            # Storage Path
            pdf_storage_path = os.path.join(
                self.pdf_image_storage_dir, f"page{str(i)}.jpg"
            )
            # Save pages as images
            image.save(pdf_storage_path, "JPEG")

    def url_to_image(self, url_img_path: str):
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(options=firefox_options)
        driver.maximize_window()
        driver.get("https://en.wikipedia.org/wiki/The_World%27s_Billionaires")
        time.sleep(3)
        driver.save_full_page_screenshot(url_img_path)
        driver.quit()

    def doc_to_image(self):
        pass

    def upload_images_to_cloudinary(self):
        """
        Uploads all `.jpg` images from the "pdf_images" directory to Cloudinary and returns their URLs.

        This function iterates through the "pdf_images" folder, selects all files with the `.jpg` extension,
        and uploads each image to Cloudinary using its filename (without the extension) as the `public_id`.
        The `public_id` ensures that each image has a unique identifier in Cloudinary, preventing overwriting
        of files. Each image is opened in binary mode (`"rb"`) to handle the file correctly during the upload.

        The function returns a list of secure URLs for the uploaded images.

        Returns:
            list: A list containing the secure URLs of the uploaded images.
        """
        urls = []
        for image in Path(self.pdf_image_storage_dir).iterdir():
            if image.suffix == ".jpg":
                with open(image, "rb") as img:
                    public_id = image.stem
                    # Upload multiple images from directory
                    upload_result = cloudinary.uploader.upload(
                        img,
                        public_id=public_id,
                    )
                    urls.append(upload_result["secure_url"])
        return urls

    def store_list_in_chroma_db(self, urls: list[str]) -> None:
        # Take the urls list from cloudinary and then store the urls in a chroma database with key value pair "id":[...list of urls]
        # After that we would then feed these urls to the openai vision models and the id would be what we would use to identify them
        #
        pass
