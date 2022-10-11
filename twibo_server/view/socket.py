from flask import request
from twibo_server import socketIO
from twibo_server.utils import logger


@socketIO.on('connect', namespace='/twibo')
def test_connect():
    logger.info('connected')


@socketIO.on_error('/twibo')
def error_handler_chat(e):
    event_name = request.event['message']
    logger.error(event_name)
