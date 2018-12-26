# kaggle-kernel-notification
## Overview
Kaggle API と Heroku を使って、新規投稿された Kernel を Slack に投稿します。

## Requirement
- git
- Heroku CLI
- anaconda3-5.2.0
    - Python 3.6.5
        - kaggle 1.5.0
        - pytz 2018.4

- Kaggle API
- Slack
- Heroku Account
- Credit Card

## Usage
### 1. Slack の Webhook URL を取得
#### 1.1 サイドバー下の App 横にある「+」を押します。  
![app.png](https://qiita-image-store.s3.amazonaws.com/0/245792/4dfd7e35-b26e-b23d-fd68-52512cfc9fbf.png)

#### 1.2 Incomig Webhook をインストールして設定を追加
![スクリーンショット 2018-12-27 0.10.50.png](https://qiita-image-store.s3.amazonaws.com/0/245792/82e40eb1-0bf1-24b2-8cff-14172acb96c7.png)

以下からブラウザでの操作になります。
![スクリーンショット 2018-12-27 0.14.33.png](https://qiita-image-store.s3.amazonaws.com/0/245792/b4192dac-7f88-2c32-9baf-61f0608ec2e5.png)

#### 1.3 通知を送るチャンネルを選択（or 作成）
![スクリーンショット 2018-12-27 0.14.46.png](https://qiita-image-store.s3.amazonaws.com/0/245792/7e06c886-838a-f9cd-4501-0c016edd8eb9.png)

Webhook URL をメモっときます。
 ![スクリーンショット 2018-12-27 0.15.01.png](https://qiita-image-store.s3.amazonaws.com/0/245792/03dcbc59-3205-f533-7489-6012130bf389.png)

これで Slack での準備は完了です。

### 2. コードをダウンロード

```
$ git clone https://github.com/Doarakko/kaggle-kernel-notification
$ cd kaggle-kernel-notification
```
#### 2.1 通知するコンペを設定
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
通知したいコンペ名（`ref`カラムの値）を、以下のリストに入れます。
何個でも OK です。

```python:main.py
COMPETITIONS_LIST = ['elo-merchant-category-recommendation', 'vsb-power-line-fault-detection']
```

### 3. Heroku にデプロイ
```
$ heroku login
$ heroku create {適当なアプリ名}
$ git add --all
$ git commit -m 'Yeah!'
$ git push heroku master
```
### 4. Heroku の環境変数を設定
`$ heroku create {適当なアプリ名}`で作ったアプリが作成されています。
![スクリーンショット 2018-12-27 0.31.32.png](https://qiita-image-store.s3.amazonaws.com/0/245792/176658c3-9912-2826-061b-983b2ff00243.png)
作ったアプリをクリックして、「Settings」を開きます。
「Config Vars」に以下の環境変数を設定してください。

```
KAGGLE_USERNAME: kaggle.json の username
KAGGLE_KEY: kaggle.json の key
SLACK_WEBHOOK_URL: 1.3 で取得した Webhook URL です 
```
![スクリーンショット 2018-12-27 0.29.54.png](https://qiita-image-store.s3.amazonaws.com/0/245792/45ac77c0-bad4-78b1-f356-b2fb138c3fcc.png)

### 5. 試しに実行

```
$ heroku run python main.py
Running python main.py on ⬢ {適当なアプリ名}... up, run.7384 (Free)
```
1.3 で選択したチャンネルに投稿されていれば OK です。
![スクリーンショット 2018-12-27 0.42.13.png](https://qiita-image-store.s3.amazonaws.com/0/245792/6bcdb41b-1889-1ba8-fec0-501959b71b6d.png)

### 6. 定期実行させる
#### 6.1 Heroku のスケジューラーを入れる
おそらく、ここらへんで Heroku 上でクレジットカードを登録する必要があります。
結構前にやったので忘れました。

```
$ heroku addons:create scheduler:standard
```
Heroku 上で確認すると「Heroku Scheduler」がインストールされています。
![スクリーンショット 2018-12-27 0.54.28.png](https://qiita-image-store.s3.amazonaws.com/0/245792/6c0d6c9e-061b-7b12-30a3-299490b50d16.png)

#### 6.2 タスクを設定
![スクリーンショット 2018-12-27 0.54.45.png](https://qiita-image-store.s3.amazonaws.com/0/245792/ddd7e9d6-096d-2631-dd34-fda65a02fd92.png)

好きな時間（UTC）を設定します。
![スクリーンショット 2018-12-27 0.54.55.png](https://qiita-image-store.s3.amazonaws.com/0/245792/3fa14db0-0205-e6dc-5731-2625df7fa0f5.png)

「FREQUENCY」は `Daily` にしてください。
プログラムの仕様で、Kernel の最終実行日がプログラム実行日と同じ場合に通知するようにしています。
そのため、`Hourly` or `Every 10 minutes` にしても意味ないです。


## Hints
- [「Kaggle API」を Python で実行してみた](https://doarakko.hatenablog.com/entry/kaggle_api_in_python) 
- [作ったプログラム](https://github.com/Doarakko/kaggle-kernel-notification)
