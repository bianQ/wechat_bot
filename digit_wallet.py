"""
Author  : Alan
Date    : 2019/8/28 16:03
Email   : vagaab@foxmail.com
"""

from config import URL, HEADER, INTERVAL, CORN_TYPE, CORN_DICT, EN_TO_ZH_DICT, WARN_INTERVAL
from mail import Mail
from db import DBSession

import requests

import time
from threading import Thread


class Corn:

    def __init__(self, corn_type, current=0, buy=0, down=0, up=0, total_price=0, percent=0.05):
        self.corn_type = corn_type
        self.current = current
        self.buy = buy
        self.down = down
        self.up = up
        self.total_price = total_price
        self.percent = percent

    @property
    def is_notice(self):
        if self.buy:
            if abs(self.current - self.buy) / self.buy >= self.percent:
                return True
            return False
        if self.down == 0 or self.up == 0:
            return False
        if self.down and self.current <= self.down:
            return True
        if self.up and self.current >= self.up:
            return True
        return False

    @property
    def info(self):
        text = '\n'.join([f'{EN_TO_ZH_DICT[k]}：{v}' for k, v in self.__dict__.items() if v])
        if self.profit:
            text += f'\n收益：{self.profit}\n收益率：%.4f' % (self.profit / self.total_price)
        return text

    @property
    def profit(self):
        if self.buy == 0 or self.total_price == 0:
            return None
        corn_num = self.total_price / self.buy
        return round((self.current - self.buy) * corn_num, 2)

    @property
    def profit_percent(self):
        if self.buy == 0:
            return None
        return '%.2f' % ((self.current - self.buy) / self.buy * 100) + '%'

    def update(self, key, value):
        setattr(self, key, float(value))


class Wallet:

    def __init__(self, user_id):
        self.user_id = user_id
        self.db = DBSession()
        self.session = requests.session()
        self.corn_types = CORN_TYPE
        self.corns = {}
        # stop/active
        self.status = 'stop'
        self.warn_interval = WARN_INTERVAL
        self.warn_time = None
        self.mail = Mail()
        self.session.headers.update(HEADER)

        self.load()

    def refresh(self):
        response = self.session.get(URL)
        data = response.json()['data']
        msg = []
        for corn in self.corns.values():
            corn_data = [i for i in data if i['symbol'] == CORN_DICT.get(corn.corn_type)][0]
            corn.update('current', corn_data['close'])
            if corn.is_notice:
                msg.append(corn.info)
        self.warning(msg)

    def warning(self, msg):
        if msg:
            now = int(time.time())
            warn_time = self.warn_time
            if warn_time is not None and warn_time + self.warn_interval > now:
                return
            divide_line = '\n-----------------------------\n'
            text = divide_line.join(msg)
            self.warn_time = now
            self.mail.send(text)

    def auto_refresh(self):
        while True:
            self.refresh()
            if self.status == 'stop':
                break
            time.sleep(INTERVAL)

    def load(self):
        for corn_type in self.corn_types:
            corn_info = self.db.query(self.user_id, corn_type)
            self.corns[corn_type] = Corn(**corn_info)
        self.active()

    def active(self):
        t = Thread(target=self.auto_refresh)
        t.start()
        self.status = 'active'

    def stop(self):
        self.status = 'stop'

    @property
    def is_alive(self):
        if self.status == 'active':
            return True
        return False

    @property
    def profit(self):
        return sum([corn.profit for corn in self.corns])

    @property
    def info(self):
        divide_line = '\n-----------------------------\n'
        return divide_line.join([m.info for m in self.corns.values()])
