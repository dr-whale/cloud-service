from src.yandex import Client, ClientError, InvalidMethodError, BadConfigError, InvalidArgumentError
from src.lib import CacheManager, Log
from config import config
from datetime import datetime
import pika, json

def error_decorator(func):
    def test_wrapper(arg):
        code = 500
        message = 'Error'
        try:
            return func(arg)
        except InvalidArgumentError as exp:
            code = 404
            message = str(exp)
            Log().error('InvalidArgumentError',exc_info=True)
        except BadConfigError as exp:
            code = 403
            message = str(exp)
            Log().error('BadConfigError',exc_info=True)
        except InvalidMethodError as exp:
            code = 412
            message = str(exp)
            Log().error('InvalidMethodError',exc_info=True)
        except ClientError as exp:
            code = 400
            message = str(exp)
            Log().error('ClientError',exc_info=True)
        except Exception as exp:
            code = 500
            message = str(exp)
            Log().error('General Exception',exc_info=True)
        #return json.dumps({"status": "error", "message": message, "code": code})
        print(message)
    test_wrapper.__name__ = func.__name__
    return test_wrapper

weather_client = None

def client_create():
    global weather_client
    if not weather_client:
        weather_client = Client(config.BASE_URL, config.API_KEY)
    return weather_client

@error_decorator
def weather_send(date):
    weather = CacheManager().get(date)
    if not weather:
        #delta = datetime.strptime(date, "%d.%m.%Y").date() - datetime.today().date()
        #full_day = client_create().weather_req(yandex.DATA_URL, yandex.PARAMS)['forecasts'][delta.days]['parts']['day']
        simple_day = client_create().weather_req(config.DATA_URL, config.PARAMS)['forecast']['parts'][0]
        weather = json.dumps(dict(forecast_date = date, temperature = simple_day['temp_avg'], condition = simple_day['condition']))
        CacheManager().remember(date, weather)
    channel.queue_declare(queue = 'weather', durable = True)
    channel.basic_publish(exchange = '', routing_key = 'weather', body = weather)
    Log().info('Weather send to Rabbit')
    print('Weather send')


connection = pika.BlockingConnection(pika.ConnectionParameters(config.RABBIT_HOST))
Log().info("Connection to Rabbit Success")
channel = connection.channel()
channel.queue_declare(queue = 'date', durable = True)

def callback(ch, method, properties, body):
    print('Callback')
    weather_send(json.loads(body)['date'])

channel.basic_consume(queue = 'date', on_message_callback = callback, auto_ack = True)
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
