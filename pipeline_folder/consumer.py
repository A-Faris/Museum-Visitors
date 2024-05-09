import logging
import json
import argparse
from confluent_kafka import Consumer
from os import environ
from dotenv import load_dotenv
from pipeline import log_to_file, import_to_database
from datetime import datetime, time, UTC

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
        ('at', time, TIME_RANGE),
        ('site', int, SITE_VALUES),
        ('val', int, VAL_VALUES),
        ('type', int, TYPE_VALUES),
    ]

    for key, type_, values in checks:
        dict_value = kiosk.get(key)
        print(dict_value)
        match key:
            case "at":
                try:
                    date = datetime.fromisoformat(dict_value)
                except Exception:
                    return "Key at could not be converted to datetime"

                if date > datetime.now(UTC):
                    return "Key at is set in the future"

                dict_value = date.time().replace(microsecond=0)

            case "site":
                if dict_value:
                    if not dict_value.isdigit():
                        return "Invalid Value For Key site"
                    dict_value = int(dict_value)

            case "type":
                if not kiosk["val"] == min(VAL_VALUES):
                    continue

        error = check_type(kiosk, key, type_, values, dict_value)
        if error:
            return error

    return ""


def consume_messages(consumer: Consumer):
    print("Checking")
    msg = consumer.poll(20)
    if msg is None:
        print("Waiting...")
    elif msg.error():
        logging.info(msg.error())
        print(msg.error())
    else:
        return json.loads(msg.value().decode())


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
        kiosk_data = consume_messages(consumer)
        if not kiosk_data:
            continue

        error = check_error(kiosk_data)
        if error:
            if log:
                logging.error(msg=(kiosk_data, error))
                print(kiosk_data, error)
            print("Waiting...")
        else:
            print(kiosk_data)
            import_to_database(kiosk_data)
