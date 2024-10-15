# import module
from pdf2image import convert_from_path
import logging
import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from pathlib import Path

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
        pptx_input_path: str,
        pptx_output_path: str,
        pdf_directory: str,
        pdf_image_storage_dir: str,
        pptx_image_storage_dir: str,
    ) -> None:
        self.pptx_input_path = pptx_input_path
        self.pptx_output_path = pptx_output_path
        self.pdf_directory = pdf_directory
        self.pdf_image_storage_dir = pdf_image_storage_dir
        self.pptx_image_storage_dir = pptx_image_storage_dir

    def upload_static_file_to_cloudinary(self, file_name: str):
        """
        Uploads a single file stored in a temporary directory to cloudinary, and deletes the folder from the local machine after.
        Static files include pdfs,pptx,docx
        """
        static_file_directory: str = os.path.join(self.pptx_input_path, file_name)
        if os.path.exists(static_file_directory):
            try:
                resource_url = cloudinary.uploader.upload(
                    static_file_directory,
                    resource_type="raw",
                )
            except Exception as e:
                print(e)
            else:
                os.remove(os.path.join(self.pptx_input_path, file_name))
                return resource_url["url"]

    # Store Pdf with convert_from_path function
    def pdf_to_image(self, pdf_filename: str) -> None:
        """Converts pdf files into images"""
        pdf_file_path: str = os.path.join(self.pdf_directory, pdf_filename)
        images = convert_from_path(pdf_file_path)
        for i, image in enumerate(images):
            # Storage Path
            pdf_storage_path = os.path.join(
                self.pdf_image_storage_dir, f"page{str(i)}.jpg"
            )
            # Save pages as images in the pdf
            image.save(pdf_storage_path, "JPEG")

    # def pptx_to_image(self, pptx_filename: str) -> None:
    #     # First we convert the pptx to pdfs (Ideally these would be temporary paths since we are using s3)
    #     input_file_path = os.path.join(self.pptx_input_path, pptx_filename)
    #     convert(input_path=input_file_path, output_folder_path=self.pptx_output_path)
    #     # We convert the pdf to images
    #     images = convert_from_path(self.pptx_output_path)
    #     for i, image in enumerate(images):
    #         # Save pages as images in the pdf
    #         file_path = os.path.join(self.pptx_image_storage_dir, f"page{str(i+1)}.jpg")
    #         image.save(file_path, "JPEG")

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
