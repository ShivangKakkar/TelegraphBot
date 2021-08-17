from TelegraphBot.database.chats_sql import Chats
from TelegraphBot.database import SESSION
from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.new_chat_members & filters.service & filters.group, group=1)
async def chats_sql(bot: Client, msg: Message):
    info = await bot.get_me()
    new_members = msg.new_chat_members
    if info in new_members:
        q = SESSION.query(Chats).get(int(msg.chat.id))
        if not q:
            SESSION.add(Chats(msg.chat.id, msg.chat.username, "Everyone"))
            SESSION.commit()
        else:
            SESSION.close()
