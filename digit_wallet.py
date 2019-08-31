"""
Author  : Alan
Date    : 2019/8/28 16:03
Email   : vagaab@foxmail.com
"""

from config import URL, HEADER, INTERVAL, CORN_TYPE, OPERATE_DICT

import requests

import time
from threading import Thread


class Corn:

    def __init__(self, corn_type):
        self.corn_type = corn_type
        self.current = 0
        self.buy = 0
        self.down = 0
        self.up = 0
        self.total_price = 0
        self.percent = 0.05

    @property
    def is_notice(self):
        if self.buy:
            if abs(self.current - self.buy) >= self.percent:
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
    def profit(self):
        if self.buy == 0:
            return None
        corn_num = self.total_price / self.buy
        return round((self.current - self.buy) * corn_num, 2)

    @property
    def profit_percent(self):
        if self.buy == 0:
            return None
        return '%.2f' % ((self.current - self.buy) / self.buy * 100) + '%'

    def update(self, key, value):
        setattr(self, key, value)


class Wallet:

    def __init__(self):
        self.session = requests.session()
        self.corn_types = CORN_TYPE
        self.corns = {}
        # stop/active
        self.status = 'stop'
        self.session.headers.update(HEADER)

    def refresh(self):
        response = self.session.get(URL)
        data = response.json()['data']
        for corn in self.corns.values():
            corn_data = [i for i in data if i['symbol'] == OPERATE_DICT.get(corn.corn_type)][0]
            corn.current = corn_data['close']

    def auto_refresh(self):
        while True:
            self.refresh()
            if self.status == 'stop':
                break
            time.sleep(INTERVAL)

    def load(self):
        self.corns = {corn_type: Corn(corn_type) for corn_type in self.corn_types}
        self.active()
        self.status = 'active'

    def active(self):
        t = Thread(target=self.auto_refresh)
        t.start()

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
