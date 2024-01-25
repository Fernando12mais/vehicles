from imagekitio import ImageKit
import os

from dotenv import load_dotenv

load_dotenv()


imagekit = ImageKit(
    private_key=os.getenv("IMAGE_KIT_PRIVATE_KEY"),
    public_key=os.getenv("IMAGE_KIT_PUBLIC_KEY"),
    url_endpoint=os.getenv("IMAGE_KIT_URL_ENDPOINT"),
)
