from flask import Flask, jsonify, request
from error import ValidationError, ServerError
import os
from dotenv import load_dotenv
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
        except ServerError as exp:
            code = 501
            message = str(exp)
        return jsonify({"status": "error", "message": message}), code
    error_wrapper.__name__ = func.__name__
    return error_wrapper

app = Flask(__name__)

@app.route('/date')
@error_decorator
def date_send():
    request_date = request.args.get('date')
    load_dotenv()
    try:
        datetime.datetime.strptime(request_date, '%d.%m.%Y')
    except: 
        raise ValidationError('Value not Date')
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ.get("RABBIT_HOST")))
        #connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    except:
        raise ServerError('Bad connection parameters')
    channel = connection.channel()
    channel.queue_declare(queue = 'date', durable = True)
    channel.basic_publish(exchange = '', routing_key = 'date', body = json.dumps(dict(date = request_date)))
    connection.close()
    body = dict(status = 'ok', message = 'Date send')
    return jsonify(body), 200
