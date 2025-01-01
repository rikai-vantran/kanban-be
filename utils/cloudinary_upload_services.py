from configs.cloudinary_config import cloudinary
from cloudinary import CloudinaryImage

def upload_file(image, public_id, asset_folder="Trello"):
    print("Uploading file to cloudinary")
    upload_result = cloudinary.uploader.upload(
        image, public_id=public_id, asset_folder=asset_folder)
    return upload_result["secure_url"]

def remove_file(public_id):
    try:
        cloudinary.uploader.destroy(public_id)
        return True
    except Exception as e:
        return False


def create_folder(folder_name):
    try:
        older_create_result = cloudinary.api.create_folder(folder_name)
        return True
    except Exception as e:
        return False
