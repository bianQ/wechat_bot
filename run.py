"""
Author  : Alan
Date    : 2019/8/28 10:39
Email   : vagaab@foxmail.com
"""
from config import APPID, SECRET, TOKEN, HOST
from digit_wallet import Wallet
from reply import Msg

from flask import Flask
from flask import request
import requests

import hashlib
import json
import time
from xml.etree import cElementTree as et


class Bot:

    def __init__(self):
        self.appid = APPID
        self.secret = SECRET
        self.access_token = ''
        self.token_expires = 0
        self.session = requests.session()

    def get_token(self):
        response = self.session.get(f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.appid}&secret={self.secret}')
        data = json.loads(response)
        self.access_token = data['access_token']
        self.token_expires = int(time.time()) + data['expires_in']

    @property
    def is_active(self):
        now = int(time.time())
        if now > self.token_expires:
            return True
        else:
            return False

    def send(self, msg):
        if not self.access_token or not self.is_active:
            self.get_token()
        pass


app = Flask(__name__)
app.debug = True
wallet = Wallet()
msg = Msg(wallet)


@app.route('/wx', methods=['GET', 'POST'])
def auth():

    if request.method == 'GET':
        token = TOKEN
        # 获取输入参数
        data = request.args
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        # 字典排序
        arg_list = [token, timestamp, nonce]
        arg_list.sort()
        s = ''.join(arg_list)
        # sha1加密算法
        hascode = hashlib.sha1(s.encode('utf-8')).hexdigest()
        # 如果是来自微信的请求，则回复 echostr
        if hascode == signature:
            return echostr
        else:
            return ""
    if request.method == 'POST':
        xml_data = request.data
        xml_rec = et.fromstring(xml_data)
        to_user = xml_rec.find('ToUserName').text
        from_user = xml_rec.find('FromUserName').text
        # msg_type = xml_rec.find('MsgType').text
        content = xml_rec.find('Content').text
        # msg_id = xml_rec.find('MsgId').text
        # reply_content = '这项目，我王多鱼投了'

        msg.wallet.load(from_user)
        reply_content = msg.create_msg(to_user, from_user, content)
        return reply_content


if __name__ == '__main__':
    app.run(host=HOST, port=80)
