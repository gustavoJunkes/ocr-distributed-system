from PIL import Image
import pytesseract
import pika


connection_url = "amqps://jfibbsmk:n-A5itYWorE5ccBxztruhgfILRfzQ8oa@jaragua.lmq.cloudamqp.com/jfibbsmk"

connection = pika.BlockingConnection(pika.URLParameters(connection_url))
channel = connection.channel()

def callback(ch, method, properties, body):
    print(f"Mensagem recebida: {body.decode()}")  # aqui processa a mensagem da fila
    ch.basic_ack(delivery_tag=method.delivery_tag) # todo review

    body = body.decode().strip('"') 

    extracted_text = process_image(body.image) # todo: a imagem virá em link
    post_extracted_text(extracted_text)

def process_image(image_path):
    # return "Texto extraído da imagem"
    img = Image.open(image_path)

    text = pytesseract.image_to_string(img)

    return text

# image_path = r'C:\Users\Gustavo.Junkes\Documents\GitHub\ocr-distributed-system\ocr-service\image.png'
# text = process_image(image_path)
# print("Texto extraído da imagem:")
# print(text)

def post_extracted_text(text):
    channel.basic_publish(
        exchange='media.events',
        routing_key='store.request',
        body=text
    )

channel.basic_consume(queue='q.ocr.request', on_message_callback=callback)

print('Aguardando mensagens. Para sair, pressione CTRL+C')
channel.start_consuming()  
