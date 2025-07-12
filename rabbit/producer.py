import pika
import json
from config.api_config import settings

class Producer:
    def __init__(self, queue_name):
        self.queue_name = queue_name

    def send(self, message: dict):
        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASS)
        parameters = pika.ConnectionParameters(host=settings.RABBITMQ_HOST, credentials=credentials)
        connection = pika.BlockingConnection(parameters)

        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name, durable=True)

        channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )

        print(f"Message sent to {self.queue_name}: {message}")
        connection.close()