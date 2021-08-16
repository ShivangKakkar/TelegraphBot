from sqlalchemy import Column, UnicodeText, String
from TelegraphBot.database import BASE, SESSION


class Chats(BASE):
    __tablename__ = "chats"
    __table_args__ = {'extend_existing': True}
    chat_id = Column(String, primary_key=True)
    username = Column(UnicodeText)

    def __init__(self, chat_id, username=None):
        self.chat_id = chat_id
        self.username = username

    def __repr__(self):
        return "<Chat {} ({})>".format(self.username, self.chat_id)


Chats.__table__.create(checkfirst=True)


def num_chats():
    try:
        return SESSION.query(Chats).count()
    finally:
        SESSION.close()
