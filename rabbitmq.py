import json
import pika

from services.smtp_service import SmtpService


class RabbitMQClient:

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters("localhost")
        )
        self.channel = self.connection.channel()
        self.exchange_name = ""

    def _declare_queue(self):
        # By durable=True the queue will survive if the RabbitMQ server is restarted
        result = self.channel.queue_declare(queue="", durable=True)
        return result.method.queue

    def _publish(self, routing_key, message):
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=routing_key,
            body=json.dumps(message),
            # Makaing the message persistent tells RabbitMQ to save the message to disk
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
        )

    def _consume(self, queue_name, callback):

        def wrapper(ch, method, properties, body):
            callback(body)
            # send acknoledgement to RabbitMQ
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=50)
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=wrapper,
        )
        print(f" [*] Waiting for messages in {queue_name}. To exit press CTRL+C")
        self.channel.start_consuming()

    def close(self):
        if self.connection.is_open:
            self.channel.stop_consuming()
            self.connection.close()


class NotificationRabbitMQClient(RabbitMQClient):

    def __init__(self, exchange_name="notification_exchange", exchange_type="direct"):
        super().__init__()
        self.exchange_name = exchange_name
        self.channel.exchange_declare(
            exchange=exchange_name, exchange_type=exchange_type
        )

    def declare_queue_and_bind(self, binding_key):
        queue_name = self._declare_queue()
        self.channel.queue_bind(
            exchange=self.exchange_name, queue=queue_name, routing_key=binding_key
        )
        return queue_name

    def publish_email(self, message):
        self._publish("email", message)

    def consume_email(self, queue_name):
        def email_handler(message):
            decoded_message = message.decode("utf-8")
            data = json.loads(decoded_message)
            receivers = data.get("receivers", [])
            content = data.get("content", "")
            print(f" [x] Received {content} to send to {receivers}")
            smtp_service = SmtpService()
            smtp_service.send_email(
                subject="Notification",
                receivers=receivers,
                html_message=content,
                quit=True,
            )

        self._consume(queue_name, email_handler)


rabbitmq_client = NotificationRabbitMQClient()
