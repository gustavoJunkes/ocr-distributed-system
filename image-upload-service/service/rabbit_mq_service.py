import pika
import json

connection_url = "amqps://jfibbsmk:n-A5itYWorE5ccBxztruhgfILRfzQ8oa@jaragua.lmq.cloudamqp.com/jfibbsmk"

connection = pika.BlockingConnection(pika.URLParameters(connection_url))
channel = connection.channel()

def send_message(file_path, job_id):
    message = {'file_path': file_path, 'job_id': job_id}

    channel.basic_publish(
        exchange='media.events',
        routing_key='ocr.request',
        body=json.dumps(message)
    )

