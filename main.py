import os
from datetime import datetime
import json
import requests
from pytz import timezone
from kaggle.api.kaggle_api_extended import KaggleApi

POST = os.environ['POST']
COMPETITIONS_LIST = os.environ['COMPETITIONS_LIST']

if POST == 'slack':
    SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
elif POST == 'line':
    LINE_NOTIFY_TOKEN = os.environ['LINE_NOTIFY_TOKEN']


def get_kernels_url(competition_name):
    api = KaggleApi()
    api.authenticate()
    kernels_list = api.kernels_list(
        competition=competition_name, sort_by='dateCreated')

    now = datetime.utcnow()
    kernels_url = ''

    for kernel_info in kernels_list:
        last_run_date = getattr(kernel_info, 'lastRunTime')
        last_run_date = timezone('UTC').localize(last_run_date)

        if last_run_date.date() == now.date():
            kernels_url += 'https://www.kaggle.com/{}\n'.format(
                getattr(kernel_info, 'ref'))

    return kernels_url


def post_slack(title, value):
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
    for competition_name in COMPETITIONS_LIST:
        kernels_url = get_kernels_url(competition_name=competition_name)

        if POST == 'slack':
            post_slack(title=competition_name, value=kernels_url)
        elif POST == 'line':
            # message = '\n{}\n{}'.format(competition_name, kernels_url)
            message = '\n{}'.format(kernels_url)
            post_line(message)


main()
