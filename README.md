# kaggle-kernel-notification
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

Notify new posted kernel to Slack using Kaggle API and Heroku.

## Requirement
- Python 3.6.5
    - kaggle 1.5.0
    - pytz 2018.4

- Kaggle API
- Slack

## Usage
### 1. Get Slack Webhook URL

### 2. Download code

```
$ git clone https://github.com/Doarakko/kaggle-kernel-notification
$ cd kaggle-kernel-notification
```

#### 2.1 Get kaggle competitions name
```
$ kaggle competitions list
ref                                            deadline             category            reward  teamCount  userHasEntered
---------------------------------------------  -------------------  ---------------  ---------  ---------  --------------
digit-recognizer                               2030-01-01 00:00:00  Getting Started  Knowledge       2750           False
titanic                                        2030-01-01 00:00:00  Getting Started  Knowledge      10701            True
house-prices-advanced-regression-techniques    2030-01-01 00:00:00  Getting Started  Knowledge       4681           False
imagenet-object-localization-challenge         2029-12-31 07:00:00  Research         Knowledge         31           False
competitive-data-science-predict-future-sales  2019-12-31 23:59:00  Playground           Kudos       2014            True
histopathologic-cancer-detection               2019-03-30 23:59:00  Playground       Knowledge        291           False
vsb-power-line-fault-detection                 2019-03-21 23:59:00  Featured           $25,000        109           False
microsoft-malware-prediction                   2019-03-13 23:59:00  Research           $25,000        591            True
humpback-whale-identification                  2019-02-28 23:59:00  Featured           $25,000        825           False
elo-merchant-category-recommendation           2019-02-26 23:59:00  Featured           $50,000       1826           False
ga-customer-revenue-prediction                 2019-02-15 23:59:00  Featured           $45,000       1104            True
reducing-commercial-aviation-fatalities        2019-02-12 23:59:00  Playground            Swag         16           False
```

#### 2.2 Setting kaggle competitons name in `main.py`
```
COMPETITIONS_LIST = ['elo-merchant-category-recommendation', 'vsb-power-line-fault-detection']
```

### 3. Deploy to Heroku
```
$ heroku login
$ heroku create <app name>
$ git add --all
$ git commit -m 'Yeah!'
$ git push heroku master
```
### 4. Setting environment variable on Heroku

|Name|Note|
|:--|:--|
|KAGGLE_USERNAME||
|KAGGLE_KEY||
|SLACK_WEBHOOK_URL||

### 5. Run on local

```
$ heroku run python main.py
Running python main.py on ⬢ <app name>... up, run.7384 (Free)
```

### 6. Run every day
#### 6.1 Install Heroku scheduler
```
$ heroku addons:create scheduler:standard
```

#### 6.2 Setting task on Heroku
Set `FREQUENCY` with `Daily`.

In the specification of the program, notify when the last execution date of Kernel is the same as the program execution date.

Therefore, it does not make sense to `Hourly` or `Every 10 minutes`.
