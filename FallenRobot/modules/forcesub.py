import logging
import time

from pyrogram import filters
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    PeerIdInvalid,
    UsernameNotOccupied,
    UserNotParticipant,
)
from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup

from FallenRobot import DRAGONS as SUDO_USERS
from FallenRobot import pbot
from FallenRobot.modules.sql import forceSubscribe_sql as sql


logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(
    lambda _, __, query: query.data == "onUnMuteRequest"
)


@pbot.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, cb):
    user_id = cb.from_user.id
    chat_id = cb.message.chat.id
    chat_db = sql.fs_settings(chat_id)
    if chat_db:
        channel = chat_db.channel
        chat_member = client.get_chat_member(chat_id, user_id)
        if chat_member.restricted_by:
            if chat_member.restricted_by.id == (client.get_me()).id:
                try:
                    client.get_chat_member(channel, user_id)
                    client.unban_chat_member(chat_id, user_id)
                    cb.message.delete()
                    # if cb.message.reply_to_message.from_user.id == user_id:
                    # cb.message.delete()
                except UserNotParticipant:
                    client.answer_callback_query(
                        cb.id,
                        text=f"» Join @{channel} Channel & then press 'Unmute Me' button.",
                        show_alert=True,
                    )
            else:
                client.answer_callback_query(
                    cb.id,
                    text="» You are muted by Admins for another reason so i can't unmute yᴏu.",
                    show_alert=True,
                )
        else:
            if (
                not client.get_chat_member(chat_id, (client.get_me()).id).status
                == "administrator"
            ):
                client.send_message(
                    chat_id,
                    f"» **{cb.from_user.mention} is trying to unmute himself but i can't unmute him because i am not an Admin in this chat.**\n__#Leaving Chat...__",
                )

            else:
                client.answer_callback_query(
                    cb.id,
                    text="» WARNING! Don't press the unmute button when you can talk.",
                    show_alert=True,
                )


@pbot.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
    chat_id = message.chat.id
    chat_db = sql.fs_settings(chat_id)
    if chat_db:
        user_id = message.from_user.id
        if (
            not client.get_chat_member(chat_id, user_id).status
            in ("administrator", "creator")
            and not user_id in SUDO_USERS
        ):
            channel = chat_db.channel
            try:
                client.get_chat_member(channel, user_id)
            except UserNotParticipant:
                try:
                    sent_message = message.reply_text(
                        "Hey baby, {} 💔 \n **You haven't joined @{} channel yet**🧐 \n \nPlease Join [This Channel](https://t.me/{}) & then press the **UNMUTE ME** button. \n \n ".format(
                            message.from_user.mention, channel, channel
                        ),
                        disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "• CHANNEL •",
                                        url="https://t.me/{}".format(channel),
                                    )
                                ],
                                [
                                    InlineKeyboardButton(
                                        "• UNMUTE ME •", callback_data="onUnMuteRequest"
                                    )
                                ],
                            ]
                        ),
                    )
                    client.restrict_chat_member(
                        chat_id, user_id, ChatPermissions(can_send_messages=False)
                    )
                except ChatAdminRequired:
                    sent_message.edit(
                        "😕 I'm not an Admin here...\n__Give me permissions to ban users & then try again... \n#Ending FSub...__"
                    )

            except ChatAdminRequired:
                client.send_message(
                    chat_id,
                    text=f"😕 I'm not an Admin in @{channel} Channel.\n__Promote me as an Admin in the channel.\n#Ending FSub...__",
                )


@pbot.on_message(filters.command(["forcesubscribe", "fsub"]) & ~filters.private)
def config(client, message):
    user = client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status == "creator" or user.user.id in SUDO_USERS:
        chat_id = message.chat.id
        if len(message.command) > 1:
            input_str = message.command[1]
            input_str = input_str.replace("@", "")
            if input_str.lower() in ("off", "no", "disable"):
                sql.disapprove(chat_id)
                message.reply_text("» Succesfully disabled Force Subscribe.")
            elif input_str.lower() in ("clear"):
                sent_message = message.reply_text(
                    "» Unmuting all members muted by not joining the channel..."
                )
                try:
                    for chat_member in client.get_chat_members(
                        message.chat.id, filter="restricted"
                    ):
                        if chat_member.restricted_by.id == (client.get_me()).id:
                            client.unban_chat_member(chat_id, chat_member.user.id)
                            time.sleep(1)
                    sent_message.edit("» Unmuted all members who are muted by me for not joining the channel.")
                except ChatAdminRequired:
                    sent_message.edit(
                        "😕 I'm not an Admin in this chat.\n__I can't unmute members because i don't have permissions to mute/unmute users in this chat.__"
                    )
            else:
                try:
                    client.get_chat_member(input_str, "me")
                    sql.add_channel(chat_id, input_str)
                    message.reply_text(
                        f"» Force Subscribe enabled succesfully\n__Force Sub enabled, All the group members have to subsribe this [CHANNEL](https://t.me/{input_str}) for sending messages in this chat.__",
                        disable_web_page_preview=True,
                    )
                except UserNotParticipant:
                    message.reply_text(
                        f"😕 I'm not an Admin in the channel\n__Promote me as an Admin in the [CHANNEL](https://t.me/{input_str}) to enable Force Subscribe.__",
                        disable_web_page_preview=True,
                    )
                except (UsernameNotOccupied, PeerIdInvalid):
                    message.reply_text(f"» Invalid Channel username")
                except Exception as err:
                    message.reply_text(f"**ERROR:** ```{err}```")
        else:
            if sql.fs_settings(chat_id):
                message.reply_text(
                    f"» Force Subscribe is enabled.\n__For this [CHANNEL](https://t.me/{sql.fs_settings(chat_id).channel})__",
                    disable_web_page_preview=True,
                )
            else:
                message.reply_text("» Force Subscribe is disabled in in this chat.")
    else:
        message.reply_text(
            "» Only owner of this chat can enable Force Subscribe."
        )


__help__ = """
*Force Subscribe*:

*ⲩⲟⲟⲛⲓⲉ* can mute members who are not subscribed your channel until they subscribe When enabled I will mute unsubscribed members and show them a unmute button. When they pressed the button I will unmute them

*Setup*: *Only for chat owner*
‣ Add me in your group as admin
‣ Add me in your channel as admin 
    
*Commmands*:
‣ /fsub {channel username} : To turn on and setup the channel.

💡Do this first...

‣ /fsub : To get the current settings.
‣ /fsub disable : To turn of ForceSubscribe..

💡If you disable fsub, you need to set again for working.. /fsub {channel username} 

‣ /fsub clear : To unmute all members who are muted by me for not joining the channel.
"""
__mod_name__ = "Force-Sub"

