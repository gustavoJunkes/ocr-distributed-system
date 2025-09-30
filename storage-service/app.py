import pika
from service.storage_service import upload_file
from service.file_service import create_file, remove_file
import json
from firebase_admin import credentials
import firebase_admin


connection_url = "amqps://jfibbsmk:n-A5itYWorE5ccBxztruhgfILRfzQ8oa@jaragua.lmq.cloudamqp.com/jfibbsmk"

cred = credentials.Certificate('firebase.json') 
firebase_admin.initialize_app(cred, {'storageBucket': 'ocr-distributed-system.firebasestorage.app'}) 

connection = pika.BlockingConnection(pika.URLParameters(connection_url))
channel = connection.channel()

def callback(ch, method, properties, body):
    print(f"Mensagem recebida: {body.decode()}") 
    print(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

    json_body = json.loads(body.decode())
            
    extracted_text = json_body['extracted_text']
    job_id = json_body['job_id']

    execute(extracted_text, job_id)

def execute(text, job_id):
    file_name = create_file(job_id, text)
    with open(file_name, 'rb') as file:
        upload_file(file) 

    remove_file(file_name)

    print("Arquivo salvo com sucesso")

if __name__ == '__main__':
    channel.basic_consume(queue='q.store.request', on_message_callback=callback)

    print('Aguardando mensagens. Para sair, pressione CTRL+C')
    channel.start_consuming()
