import os
import requests
import json
from datetime import datetime
from pytz import timezone
from kaggle.api.kaggle_api_extended import KaggleApi

import config

URL = os.environ['SLACK_WEBHOOK_URL']
COMPETITIONS_LIST = ['elo-merchant-category-recommendation', 'vsb-power-line-fault-detection']


def get_kernels_url(competition_name=None):
    api = KaggleApi()
    api.CONFIG_NAME_USER = os.environ['KAGGLE_CONFIG_NAME_USER']
    api.CONFIG_NAME_KEY = os.environ['KAGGLE_CONFIG_NAME_KEY']
    # api.authenticate()
    kernels_list = api.kernels_list(competition=competition_name, sort_by='dateCreated')

    now = datetime.utcnow()
    message = '{}\n'.format(competition_name)

    for kernel_info in kernels_list:
        last_run_date = getattr(kernel_info, 'lastRunTime')
        last_run_date = timezone('UTC').localize(last_run_date)

        if last_run_date.date() == now.date():
            message += 'https://www.kaggle.com/{}\n'.format(getattr(kernel_info, 'ref'))

    return message


def post_slack(message='hoge'):
    payload = {
        'username': 'Kaggle Kernel Notification',
        'icon_url': 'https://pbs.twimg.com/profile_images/1146317507/twitter_400x400.png',
        'text': message,
    }
    requests.post(URL, data=json.dumps(payload))


def main():
    for copetition_name in COMPETITIONS_LIST:
        message = get_kernels_url(copetition_name)
        post_slack(message=message)

main()
