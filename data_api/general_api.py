from flask import Flask, jsonify, request
from error import ValidationError, ServerError
from config import config
from log import Log
import json, pika, datetime

def error_decorator(func):
    def error_wrapper():
        code = 500
        message = 'Error'
        try:
            return func()
        except ValidationError as exp:
            code = 406
            message = str(exp)
            Log().error("DataValueError",exc_info=True)
        except ServerError as exp:
            code = 501
            message = str(exp)
            Log().error("ServerError",exc_info=True)
        return jsonify({"status": "error", "message": message}), code
    error_wrapper.__name__ = func.__name__
    return error_wrapper

app = Flask(__name__)

@app.route('/date')
@error_decorator
def date_send():
    request_date = request.args.get('date')
    try:
        datetime.datetime.strptime(request_date, '%d.%m.%Y')
        Log().info(f"Request argument is data: {request_date}")
    except: 
        raise ValidationError('Value not Date')
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(config.RABBIT_HOST))
        Log().info("Connection to Rabbit Success")
    except:
        raise ServerError('Bad connection parameters')
    channel = connection.channel()
    channel.queue_declare(queue = 'date', durable = True)
    channel.basic_publish(exchange = '', routing_key = 'date', body = json.dumps(dict(date = request_date)))
    connection.close()
    body = dict(status = 'ok', message = 'Data send')
    Log().info('Data send to queue')
    return jsonify(body), 200
