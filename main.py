import asyncio
import json  # builtin module for json handling
import os  # builtin module
import pprint as pp  # pip install pprintpp
from io import StringIO

import discord  # pip install discord
import markdown  # pip install markdown
from bs4 import BeautifulSoup  # pip install beautifulsoup4
from discord.ext import commands
from dotenv import load_dotenv  # pip install python-dotenv
from markdown import Markdown  # pip install markdown

from Api_handling.judge0_api import compile_bot

prefix = ';'

load_dotenv()
bot = commands.Bot(
    prefix, description="A fun bot that currently only compiles c++,c,py and vbnet code",
    case_insensitive=True)


num_to_emote = {
    0: "0️⃣",
    1: "1️⃣",
    2: "2️⃣",
    3: "3️⃣",
    4: "4️⃣",
    5: "5️⃣",
    6: "6️⃣",
    7: "7️⃣",
    8: "8️⃣",
    9: "9️⃣",
    10: "🔟",
    11: "😀",
    12: "😃",
}
emote_to_num = {
    "0️⃣": 0,
    "1️⃣": 1,
    "2️⃣": 2,
    "3️⃣": 3,
    "4️⃣": 4,
    "5️⃣": 5,
    "6️⃣": 6,
    "7️⃣": 7,
    "8️⃣": 8,
    "9️⃣": 9,
    "🔟": 10,
    "😀": 11,
    "😃": 12
}


convert_lang = {"cpp": "C++",
                "c": "C",
                "py": "Python",
                "python": "Python",
                "vbnet": "Visual Basic.Net"
                }
languages = dict()
with open('Api_handling\\languages.json') as json_file:
    languages = json.load(json_file)


@bot.event
async def on_ready():  # When the bot starts
    print(f"Bot online and logged in as {bot.user}")


@ bot.command(name="embed")
async def embedi(ctx):
    embed = discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/",
                          description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
    await ctx.send(embed=embed)


@ bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hi " + ctx.message.author.display_name)


@bot.command(name="compile")
async def Compile(ctx):
    i = 3
    print(ctx.message.content)
    s = ctx.message.content[8:]
    s = s[4:len(s)-3]
    print(s)
    lang = (s.partition('\n')[0]).strip()
    print(lang)
    await ctx.send("```language: %s```" % lang)
    code = s.join(s.split('\n', 1)[1:])
    code.strip()

    def message_check(m):
        return m.channel == ctx.channel and m.author == ctx.message.author

    def rxn_check(reaction, user):
        try:
            return user == ctx.message.author and emote_to_num[str(reaction.emoji)] <= 10
        except KeyError:
            return False

    opt = dict()
    search(convert_lang[lang], opt)
    # print(opt)
    desc = ""
    for i in opt.keys():
        desc += num_to_emote[i] + " "+opt[i][1]+"\n"

    embed = discord.Embed(title="Choose Compiler Options", description=desc)
    embed_message = await ctx.send(embed=embed)

    for i in (opt.keys()):
        print(num_to_emote[i])
        await embed_message.add_reaction(num_to_emote[i])
    compiler = ""
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=rxn_check)
    except asyncio.TimeoutError:
        await ctx.send("No User specification, by default 1st option is chosen")
        compiler = opt[1]
    else:
        compiler = opt[emote_to_num[str(reaction.emoji)]]
        await ctx.send("Compiler chosen: %s" % compiler[1])
    print(compiler)
    embed = discord.Embed(
        title="User Input", description="give Input in code blocks\n send 👎 (not in code blocks) to cancel input\n Wait time of 60 sec ")
    embed_message = await ctx.send(embed=embed)

    # temp = await ctx.send("User Input () (wait time of 60 sec) (send 👎 to cancel input): ")

    msg = ""
    try:
        msg = await bot.wait_for('message', timeout=60.0, check=message_check)
        if "👎" in msg.content:
            await ctx.send("`No User Input`")
            return await compile_bot(ctx, code, lang=int(compiler[0]))

    except asyncio.TimeoutError:
        await ctx.send("`No user input recieved (Timeout)`")
        await compile_bot(ctx, code, lang=int(compiler[0]))

    else:
        await ctx.send("User input recieved 👍")
        print(msg.content)
        await compile_bot(ctx, code, msg.content[3:len(msg.content)-3], lang=int(compiler[0]))

# print(languages)


def search(lang, opt):
    k = 1
    for language in languages:
        if language["name"].lower().startswith(lang.lower()+" "):
            opt[k] = [language["id"], language["name"]]
            k += 1
    print(k)
    pp.pprint(opt)


print(os.getenv('x-rapidapi-key'))
bot.run(os.getenv('TOKEN'))
