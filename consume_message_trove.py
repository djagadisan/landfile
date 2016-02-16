import logging
import pika
import pprint
import json

USERNAME = 'trove-melb'
PASSWORD = 'ETh7ahhieth6phee'
HOST = 'mq2-qh2'
VIRTUAL_HOST = 'trove'


def callback(ch, method, properties, body):
        pp = pprint.PrettyPrinter(indent=4)
        json_data = json.loads(body)
        try:
            # Try remove user_data if it exists
            json_data['payload']['args']['instance'].pop('user_data')
        except:
            pass
        pp.pprint(json_data)
        #pprint " [x] Received %r" % (body,)
        ch.basic_ack(delivery_tag=method.delivery_tag)


def createConnection():
        credentials = pika.PlainCredentials(USERNAME, PASSWORD)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                HOST,
                5672,
                VIRTUAL_HOST,
                credentials))
        return connection


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.CRITICAL)
channel = createConnection().channel()


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='notifications.info')
channel.start_consuming()
