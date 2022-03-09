from discord.html import Parser

with open("examples/basic.html", "r") as f:
	contents = f.readlines()

parser = Parser()

parser.parse(contents)