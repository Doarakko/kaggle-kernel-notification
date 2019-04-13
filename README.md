# Kaggle Kernel Notification
[![CircleCI](https://circleci.com/gh/Doarakko/kaggle-kernel-notification.svg?style=svg)](https://circleci.com/gh/Doarakko/kaggle-kernel-notification)

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

Notify new posted kernel to Slack using Kaggle API and Heroku.

## Requirements
- Kaggle API
- Heroku
- Credit card
    - It does not take money, to sign up and deploy heroku
- [Slack](https://api.slack.com/incoming-webhooks) or [LINE](https://notify-bot.line.me)

## Usage
### 1. Press button(`Deplo to Heroku`) and enter environment variables
### 2. Set task on Heroku
Set `FREQUENCY` with `Daily`.

In the specification of the program, notify when the last execution date of Kernel is the same as the program execution date.

Therefore, it does not make sense to `Hourly` or `Every 10 minutes`.

## Contribution
Welcome issue and pull request.

For example, add other notification destination(Discord, Chatwork, etc).

## License
MIT

## Author
Doarakko