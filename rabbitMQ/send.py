#!/usr/bin/env python
import pika
import sys
import random 
import time
from random import uniform

credentials = pika.PlainCredentials('test', 'test')
parameters = pika.ConnectionParameters('192.168.1.40', 5672, '/', credentials)

count = 0
while True:
    count = count + 1
    temp = uniform(10.3, 20.5)
    currentDate = time.strftime("%x")
    currentTime = time.strftime("%X")
    message = '#' + str(count) + ' ' + str(temp) + ' ' + str(currentDate) + ' ' + str(currentTime)
    try:
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)
        channel.basic_publish(exchange='',
                            routing_key='task_queue',
                            body=message,
                            properties=pika.BasicProperties(
                                delivery_mode = 2, # make message persistent
                            ))
        print(" [x] Sent %r" % message)
    except pika.exceptions.ConnectionClosed:
        print 'Connection lost! Trying to reconnect...'

