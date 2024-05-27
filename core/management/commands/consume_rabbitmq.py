from django.core.management.base import BaseCommand
from rabbitmq import rabbitmq_client


class Command(BaseCommand):
    help = "Starts a RabbitMQ consumer for handeling notifications."

    def handle(self, *args, **options):
        binding_key = args[0] if args else "email"
        email_queue_name = rabbitmq_client.declare_queue_and_bind(binding_key)
        if binding_key == "email":
            rabbitmq_client.consume_email(email_queue_name)
        else:
            print(f"Unknown binding key: {binding_key}")
            rabbitmq_client.close()
