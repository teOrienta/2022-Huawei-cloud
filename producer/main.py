from config import get_app_config
import logging, pika, json, time

logger = logging.getLogger(__name__)
config = get_app_config("../.env")

RABBIT_HOST = config["RABBIT_HOST"]
RABBIT_QUEUE = config["RABBIT_QUEUE"]

parameters = pika.ConnectionParameters(
    host=RABBIT_HOST,
)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=RABBIT_QUEUE)

with open("dados.csv", "r", encoding="utf-8") as file:
    next(file)
    index = 0
    for line in file:
        event = line.strip().split(";")
        event = {
            "case:concept:name": event[0], 
            "concept:name": event[1],
            "start_timestamp": event[2],
            "time:timestamp": event[3],
        }
        channel.basic_publish(exchange = '',
                              routing_key = RABBIT_QUEUE,
                              body = json.dumps(event))
        logger.info(f"{index} events sent")
        time.sleep(0.5)
        index += 1
