#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

for i in range(10000):
    channel.basic_publish(exchange='', routing_key='hello', body='hello world!')
print " [x] Sent 'hello world!'"
connection.close()
