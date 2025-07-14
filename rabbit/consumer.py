import pika
import json
import logging
from config.api_config import settings

logger = logging.getLogger(__name__)

class Consumer:
    def __init__(self, queue_name, on_message):
        self.queue_name = queue_name
        self.on_message = on_message
        logger.info(f"Consumer initialized for queue: {queue_name}")

    def consume(self):
        try:
            credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASS)
            parameters = pika.ConnectionParameters(host=settings.RABBITMQ_HOST, credentials=credentials)
            connection = pika.BlockingConnection(parameters)

            channel = connection.channel()
            channel.queue_declare(queue=self.queue_name, durable=True)

            def callback(ch, method, properties, body):
                print(body)
                message = json.loads(body)
                self.on_message(message)
                ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_consume(queue=self.queue_name, on_message_callback=callback)
            logger.info(f"Waiting for messages in {self.queue_name}. To exit press CTRL+C")
            try:
                channel.start_consuming()
            except KeyboardInterrupt:
                logger.info("Stopping consumer...")
                channel.stop_consuming()
            finally:
                connection.close()
        except Exception as e:
            logger.exception(f"Failed to consume messages from queue '{self.queue_name}': {e}")
            raise