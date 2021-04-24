# (c) @AbirHasan2005

import os
import time
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid
from configs import Config

## --- Sub Configs --- ##
BOT_USERNAME = Config.BOT_USERNAME
BOT_TOKEN = Config.BOT_TOKEN
API_ID = Config.API_ID
API_HASH = Config.API_HASH
DB_CHANNEL = Config.DB_CHANNEL
ABOUT_BOT_TEXT = Config.ABOUT_BOT_TEXT
ABOUT_DEV_TEXT = Config.ABOUT_DEV_TEXT
HOME_TEXT = Config.HOME_TEXT
BOT_OWNER = Config.BOT_OWNER
broadcast_ids = {}
Bot = Client(BOT_USERNAME, bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)


@Bot.on_message(filters.command("start") & filters.private)
async def start(bot, cmd):
	usr_cmd = cmd.text.split("_")[-1]
	if usr_cmd == "/start":
		await cmd.reply_text(
			HOME_TEXT.format(cmd.from_user.first_name, cmd.from_user.id),
			parse_mode="Markdown",
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("Support Group", url="https://t.me/MoviesBazzz2"),
						InlineKeyboardButton("🔥MoviesBazzz🔥", url="https://t.me/joinchat/TP9IxftrpLQHA2NE")
					],
					[
						InlineKeyboardButton("About Bot", callback_data="aboutbot"),
						InlineKeyboardButton("About Dev", callback_data="aboutdevs")
					]
				]
			)
		)
	else:
		try:
			file_id = int(usr_cmd)
			send_stored_file = await bot.forward_messages(chat_id=cmd.from_user.id, from_chat_id=DB_CHANNEL, message_ids=file_id)
			#await send_stored_file.reply_text(f"**Here is Sharable Link of this file:** https://telegram.dog/{BOT_USERNAME}?start=MoviesBazzz_{file_id}\n\n__To Retrive the Stored File, just open the link!__", disable_web_page_preview=True, quote=True)
		except Exception as err:
			await cmd.reply_text(f"Something went wrong!\n\n**Error:** `{err}`")

@Bot.on_message(filters.media & ~filters.edited & filters.user(BOT_OWNER))
async def main(bot, message):
	if message.chat.type == "private":
		editable = await message.reply_text("Wait Boss...")
		try:
			forwarded_msg = await message.forward(DB_CHANNEL)
			file_er_id = forwarded_msg.message_id
			await forwarded_msg.reply_text(f"#PRIVATE_FILE:\n\n[{message.from_user.first_name}](tg://user?id={message.from_user.id}) Got File Link!", parse_mode="Markdown", disable_web_page_preview=True)
			share_link = f"https://telegram.dog/{BOT_USERNAME}?start=MoviesBazzz_{file_er_id}"
			await editable.edit(
				f"**Your File Stored in my Database!**\n\nHere is the Permanent Link of your file: {share_link} \n\nJust Click the link to get your file!",
				parse_mode="Markdown",
				reply_markup=InlineKeyboardMarkup(
					[[InlineKeyboardButton("Open Link", url=share_link)], [InlineKeyboardButton("🔥MoviesBazzz🔥", url="https://t.me/joinchat/TP9IxftrpLQHA2NE"), InlineKeyboardButton("Support Group", url="https://t.me/linux_repo")]]
				),
				disable_web_page_preview=True
			)
		except Exception as err:
			await editable.edit(f"Something Went Wrong!\n\n**Error:** `{err}`")
	elif message.chat.type == "channel":
		if message.chat.id == Config.LOG_CHANNEL:
			return
		forwarded_msg = None
		file_er_id = None
		if message.forward_from_chat:
			return
		elif message.forward_from:
			return
		else:
			pass
		if message.photo:
			return
		try:
			forwarded_msg = await message.forward(DB_CHANNEL)
			file_er_id = forwarded_msg.message_id
			share_link = f"https://telegram.dog/{BOT_USERNAME}?start=MoviesBazzz_{file_er_id}"
			CH_edit = await bot.edit_message_reply_markup(message.chat.id, message.message_id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Get Sharable Stored Link", url=share_link)]]))
			if message.chat.username:
				await forwarded_msg.reply_text(f"#CHANNEL_BUTTON:\n\n[{message.chat.title}](https://t.me/{message.chat.username}/{CH_edit.message_id}) Channel's Broadcasted File's Button Added!")
			else:
				private_ch = str(message.chat.id)[4:]
				await forwarded_msg.reply_text(f"#CHANNEL_BUTTON:\n\n[{message.chat.title}](https://t.me/c/{private_ch}/{CH_edit.message_id}) Channel's Broadcasted File's Button Added!")
		except Exception as err:
			print(f"Error: {err}")


@Bot.on_callback_query()
async def button(bot, cmd: CallbackQuery):
	cb_data = cmd.data
	if "aboutbot" in cb_data:
		await cmd.message.edit(
			ABOUT_BOT_TEXT,
			parse_mode="Markdown",
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("Go Home", callback_data="gotohome"),
						InlineKeyboardButton("About Dev", callback_data="aboutdevs")
					]
				]
			)
		)
	elif "aboutdevs" in cb_data:
		await cmd.message.edit(
			ABOUT_DEV_TEXT,
			parse_mode="Markdown",
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("About Bot", callback_data="aboutbot"),
						InlineKeyboardButton("Go Home", callback_data="gotohome")
					]
				]
			)
		)
	elif "gotohome" in cb_data:
		await cmd.message.edit(
			HOME_TEXT.format(cmd.message.chat.first_name, cmd.message.chat.id),
			parse_mode="Markdown",
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("Support Group", url="https://t.me/MoviesBazzz2"),
						InlineKeyboardButton("🔥MoviesBazzz🔥", url="https://t.me/joinchat/TP9IxftrpLQHA2NE")
					],
					[
						InlineKeyboardButton("About Bot", callback_data="aboutbot"),
						InlineKeyboardButton("About Dev", callback_data="aboutdevs")
					]
				]
			)
		)
	elif "refreshmeh" in cb_data:
		if not Config.UPDATES_CHANNEL == None:
			invite_link = await bot.export_chat_invite_link(Config.UPDATES_CHANNEL)
			try:
				user = await bot.get_chat_member(Config.UPDATES_CHANNEL, cmd.message.chat.id)
				if user.status == "kicked":
					await cmd.message.edit(
						text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/MoviesBazzz2).",
						parse_mode="markdown",
						disable_web_page_preview=True
					)
					return
			except UserNotParticipant:
				await cmd.message.edit(
					text="**You Still Didn't Join ☹️, Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!",
					reply_markup=InlineKeyboardMarkup(
						[
							[
								InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link)
							],
							[
								InlineKeyboardButton("🔄 Refresh 🔄", callback_data="refreshmeh")
							]
						]
					),
					parse_mode="markdown"
				)
				return
			except Exception:
				await cmd.message.edit(
					text="Something went Wrong. Contact my [Support Group](https://t.me/MoviesBazzz2).",
					parse_mode="markdown",
					disable_web_page_preview=True
				)
				return
		await cmd.message.edit(
			text=HOME_TEXT.format(cmd.message.chat.first_name, cmd.message.chat.id),
			parse_mode="Markdown",
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("Support Group", url="https://t.me/MoviesBazzz2"),
						InlineKeyboardButton("🔥MoviesBazzz🔥", url="https://t.me/joinchat/TP9IxftrpLQHA2NE")
					],
					[
						InlineKeyboardButton("About Bot", callback_data="aboutbot"),
						InlineKeyboardButton("About Dev", callback_data="aboutdevs")
					]
				]
			)
		)

Bot.run()
