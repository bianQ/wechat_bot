"""
Author  : Alan
Date    : 2019/8/30 11:24
Email   : vagaab@foxmail.com
"""
from config import MENU, MENU_REFRESH_INTERVAL, INFO, CORN_TYPE, OPERATE_DICT

import time
from threading import Thread


class Msg:

    def __init__(self, wallet):
        self.wallet = wallet
        self.menu = MENU
        self.corn_type = ''

    @property
    def now(self):
        return int(time.time())

    def format_msg(self, to_user, from_user, msg):
        text = f"""
        <xml>
        <ToUserName><![CDATA[{from_user}]]></ToUserName>
        <FromUserName><![CDATA[{to_user}]]></FromUserName>
        <CreateTime>{self.now}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{msg}]]></Content>
        </xml>
        """
        return text

    def reply_text(self, content):
        text_list = []
        divide_line = '\n-----------------------------\n'
        if content == '查询':
            pass
        if content == '我的设置':
            for corn in self.wallet.corns.values():
                text_list.append('\n'.join([f'{k}: {v}' for k, v in corn.__dict__.items() if v]))
        text = divide_line.join(text_list)
        return text

    def create_msg(self, to_user, from_user, content):
        if content not in self.menu:
            if not isinstance(self.menu, dict):
                if content.isdigit():
                    self.wallet.corns.get(self.corn_type).update(OPERATE_DICT[self.menu], int(content))
                    msg = f'{self.corn_type} {self.menu} 成功设置为 {content}'
                    self.menu = MENU
                else:
                    msg = f'输入格式错误，请重新输入'
                return self.format_msg(to_user, from_user, msg)
            msg = '\n'.join([INFO, *[f'{i+1}、{v}' for i, v in enumerate(self.menu)]])
        else:
            if content == '重置':
                self.menu = MENU
                msg = '\n'.join([INFO, *[f'{i+1}、{v}' for i, v in enumerate(self.menu)]])
                return self.format_msg(to_user, from_user, msg)
            if content in CORN_TYPE:
                self.corn_type = content
            if not isinstance(self.menu, dict):
                self.menu = content
                return self.format_msg(to_user, from_user, '请输入金额/百分比')
            sub_menu = self.menu.get(content)
            if sub_menu:
                t = Thread(target=self.refresh_menu)
                t.start()
                self.menu = sub_menu
                msg = '\n'.join([INFO, *[f'{i+1}、{v}' for i, v in enumerate(self.menu)]])
            else:
                msg = self.reply_text(content)
        return self.format_msg(to_user, from_user, msg)

    def refresh_menu(self):
        for _ in range(MENU_REFRESH_INTERVAL):
            if self.menu == MENU:
                break
            time.sleep(1)
        self.menu = MENU
