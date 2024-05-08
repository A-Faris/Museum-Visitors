import logging
import json
import argparse
from confluent_kafka import Consumer
from os import environ
from dotenv import load_dotenv
from pipeline import log_to_file, import_to_database
from datetime import datetime, time

MAX_MESSAGES = 10000
SITE_VALUES = (0, 1, 2, 3, 4, 5)
VAL_VALUES = (-1, 0, 1, 2, 3, 4)
TYPE_VALUES = (0, 1)
REQUIRED_KEYS = {"at", "site", "val"}
TIME_RANGE = (time(8, 45), time(18, 15))


def check_type(check_dict: dict, key: str, type_: type, values: tuple, dict_value) -> str:
    """Checks if key exists and values are valid and of the correct type"""
    if check_dict.get(key) is None:
        return f"Missing Key: {key}"
    if not isinstance(dict_value, type_):
        return f"Invalid Type For Key {key}"
    if not min(values) <= dict_value <= max(values):
        return f"Invalid Value For Key {key}"
    return ""


def check_error(kiosk: dict) -> str:
    """Checks for errors and returns an appropriate error message"""
    checks = [
        ('site', int, SITE_VALUES),
        ('val', int, VAL_VALUES),
        ('type', int, TYPE_VALUES),
        # ('at', time, TIME_RANGE)
    ]

    for key, type_, values in checks:
        dict_value = kiosk.get(key)
        match key:
            case "site":
                if dict_value:
                    if not dict_value.isdigit():
                        return "Invalid Value For Key site"
                    dict_value = int(dict_value)

            case "type":
                if not dict_value == min(VAL_VALUES):
                    continue

            case "at":
                try:
                    date = datetime.fromisoformat(dict_value)
                    if date > datetime.now():
                        return "Invalid Value For Key at"
                    dict_value = date.time()
                except Exception:
                    return "Invalid Value For Key at"

        error = check_type(kiosk, key, type_, values, dict_value)
        if error:
            return error

    return ""


def consume_messages(consumer: Consumer, log: bool):
    print("Checking")
    msg = consumer.poll(20)
    if msg is None:
        return "Waiting..."
    elif msg.error():
        logging.info(msg.error())
        return msg.error()
    else:
        kiosk_data = json.loads(msg.value().decode())

        error = check_error(kiosk_data)
        if error:
            if log:
                logging.error(msg=(kiosk_data, error))
                return kiosk_data, error
            return "Waiting..."

        import_to_database(kiosk_data)
        return kiosk_data


def log_argument() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", "-l",
                        default=True,
                        help="Choose to log to a file or to the terminal. Default 'True'.",
                        type=bool)
    return parser.parse_args().log


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
    log = log_argument()

    consumer = Consumer(kafka_config)
    consumer.subscribe([environ["TOPIC"]])

    for _ in range(MAX_MESSAGES):
        print(consume_messages(consumer, log))
