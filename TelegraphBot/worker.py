from pyrogram import Client, filters
from TelegraphBot.telegraph import work_to_do
from pyrogram.types import Message
from TelegraphBot.database.chats_sql import Chats
from TelegraphBot.database import SESSION


@Client.on_message(filters.private & ~filters.text)
async def telegraph(_, message: Message):
    url, status = await work_to_do(message)
    if url:
        if status == "":
            await message.reply(url, quote=True)
        else:
            await status.edit(url)


@Client.on_message(filters.group & filters.command(["t", "telegraph", "tg"], prefixes=["/", "!"]))
async def telegraph_group(_, message: Message):
    user_id = message.from_user.id
    q = SESSION.query(Chats).get(message.chat.id)
    if q.allow_usage == "Admins Only":
        chat_user = await message.chat.get_member(user_id)
        if chat_user.status in ["creator", "administrator"]:
            allowed = True
        else:
            allowed = False
    else:
        allowed = True
    SESSION.close()
    if allowed:
        if not message.reply_to_message:
            await message.reply("Please Reply to a Media Message.")
            return
        elif message.reply_to_message.empty:
            await message.reply("Huh? Message has been Deleted I guess...")
            return
        elif message.reply_to_message.text:
            await message.reply("Can't upload text messages to telegraph")
            return
        url, status = await work_to_do(message.reply_to_message)
        if url:
            if status == "":
                await message.reply(url, quote=True)
            else:
                await status.edit(url)
