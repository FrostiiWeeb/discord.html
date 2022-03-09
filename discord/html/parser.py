# std libraries
import re
import typing
import asyncio

from enum import Enum, IntEnum

# third party
import discord

from bs4 import BeautifulSoup
from discord.ext import commands

BOT = typing.TypeVar("BOT", bound="Bot")

class TagTable(Enum):
	bot_starting = "<bot"
	bot_ending = "/bot>"
	run = "<run>"

class Bot(commands.Bot, typing.Generic[BOT]):
	def __init__(self, command_prefix, help_command=None, description=None, **options):
		self.token = options.pop("token")
		super().__init__(command_prefix, help_command, description, **options)

class Parser:
	def __init__(self) -> None:
		pass

	def parse(self, contents: typing.List[str]):
		bot: Bot = None
		bot_initiated: typing.Optional[bool] = False
		bot_ended: typing.Optional[bool] = False
		for line in contents:
			line = line.strip(" ")
			if line.startswith("<bot"):
				if bot_initiated:
					raise ValueError("Max Bot Instances: 1")
				try:
					token = re.search(r'token=[\'"]([^\'"]*)[\'"]', line, re.MULTILINE).group(1)
				except AttributeError:
					raise ValueError("token parameter missing")
				try:
					command_prefix = re.search(r'prefix=[\'"]([^\'"]*)[\'"]', line, re.MULTILINE).group(1)
				except AttributeError:
					raise ValueError("prefix attribute not set.")
				bot = Bot(token=token, command_prefix=command_prefix)
			if line.startswith("</bot"):
				if bot_ended:
					raise ValueError("Max Bot Instances: 1")
				bot_ended = True
			if line.startswith("<run>"):
				if not bot:
					raise ValueError("Bot not initialized")
				bot.run(bot.token)