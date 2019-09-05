"""
Author  : Alan
Date    : 2019/9/4 15:17
Email   : vagaab@foxmail.com
"""

from sqlalchemy import Column, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User:

    __tablename__ = 'user'
    user_id = Column(String(30), primary_key=True)
    corn_type = Column(String(10), primary_key=True)
    up = Column(Float(2), default=0)
    down = Column(Float(2), default=0)
    buy = Column(Float(2), default=0)
    total_price = Column(Float(2), default=0)
    percent = Column(Float(2), default=0.05)
