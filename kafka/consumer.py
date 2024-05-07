from confluent_kafka import Consumer
from os import environ
from dotenv import load_dotenv


def consume_messages(consumer: Consumer) -> None:
    while True:
        print("hi")
        msg = consumer.poll(1)
        if msg is None:
            print("Waiting...")
        elif msg.error():
            raise KafkaException(msg.error())
        else:
            value = json.loads(msg.value().decode('utf-8'))
            machine_id = msg.key().decode('utf-8')
            print("Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
                topic=msg.topic(), key=machine_id, value=str(value)))
        if msg:
            print(msg.value().decode())


if __name__ == "__main__":

    load_dotenv()
    kafka_config = {
        'bootstrap.servers': environ["BOOTSTRAP_SERVERS"],
        'security.protocol': environ["SECURITY_PROTOCOL"],
        'sasl.mechanisms': environ["SASL_MECHANISM"],
        'sasl.username': environ["USERNAME"],
        'sasl.password': environ["PASSWORD"],
        'group.id': environ["GROUP"],
        'auto.offset.reset': environ["AUTO_OFFSET"]
    }

    consumer = Consumer(kafka_config)
    # consumer.subscribe([environ["TOPIC"]])
    consume_messages(consumer)
