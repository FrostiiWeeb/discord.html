import setuptools

with open("README.md", "r") as f:
	desc = f.read()

import re

with open("discord/html/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

setuptools.setup(
    name="discord.html",
    version=version,
    author="Alex Hutz",
	long_description=desc,
	long_description_content_type="text/markdown",
    author_email="frostiitheweeb@outlook.com",
    description="A discord.py wrapper, enables html-like interace.",
    url="https://github.com/FrostiiWeeb/discord.html",
    project_urls={
        "Bug Tracker": "https://github.com/FrostiiWeeb/discord.html/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=["discord.html", "discord"],
	install_requires=["aiohttp==3.7.4.post0", "discord.py==1.7.3"],
    python_requires=">=3.7",
)
