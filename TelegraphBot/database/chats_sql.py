from sqlalchemy import Column, UnicodeText, String, BigInteger
from TelegraphBot.database import BASE, SESSION


class Chats(BASE):
    __tablename__ = "chats"
    __table_args__ = {'extend_existing': True}
    chat_id = Column(BigInteger, primary_key=True)
    username = Column(UnicodeText)
    allow_usage = Column(String)

    def __init__(self, chat_id, username=None, allow_usage="Everyone"):
        self.chat_id = chat_id
        self.username = username
        self.allow_usage = allow_usage

    def __repr__(self):
        return "<Chat {} {} ({})>".format(self.username, self.allow_usage, self.chat_id)


Chats.__table__.create(checkfirst=True)


def num_chats():
    try:
        return SESSION.query(Chats).count()
    finally:
        SESSION.close()
