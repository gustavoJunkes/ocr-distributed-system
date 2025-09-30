from PIL import Image
import pytesseract
import pika
import json
import io
from firebase_admin import credentials, storage
import firebase_admin


cred = credentials.Certificate('firebase.json') 
firebase_admin.initialize_app(cred, {'storageBucket': 'ocr-distributed-system.firebasestorage.app'})

connection_url = "amqps://jfibbsmk:n-A5itYWorE5ccBxztruhgfILRfzQ8oa@jaragua.lmq.cloudamqp.com/jfibbsmk"

connection = pika.BlockingConnection(pika.URLParameters(connection_url))
channel = connection.channel()

def callback(ch, method, properties, body):
    print(f"Mensagem recebida: {body.decode()}") 
    ch.basic_ack(delivery_tag=method.delivery_tag)

    try:
        message_data = json.loads(body.decode())
        file_path = message_data['file_path']
        job_id = message_data['job_id']
        
        print(f"Processando job {job_id} com file_path: {file_path}")
        
        extracted_text = process_image_from_firebase(file_path)        
        post_extracted_text(extracted_text, job_id)
        
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

def process_image_from_firebase(file_path):
    try:
        bucket = storage.bucket()
        blob = bucket.blob(file_path)
        image_data = blob.download_as_bytes()
        img = Image.open(io.BytesIO(image_data))
        text = pytesseract.image_to_string(img)
        
        return text.strip()
        
    except Exception as e:
        print(f"Erro ao processar imagem do Firebase: {e}")
        return f"Erro ao processar imagem: {str(e)}"

def process_image(image_path):
    img = Image.open(image_path)

    text = pytesseract.image_to_string(img)

    return text


def post_extracted_text(text, job_id):
    result_message = {
        'extracted_text': text,
        'job_id': job_id
    }
    
    channel.basic_publish(
        exchange='media.events',
        routing_key='store.request',
        body=json.dumps(result_message)
    )
    
    print(f"Resultado publicado para job {job_id}: {text[:100]}...")

channel.basic_consume(queue='q.ocr.request', on_message_callback=callback)

print('Aguardando mensagens. Para sair, pressione CTRL+C')
channel.start_consuming()  
