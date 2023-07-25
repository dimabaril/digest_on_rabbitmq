import os
import sys

import pika


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)
channel = connection.channel()
channel.queue_declare(queue="id")
channel.queue_declare(queue="digest")


def send_message():
    body = input("Enter user_id for digest: ")
    channel.basic_publish(exchange="", routing_key="id", body=body)
    print(f" [x] Sent user_id {body}")


def callback(ch, method, properties, body):
    print(" [x] Received digest %r" % body.decode())
    send_message()


def main():
    print(" [*] Working. To exit press CTRL+C")
    send_message()
    channel.basic_consume(
        queue="digest", on_message_callback=callback, auto_ack=True
    )
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
