"""
Author  : Alan
Date    : 2019/8/30 11:24
Email   : vagaab@foxmail.com
"""
from config import MENU, MENU_REFRESH_INTERVAL, INFO, CORN_TYPE, OPERATE_DICT, ERROR

import time
from threading import Thread


class Directory:

    def __init__(self, name, previous=None):
        self.name = name
        self.previous = previous
        self.sub_dir = {}
        self.values = []

    def get_values(self):
        if self.name == 'root':
            return self.values
        else:
            return [*self.values, '上一页', '主页']


class Menu:

    def __init__(self, menu_dict):
        self.menu_dict = menu_dict
        self.root = None
        self.dir = None
        self.expires = None

        self.create_menu()

    def create_menu(self, sub_menu=None, previous=None):
        if sub_menu is None:
            self.root = Directory('root')
            self.create_menu(self.menu_dict, self.root)
        else:
            for key in sub_menu:
                current_dir = Directory(key, previous=previous)
                previous.sub_dir[key] = current_dir
                previous.values.append(key)
                if isinstance(sub_menu, dict) and sub_menu.get(key):
                    self.create_menu(sub_menu.get(key), current_dir)
        self.dir = self.root
        t = Thread(target=self.time_refresh)
        t.start()

    def reload(self):
        self.dir = self.root
        self.expires = None

    def change_dir(self, dir_name):
        self.expires = self.now + MENU_REFRESH_INTERVAL
        if dir_name not in self.dir.get_values():
            raise ValueError
        self.dir = self.dir.sub_dir.get(dir_name)

    @property
    def now(self):
        return int(time.time())

    def previous(self):
        self.expires = self.now + MENU_REFRESH_INTERVAL
        self.dir = self.dir.previous

    def time_refresh(self):
        while True:
            if self.expires is not None and self.now > self.expires:
                self.reload()
                time.sleep(2)


class Msg:

    def __init__(self, wallet):
        self.wallet = wallet
        self.menu = Menu(MENU)
        self.corn_type = ''
        self.corn_info = ''

    @property
    def now(self):
        return int(time.time())

    def format_dir_values(self, dir_values, header=INFO):
        return '\n'.join([header, *[f'{i+1}、{v}' for i, v in enumerate(dir_values)]])

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
        # 设置金额相关参数
        if self.menu.dir.values == list(OPERATE_DICT.keys()):
            if content in self.menu.dir.values:
                self.corn_info = content
                return '请输入金额/百分比'
            if content.isdigit():
                self.wallet.corns.get(self.corn_type).update(OPERATE_DICT[self.corn_info], content)
                self.menu.reload()
                return f'{self.corn_type} {self.corn_info} 成功设置为 {content}'
        # 设置参数错误时的返回信息
        if content not in self.menu.dir.get_values():
            return self.format_dir_values(self.menu.dir.get_values(), header=f'{ERROR}\n{INFO}')
        if content in CORN_TYPE:
            self.corn_type = content
        if content == '查询':
            return ''
        elif content == '我的设置':
            for corn in self.wallet.corns.values():
                text_list.append('\n'.join([f'{k}: {v}' for k, v in corn.__dict__.items() if v]))
            return divide_line.join(text_list)
        elif content == '主页':
            self.menu.reload()
        elif content == '上一页':
            self.menu.previous()
        else:
            self.menu.change_dir(content)
        return self.format_dir_values(self.menu.dir.get_values())

    def create_msg(self, to_user, from_user, content):
        return self.format_msg(to_user, from_user, self.reply_text(content))

    def refresh_menu(self):
        for _ in range(MENU_REFRESH_INTERVAL):
            if self.menu == MENU:
                break
            time.sleep(1)
        self.menu = MENU
