import os
import json
import datetime
import requests
from logging import StreamHandler, INFO, DEBUG, Formatter, FileHandler, getLogger

from kaggle.api.kaggle_api_extended import KaggleApi

POST = os.environ['POST']
COMPETITION_NAME = os.environ['COMPETITION_NAME']

if POST == 'slack':
    SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
elif POST == 'line':
    LINE_NOTIFY_TOKEN = os.environ['LINE_NOTIFY_TOKEN']

logger = getLogger(__name__)
log_fmt = Formatter(
    '%(asctime)s %(name)s %(lineno)d [%(levelname)s][%(funcName)s] %(message)s')
# info
handler = StreamHandler()
handler.setLevel(INFO)
handler.setFormatter(log_fmt)
logger.addHandler(handler)
logger.setLevel(INFO)
# debug
handler = StreamHandler()
handler.setLevel(DEBUG)
handler.setFormatter(log_fmt)
logger.addHandler(handler)
logger.setLevel(DEBUG)


def get_kernels_url():
    api = KaggleApi()
    api.authenticate()
    kernels_list = api.kernels_list(
        competition=COMPETITION_NAME, page_size=100, sort_by='dateCreated')

    now = datetime.datetime.utcnow()
    kernels_url = ''

    for kernel_info in kernels_list:
        last_run_date = getattr(kernel_info, 'lastRunTime')
        # assume to run once a day
        pre_date = now - datetime.timedelta(days=1)

        if last_run_date >= pre_date:
            kernels_url += 'https://www.kaggle.com/{}\n'.format(
                getattr(kernel_info, 'ref'))
    logger.debug('Get {} kernels'.format(len(kernels_list)))
    return kernels_url


def post_slack(value, title=COMPETITION_NAME):
    payload = {
        'username': 'Kaggle Kernel Notification',
        'icon_url': 'https://storage.googleapis.com/kaggle-avatars/images/2080166-kg.png',
        'attachments': [{
            'fallback': title,
            'color': '#D00000',
            'fields': [{
                'title': title,
                'value': value,
            }]
        }]
    }
    try:
        requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))
        logger.debug('Post Slack')
    except Exception as e:
        logger.error(e)


def post_line(message):
    # message = '\n{}\n{}'.format(COMPETITION_NAME, message)
    message = '\n{}'.format(message)

    headers = {
        'Authorization': 'Bearer ' + LINE_NOTIFY_TOKEN
    }
    payload = {
        'message': message
    }

    try:
        requests.post('https://notify-api.line.me/api/notify',
                      data=payload, headers=headers)
        logger.debug('Post LINE')
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    kernels_url = get_kernels_url()

    if POST == 'slack':
        post_slack(value=kernels_url)
    elif POST == 'line':
        post_line(message=kernels_url)
    else:
        logger.error('POST is invalid')
