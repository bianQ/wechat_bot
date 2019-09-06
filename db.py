"""
Author  : Alan
Date    : 2019/9/4 14:59
Email   : vagaab@foxmail.com
"""

from config import DATABASE
from models import Base, User

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def db_engine():
    engine = DATABASE.get('ENGINE')
    name = DATABASE.get('NAME')
    if engine == 'sqlite':
        return create_engine(f'{engine}:///{name}')
    else:
        host = DATABASE.get('HOST')
        user = DATABASE.get('USER')
        passwd = DATABASE.get('PASSWORD')
        charset = DATABASE.get('CHARSET') or 'utf8'
        return create_engine(f'{engine}://{user}:{passwd}@{host}/{name}', encoding=charset)


class DBSession:

    def __init__(self):
        engine = db_engine()
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)
        self.session = session()

    def query(self, user_id, corn_type):
        info = self.session.query(User).filter(User.user_id == user_id, User.corn_type == corn_type)
        if info.count() == 0:
            return {'corn_type': corn_type}
        return {k: v for k, v in info.one().__dict__.items() if k != '_sa_instance_state'}

    def update(self, user_id, corn_type, attr):
        try:
            self.session.query(User).filter(User.user_id == user_id, User.corn_type == corn_type).update(**attr)
            self.session.commit()
        except:
            self.session.rollback()
