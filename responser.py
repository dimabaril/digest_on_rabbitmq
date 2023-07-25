import json
import os
import sys

import pika

from services import generate_digest

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)
channel = connection.channel()
channel.queue_declare(queue="id")
channel.queue_declare(queue="digest")


def send_message(body):
    channel.basic_publish(exchange="", routing_key="digest", body=body)
    print(" [x] Sent digest %r" % body)


def callback(ch, method, properties, body):
    print(" [x] Received user_id %r" % body.decode())
    message = generate_digest(body.decode())
    message = json.dumps(message)
    send_message(message)


def main():
    channel.basic_consume(
        queue="id",
        on_message_callback=callback,
        auto_ack=True,
    )
    print(" [*] Working. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
