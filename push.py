import logging
import traceback
from flask import Flask, request

app = Flask(__name__)

import requests
import config

def notify(title, body, tag):
    # tag -> bark推送token
    app.logger.info("notify to bark")
    app.logger.debug(tag)
    payload = {
            "title":title,
            "body":body,
            "url":"rocketchat://room",
            "level":"timeSensitive",
            "isArchive":1,
            }
    if not config.tokens.get(tag, None):
        app.logger.debug("skip tag:", tag)
        return
    url = f"{config.host}/{config.tokens[tag]}/"
    resp = requests.post(url, json=payload)
    app.logger.debug(resp)


@app.route('/push/<string:service>/send', methods=['POST'])
def push_send(service):
    """
    Emulating a RocketChat push gateway like the official https://gateway.rocket.chat
    Returns the service name (could be anything) along with a HTTP 200 OK status

    :see: Notification factory https://github.com/RocketChat/Rocket.Chat/blob/ed092fbe490c21d64c071772ce1da66515837353/app/push-notifications/server/lib/PushNotification.js#L6
    :see: Payload extension https://github.com/raix/push/blob/234eeb12daa9b553d246c0a6edd3d06d550aa41b/lib/common/notifications.js#L67
    :see: API call https://github.com/RocketChat/Rocket.Chat/blob/88c8c8c0b0e57e2d5d66a19d71775bc0b10f424c/server/lib/cordova.js#L97
    :return: string
    """

    app.logger.info('New notification received')
    app.logger.debug(request.headers)
    app.logger.debug(request.json)

    try:
        token = request.json['token']
        title = request.json['options']['title']
        body = request.json['options']['text']

        notify(title=title, body=body, tag=token)

        app.logger.info('Forwarded the received notification, tag=%s', token)
    except:
        app.logger.error('Unexpected error during notification processing')
        app.logger.error(traceback.format_exc())
        app.logger.error('Could not forward the notification')
        app.logger.info(request.json)

    return service


if __name__ == '__main__':
    app.logger.setLevel(1)
    app.run(host='0.0.0.0')
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
