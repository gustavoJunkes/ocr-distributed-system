from firebase_admin import storage

DIRECTORY = 'transcripts/'

def upload_file(file):
    bucket = storage.bucket()

    print(f"Enviando arquivo: {file.name}")  

    file_path = DIRECTORY + file.name 

    blob = bucket.blob(file_path)
    
    blob.upload_from_file(file, content_type='text/plain')

    print(f"Arquivo {file.name} enviado com sucesso!")