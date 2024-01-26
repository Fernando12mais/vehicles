from libs.image_kit import imagekit


def upload_file(file: str):
    result = imagekit.upload_file(file, file_name="vehicle-picture")

    return result


def delete_file(file_id: str):
    result = imagekit.delete_file(file_id)
    return result


def upload_image(image):
    result = upload_file(image)
    return {"url": result.url, "file_id": result.file_id}
