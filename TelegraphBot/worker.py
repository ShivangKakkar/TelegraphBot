from pyrogram import Client, filters
from TelegraphBot.telegraph import work_to_do
from pyrogram.types import Message


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
