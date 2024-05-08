import logging
import json
from confluent_kafka import Consumer
from os import environ
from dotenv import load_dotenv
from pipeline import log_to_file

MAX_MESSAGES = 10000
SITE_VALUES = ('0', '1', '2', '3', '4', '5')
VAL_VALUES = (-1, 0, 1, 2, 3, 4)
TYPE_VALUES = (0, 1)
REQUIRED_KEYS = {"at", "site", "val"}


def check_type(check_dict: dict, key: str, type_: type, values: tuple) -> str:
    """Checks if key exists and values are valid and of the correct type"""
    if not check_dict.get(key):
        return f"Missing Key: {key}"
    if not isinstance(check_dict[key], type_):
        return f"Invalid Type For Key {key}"
    if check_dict[key] not in values:
        return f"Invalid Value For Key {key}"
    return ""


def check_error(kiosk: dict) -> str:
    """Checks for errors and returns an appropriate error message"""
    checks = [
        ('site', str, SITE_VALUES),
        ('val', int, VAL_VALUES),
        ('type', int, TYPE_VALUES)
    ]

    for key, type_, values in checks:
        if key == "type":
            if not kiosk['val'] == min(VAL_VALUES):
                return ""

        error = check_type(kiosk, key, type_, values)
        if error:
            return error

    return ""

    # Can't accept times before and after certain times and in the future


def consume_messages(consumer: Consumer):
    print("Checking")
    msg = consumer.poll(20)
    if msg is None:
        return "Waiting..."
    elif msg.error():
        return msg.error()
    else:
        value = json.loads(msg.value().decode('utf-8'))

        error = check_error(value)
        if error:
            logging.error(msg=(value, error))
            return error, value

        logging.info(value)
        return value


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

    log_to_file("consumer")

    consumer = Consumer(kafka_config)
    consumer.subscribe([environ["TOPIC"]])

    for _ in range(MAX_MESSAGES):
        print(consume_messages(consumer))
