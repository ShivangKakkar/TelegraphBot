import os
import requests
from PIL import Image
from pyrogram.types import Message

extensions = ["jpg", "jpeg", "png", "gif", "mp4"]
size_limit = 5242880
size_error = "Files with size more than 5 MB are not accepted."
status_text = "Converting and Uploading..."


async def work_to_do(message: Message):
    user_id = message.from_user.id
    message_id = message.message_id
    name_format = f"StarkBots_{user_id}_{message_id}"
    if message.document:
        extension = message.document.file_name[-3:]
        if extension not in extensions:
            await message.reply("This format is not supported by telegraph", quote=True)
            return
        elif message.document.file_size > size_limit:
            await message.reply(size_error, quote=True)
            return
        status = await message.reply(status_text, quote=True)
        file = await message.download(file_name=f"{name_format}.{extension}")
    elif message.sticker:
        if not message.sticker.is_animated:
            status = await message.reply(status_text, quote=True)
            sticker = await message.download(file_name=f"{name_format}.webp")
            img = Image.open(sticker).convert('RGB')
            img.save(f'downloads/{name_format}.jpg', 'jpeg')
            file = f'downloads/{name_format}.jpg'
            os.remove(sticker)
        else:
            await message.reply("Animated Stickers are not supported yet.", quote=True)
            return
    elif message.photo:
        if message.photo.file_size > size_limit:
            await message.reply(size_error, quote=True)
            return
        status = await message.reply(status_text, quote=True)
        file = await message.download(file_name=f"{name_format}.jpg")
    elif message.video:
        if message.video.file_size > size_limit:
            await message.reply(size_error, quote=True)
            return
        status = await message.reply(status_text, quote=True)
        file = await message.download(file_name=f"{name_format}.mp4")
    elif message.video_note:
        if message.video_note.file_size > size_limit:
            await message.reply(size_error, quote=True)
            return
        status = await message.reply(status_text, quote=True)
        file = await message.download(file_name=f"{name_format}.mp4")
    elif message.animation:
        if message.animation.file_size > size_limit:
            await message.reply(size_error, quote=True)
            return
        status = await message.reply(status_text, quote=True)
        file = await message.download(file_name=f"{name_format}.gif")
    else:
        await message.reply("This is not one of the supported types.", quote=True)
        return
    url = await upload(file)
    os.remove(file)
    return url, status


async def upload(file):
    files = {'files': open(file, 'rb')}
    r = requests.post("https://telegra.ph/upload", files=files)
    response = r.json()
    if isinstance(response, list):
        error = response[0].get('error')
    else:
        error = response.get('error')
    if error:
        url = error
    else:
        url = "https://telegra.ph" + response[0].get("src")
    return url
