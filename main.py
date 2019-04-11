import os
from datetime import datetime
import json
import requests
from pytz import timezone
from kaggle.api.kaggle_api_extended import KaggleApi

POST = os.environ['POST']
COMPETITION_NAME = os.environ['COMPETITION_NAME']

if POST == 'slack':
    SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
elif POST == 'line':
    LINE_NOTIFY_TOKEN = os.environ['LINE_NOTIFY_TOKEN']


def get_kernels_url():
    api = KaggleApi()
    api.authenticate()
    kernels_list = api.kernels_list(
        competition=COMPETITION_NAME, sort_by='dateCreated')

    now = datetime.utcnow()
    kernels_url = ''

    for kernel_info in kernels_list:
        last_run_date = getattr(kernel_info, 'lastRunTime')
        last_run_date = timezone('UTC').localize(last_run_date)

        if last_run_date.date() == now.date():
            kernels_url += 'https://www.kaggle.com/{}\n'.format(
                getattr(kernel_info, 'ref'))

    return kernels_url


def post_slack(value, title=COMPETITION_NAME):
    payload = {
        'username': 'Kaggle Kernel Notification',
        'icon_url': 'https://avatars0.githubusercontent.com/u/1336944',
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
    except Exception as e:
        print(e)


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
    except Exception as e:
        print(e)


def main():
    kernels_url = get_kernels_url()

    if POST == 'slack':
        post_slack(value=kernels_url)
    elif POST == 'line':
        post_line(message=kernels_url)


main()
