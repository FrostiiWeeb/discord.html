# std libraries
import typing
import asyncio

from enum import Enum
from inspect import Parameter, _ParameterKind

# third party
import discord
import tempfile

from bs4 import BeautifulSoup
from discord.ext import commands
from discord.ext.commands.errors import ClientException, MissingRequiredArgument

# local
from .bot import Bot, BOT

class TagTable(Enum):
	bot_starting = "<bot"
	bot_ending = "/bot>"
	run = "<run>"
	
def indent(text: str, amount, ch=' '):
	padding = amount * ch
	return ''.join(padding+line for line in text.splitlines(keepends=False))

class Parser:
	def __init__(self) -> None:
		pass

	def parse(self, contents: typing.List[str]):
		bots: typing.List[Bot] = []
		events: typing.List[typing.Callable] = []
		bot_initiated: typing.Optional[bool] = False
		content = "\n".join([line.strip(" ") for line in contents])
		soup = BeautifulSoup(content, "html5lib")
		for bot in soup.find_all("bot"):
			prefix = bot.get("prefix")
			token = bot.get("token")
			prefix_param = Parameter("prefix", _ParameterKind.KEYWORD_ONLY)
			token_param = Parameter("token", _ParameterKind.KEYWORD_ONLY)
			if not prefix:
				raise MissingRequiredArgument(prefix_param)
			if not token_param:
				raise MissingRequiredArgument(token_param)
			bot_initiated = True
			bots.append(Bot(prefix, token=token))
			bot_obj = bots[0]
			events = bot.find_all("event")
			for event in events:
				type = event.get("type")
				params = event.get("parameters")
				if not type:
					raise MissingRequiredArgument(Parameter("type", _ParameterKind.KEYWORD_ONLY))
				response = event.find("response")
				content = (response.contents[0])
				l = {}
				exec(f"async def {type}({params}):\n{indent(text=content, amount=4)}", l)
				bot_obj.add_listener((l[type]))
		run = soup.find("run")
		if run:
			if not bot_initiated:
				raise ClientException("Bot has not been initialized")
			if len(bots) > 1:
				raise RuntimeError("Exceeded max bot instances")
			(bots[0]).run((bots[0]).token)