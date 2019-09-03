"""
Author  : Alan
Date    : 2019/8/28 15:57
Email   : vagaab@foxmail.com
"""
import os

# wechat
APPID = os.environ.get('appid')
SECRET = os.environ.get('secret')
TOKEN = os.environ.get('token')
HOST = os.environ.get('wechat_host')

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
WARN_INTERVAL = 60 * 10
FROM_ADDRESS = '15989490620@163.com'
TO_ADDRESS = 'vagaab@foxmail.com'
PASSWORD = os.environ.get('password')
SMTP = 'smtp.163.com'
PORT = 465

# menu
CORN_DICT = {
    'BTC': 'btcusdt',
    'ETH': 'ethusdt',
}
OPERATE_DICT = {
    '价格上限': 'up',
    '价格下限': 'down',
    '买入单价': 'buy',
    '当前价格': 'current',
    '买入总价': 'total_price',
    '提醒百分比': 'percent'
}
EN_TO_ZH_DICT = {
    'corn_type': '币种',
    **{v: k for k, v in OPERATE_DICT.items() if k not in ['BTC', 'ETH']},
    'profit': '收益'
}
ERROR = '输入错误！'
INFO = '请输入要执行的操作(如：查询)：'
MENU = {
    '查询': '',
    '设置': {k: list(OPERATE_DICT.keys()) for k in CORN_TYPE},
}
MENU_REFRESH_INTERVAL = 60
