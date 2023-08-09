import os
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Madara import pgram as app

REMOVEBG_API = os.environ.get("REMOVEBG_API", "tbWHBFNxFtKoZ3kaYbFaxuJG")
UNSCREEN_API = os.environ.get("UNSCREEN_API", "xaQwmKwkjjR48jANXiFhmGo9")

@app.on_message(filters.private & (filters.photo | filters.video | filters.document))
async def remove_background(bot, update):
    if not (REMOVEBG_API or UNSCREEN_API):
        await update.reply_text(
            text="Error: API not found",
            quote=True,
            disable_web_page_preview=True
        )
        return

    message = await update.reply_text(
        text="Processing...",
        quote=True,
        disable_web_page_preview=True
    )

    try:
        new_file_name = f"./{str(update.from_user.id)}"
        if (
            update.photo or (
                update.document and "image" in update.document.mime_type
            )
        ):
            new_file_name += ".png"
            file = await update.download()
            await message.edit_text(
                text="Photo downloaded successfully. Now removing background.",
                disable_web_page_preview=True
            )
            new_document = removebg_image(file)
        elif (
            update.video or (
                update.document and "video" in update.document.mime_type
            )
        ):
            new_file_name += ".webm"
            file = await update.download()
            await message.edit_text(
                text="Video downloaded successfully. Now removing background.",
                disable_web_page_preview=True
            )
            new_document = removebg_video(file)
        else:
            await message.edit_text(
                text="Media not supported",
                disable_web_page_preview=True
            )
            return

        try:
            os.remove(file)
        except:
            pass
    except Exception as error:
        await message.edit_text(
            text=str(error),
            disable_web_page_preview=True
        )
        return

    try:
        with open(new_file_name, "wb") as file:
            file.write(new_document)
        await update.reply_chat_action("upload_document")
    except Exception as error:
        await message.edit_text(
            text=str(error),
        )
        return

    try:
        await update.reply_document(
            document=new_file_name,
            quote=True
        )
        try:
            os.remove(new_file_name)
        except:
            pass
    except Exception as error:
        await message.edit_text(
            text=f"Error: {error}",
            disable_web_page_preview=True
        )


def removebg_image(file):
    response = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": open(file, "rb")},
        data={"size": "auto"},
        headers={"X-Api-Key": REMOVEBG_API}
    )
    response.raise_for_status()  # Check for API errors
    return response.content


def removebg_video(file):
    response = requests.post(
        "https://api.unscreen.com/v1.0/videos",
        files={"video_file": open(file, "rb")},
        headers={"X-Api-Key": UNSCREEN_API}
    )
    response.raise_for_status()  # Check for API errors
    return response.content

__help__= """
*Available commands:*

there is no command just send in bot pm image or video
"""

__mod_name__ = "RMBG"   
__command_list__ = [
    "rmbg",
      ]
