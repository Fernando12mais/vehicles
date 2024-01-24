from imagekitio import ImageKit
import os


imagekit = ImageKit(
    private_key=os.getenv("IMAGE_KIT_PRIVATE_KEY"),
    public_key=os.getenv("IMAGE_KIT_PUBLIC_KEY"),
    url_endpoint=os.getenv("IMAGE_KIT_URL_ENDPOINT"),
)


async def upload_file(file: str):
    result = imagekit.upload_file(
        file="https://imgs.search.brave.com/0LP8HX2aWKZ8-4WO9PaY9YQDn_06DkFsyHUSpMLhyVQ/rs:fit:500:0:0/g:ce/aHR0cHM6Ly9vbmxp/bmV0b29scy5jb20v/aW1hZ2VzL2V4YW1w/bGVzLW9ubGluZWlt/YWdldG9vbHMvb3ds/LW9uLXRyZWUtYnJh/bmNoLnBuZw",  # required
        file_name="my_file_name.jpg",  # required
    )

    return {"message": "file created", "file": file, "result": result.url}
