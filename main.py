import os
import requests
import json
from datetime import datetime
from pytz import timezone
from kaggle.api.kaggle_api_extended import KaggleApi

# Remove comment out on local
# import config

URL = os.environ['SLACK_WEBHOOK_URL']
COMPETITIONS_LIST = ['elo-merchant-category-recommendation', 'vsb-power-line-fault-detection']


def get_kernels_url(competition_name=None):
    api = KaggleApi()
    api.authenticate()
    kernels_list = api.kernels_list(competition=competition_name, sort_by='dateCreated')

    now = datetime.utcnow()
    kernels_url = ''

    for kernel_info in kernels_list:
        last_run_date = getattr(kernel_info, 'lastRunTime')
        last_run_date = timezone('UTC').localize(last_run_date)

        if last_run_date.date() == now.date():
            kernels_url += 'https://www.kaggle.com/{}\n'.format(getattr(kernel_info, 'ref'))

    return kernels_url


def post_slack(competition_name=None, kernels_url=None):
    payload = {
        'username': 'Kaggle Kernel Notification',
        'icon_url': 'https://pbs.twimg.com/profile_images/1146317507/twitter_400x400.png',
        'attachments': [{
                        'fallback': competition_name,
                        'color': '#D00000',
                        'fields': [{
                            'title': competition_name,
                            'value': message,
                                    }]
                        }]
    }
    requests.post(URL, data=json.dumps(payload))


def main():
    for competition_name in COMPETITIONS_LIST:
        kernels_url = get_kernels_url(competition_name=competition_name)
        post_slack(competition_name=competition_name, kernels_url=kernels_url)


main()
