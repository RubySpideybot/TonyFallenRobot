import os
import re
import random
from platform import python_version as kontol
from telethon import events, Button
from telegram import __version__ as telever
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from FallenRobot.events import register
from FallenRobot import telethn as tbot


PHOTO = [
    "https://telegra.ph/file/b3152325770183815ee56.jpg",
    "https://telegra.ph/file/2228c94b368d9e0b186ab.jpg",
]

@register(pattern=("/alive"))
async def awake(event):
  TEXT = f"**Hey baby,​ [{event.sender.first_name}](tg://user?id={event.sender.id}),\n\nI am ⲩⲟⲟⲛⲓⲉ​**\n━━━━━━━━━━━━━━━━━━━\n\n"
  TEXT += f"» **My Developer​ : [𓆩ᯓ𝙃𝙤𝙧𝙣𝙮↯𝙍𝙐𝘽𝙔𓆪 𓆩𔘓𓆪](https://t.me/Horny_RUBY)** \n\n"
  TEXT += f"» **Library Version :** `{telever}` \n\n"
  TEXT += f"» **Telethon Version :** `{tlhver}` \n\n"
  TEXT += f"» **Pyrogram Version :** `{pyrover}` \n━━━━━━━━━━━━━━━━━\n\n"
  BUTTON = [[Button.url("ʜᴇʟᴘ​", "https://t.me/Yoonie_rubybot?start=help"), Button.url("Oppa🫰🏻​", "https://t.me/Horny_RUBY")]]
  ran = random.choice(PHOTO)
  await tbot.send_file(event.chat_id, ran, caption=TEXT,  buttons=BUTTON)

## Alive mod
