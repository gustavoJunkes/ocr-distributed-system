from flask import Flask, request, jsonify
from service.storage_service import upload_image
from service.rabbit_mq_service import send_message
from firebase_admin import credentials
import firebase_admin

app = Flask(__name__)

cred = credentials.Certificate('firebase.json') 
firebase_admin.initialize_app(cred, {'storageBucket': 'ocr-distributed-system.firebasestorage.app'}) 

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
MAX_SIZE_IN_MB = 3
MAX_SIZE = MAX_SIZE_IN_MB * 1024 * 1024

def hasCorrectExtension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload-photo', methods=['POST'])
def upload_photo():
    file = request.files['file']

    if not file:
        return jsonify({'error': 'Favor enviar o arquivo'}), 400
    
    if not hasCorrectExtension(file.filename):
        return jsonify({'error': f'Arquivo não é uma das extensões permitidas: {ALLOWED_EXTENSIONS}'}), 400

    if len(file.read()) > MAX_SIZE:
        return jsonify({'error': f'Tamanho ultrapassou o máximo de {MAX_SIZE_IN_MB} MB'}), 400

    file.seek(0)

    job_id, file_path = upload_image(file)
    send_message(file_path, job_id)

    return jsonify({'jobId': job_id}), 202

if __name__ == '__main__':
    app.run()