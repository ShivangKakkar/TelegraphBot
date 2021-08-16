from sqlalchemy import Column, Integer
from TelegraphBot.database import BASE, SESSION


class Users(BASE):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    user_id = Column(Integer, primary_key=True)

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return "<User ({})>".format(self.user_id)


Users.__table__.create(checkfirst=True)


def num_users():
    try:
        return SESSION.query(Users).count()
    finally:
        SESSION.close()
