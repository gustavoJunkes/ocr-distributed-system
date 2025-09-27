from firebase_admin import storage
import uuid

DIRECTORY = 'photos/'

def upload_image(file):
    bucket = storage.bucket()
    random_uuid = str(uuid.uuid4())
    file_extension = file.filename.rsplit('.', 1)[1].lower()

    file_path = DIRECTORY + random_uuid + '.' + file_extension

    blob = bucket.blob(file_path)
    
    blob.upload_from_file(file)

    return random_uuid, file_path