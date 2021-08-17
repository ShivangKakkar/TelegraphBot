from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from TelegraphBot.database.chats_sql import Chats
from TelegraphBot.database import SESSION
from pyrogram.errors import UserNotParticipant

tick = "✅"
cross = "❌"


@Client.on_message(~filters.edited & filters.incoming & filters.group & filters.command("settings"), group=-1)
async def settings(_, msg: Message):
    chat_id = msg.chat.id
    q = SESSION.query(Chats).get(chat_id)
    if not q:
        SESSION.add(Chats(chat_id, msg.chat.username, "Everyone"))
        SESSION.commit()
    else:
        SESSION.close()
    try:
        chat_user = await msg.chat.get_member(msg.from_user.id)
        if chat_user.status in ["creator", "administrator"]:
            allowed = True
        else:
            allowed = False
    except UserNotParticipant:
        allowed = False
    except AttributeError:
        if msg.sender_chat:  # Anonymous Admins
            allowed = True
        else:
            allowed = False
    if allowed:
        q = SESSION.query(Chats).get(chat_id)
        if q.allow_usage == "Everyone":
            option1 = f"Everyone {tick}"
            option2 = f"Admins Only {cross}"
        else:
            option1 = f"Everyone {cross}"
            option2 = f"Admins Only {tick}"
        SESSION.close()
        await msg.reply(
            "Choose, who can use this bot in your group!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"Allow Usage : {option1}", callback_data="everyone")],
                [InlineKeyboardButton(f"Allow Usage : {option2}", callback_data="admins_only")]
            ])
        )
