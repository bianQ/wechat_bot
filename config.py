"""
Author  : Alan
Date    : 2019/8/28 15:57
Email   : vagaab@foxmail.com
"""
import os

# wechat
APPID = os.environ('appid')
SECRET = os.environ('secret')
TOKEN = os.environ('token')

# corns
CORN_TYPE = ['BTC', 'ETH']
# BITCORN_BUY = 0
# BITCORN_DOWN = 9500
# BITCORN_UP = 10500

# request
HEADER = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}
URL = 'https://www.huobi.co/-/x/pro/market/overview5'
INTERVAL = 3

# email
FROM_ADDRESS = '15989490620@163.com'
TO_ADDRESS = 'vagaab@foxmail.com'
PASSWORD = os.environ('password')
SMTP = 'smtp.163.com'
PORT = 25

# menu
INFO = '请输入要执行的操作(如：查询)：'
MENU = {
    '查询': '',
    '我的设置': '',
    '更新设置': {**{k: ['价格上限', '价格下限', '买入单价', '买入总价', '提醒百分比', '重置'] for k in CORN_TYPE}, '重置': ''},
}
MENU_REFRESH_INTERVAL = 60
OPERATE_DICT = {
    'BTC': 'btcusdt',
    'ETH': 'ethusdt',
    '价格上限': 'up',
    '价格下限': 'down',
    '买入单价': 'buy',
    '买入总价': 'total_price',
    '提醒百分比': 'percent'
}
