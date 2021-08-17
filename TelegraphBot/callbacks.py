from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from Data import Data
from TelegraphBot.database.chats_sql import Chats
from TelegraphBot.database import SESSION
from pyrogram.errors import UserNotParticipant

tick = "✅"
cross = "❌"


# Callbacks
@Client.on_callback_query()
async def _callbacks(bot: Client, callback_query: CallbackQuery):
    user = await bot.get_me()
    mention = user["mention"]
    if callback_query.data.lower() == "home":
        chat_id = callback_query.from_user.id
        message_id = callback_query.message.message_id
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=Data.START.format(callback_query.from_user.mention, mention),
            reply_markup=InlineKeyboardMarkup(Data.buttons),
        )
    elif callback_query.data.lower() == "about":
        chat_id = callback_query.from_user.id
        message_id = callback_query.message.message_id
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=Data.ABOUT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons),
        )
    elif callback_query.data.lower() == "help":
        chat_id = callback_query.from_user.id
        message_id = callback_query.message.message_id
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=Data.HELP,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons),
        )
    elif callback_query.data.lower() == "supported_media_types":
        chat_id = callback_query.from_user.id
        message_id = callback_query.message.message_id
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=Data.SUPPORTED_MEDIA_TYPES,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(Data.supported_media_buttons),
        )
    elif callback_query.data.lower() == "close":
        chat_id = callback_query.from_user.id
        message_ids = [callback_query.message.message_id, callback_query.message.reply_to_message.message_id]
        await bot.delete_messages(chat_id, message_ids)
    elif callback_query.data.lower() == "everyone":
        user_id = callback_query.from_user.id
        chat_id = callback_query.message.chat.id
        message_id = callback_query.message.message_id
        try:
            chat_user = await bot.get_chat_member(chat_id, user_id)
        except UserNotParticipant:
            return
        if chat_user.status in ["creator", "administrator"]:
            q = SESSION.query(Chats).get(chat_id)
            if q.allow_usage == "Everyone":
                await callback_query.answer("Already set to EVERYONE", show_alert=True)
                SESSION.close()
            else:
                q.allow_usage = "Everyone"
                SESSION.commit()
                await bot.edit_message_reply_markup(
                    chat_id=chat_id,
                    message_id=message_id,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(f"Allow Usage : Everyone {tick}", callback_data="everyone")],
                        [InlineKeyboardButton(f"Allow Usage : Admins Only {cross}", callback_data="admins_only")]
                    ]),
                )
        else:
            await callback_query.answer("Only admins can change settings.", show_alert=True)
    elif callback_query.data.lower() == "admins_only":
        user_id = callback_query.from_user.id
        chat_id = callback_query.message.chat.id
        message_id = callback_query.message.message_id
        try:
            chat_user = await bot.get_chat_member(chat_id, user_id)
        except UserNotParticipant:
            return
        if chat_user.status in ["creator", "administrator"]:
            q = SESSION.query(Chats).get(chat_id)
            if q.allow_usage == "Admins Only":
                await callback_query.answer("Already set to ADMINS ONLY", show_alert=True)
                SESSION.close()
            else:
                q.allow_usage = "Admins Only"
                SESSION.commit()
                await bot.edit_message_reply_markup(
                    chat_id=chat_id,
                    message_id=message_id,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(f"Allow Usage : Everyone {cross}", callback_data="everyone")],
                        [InlineKeyboardButton(f"Allow Usage : Admins Only {tick}", callback_data="admins_only")]
                    ]),
                )
        else:
            await callback_query.answer("Only admins can change settings.", show_alert=True)
