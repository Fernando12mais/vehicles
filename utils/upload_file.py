from libs.image_kit import imagekit


def upload_file(file: str):
    result = imagekit.upload_file(file, file_name="vehicle-picture")
    return result
