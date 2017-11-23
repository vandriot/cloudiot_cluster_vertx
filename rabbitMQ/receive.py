#!/usr/bin/env python
import pika
import time

credentials = pika.PlainCredentials('test', 'test')
parameters = pika.ConnectionParameters('192.168.1.40', 5672, '/', credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(0.5)
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=2)
channel.basic_consume(callback,
                      queue='task_queue')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

