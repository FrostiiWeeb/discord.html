import typing

import discord

from discord.ext import commands

BOT = typing.TypeVar("BOT", bound="Bot")

class Bot(commands.Bot, typing.Generic[BOT]):
	def __init__(self, command_prefix, help_command=None, description=None, **options):
		self.token = options.pop("token")
		super().__init__(command_prefix, help_command, description, **options)