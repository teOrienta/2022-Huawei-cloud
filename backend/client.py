import logging, pika, traceback, time
from config import get_app_config
   
def consume_events_queue(callback: callable):
    logger = logging.getLogger(__name__)
    config = get_app_config("../.env")

    RABBIT_HOST = config["RABBIT_HOST"]
    RABBIT_QUEUE = config["RABBIT_QUEUE"]
    
    while True:
        try:
            parameters = pika.ConnectionParameters(host=RABBIT_HOST)
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.basic_qos(prefetch_count=10, global_qos=False)

            channel.basic_consume(queue = RABBIT_QUEUE,
                        on_message_callback = callback)
            channel.start_consuming()
        except:
            error_message = traceback.format_exc()
            logger.error(f"Could not consume queue: {error_message}")
            time.sleep(10)
