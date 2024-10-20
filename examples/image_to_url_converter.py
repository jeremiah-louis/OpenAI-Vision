import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
api_key = os.getenv("CLOUDINARY_API_KEY")
api_secret = os.getenv("CLOUDINARY_API_SECRET")


# Configuration
cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret,  # Click 'View API Keys' above to copy your API secret
    secure=True,
)


def upload_images_to_cloudinary():
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
    for image in Path("pdf_images").iterdir():
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
