import pandas as pd
import asyncio
import json
from logging import raiseExceptions  # builtin module for json handling
import os  # builtin module
import pprint as pp  # pip install pprintpp
from io import StringIO

import discord  # pip install discord
from discord.ext import commands
from dotenv import load_dotenv  # pip install python-dotenv

from Api.judge0_api import compile_bot

prefix = ';'

load_dotenv()
bot = commands.Bot(
    prefix, description="A fun bot that currently compiles over 40 different languages",
    case_insensitive=True)


class Emotes:
    yay = "<:yay:867316844824887328>"


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


convert_lang = {
    "cpp": "C++",
    "c": "C",
    "c++": "C++",
    "py": "Python",
    "python": "Python",
    "vbnet": "Visual Basic.Net",
    "bash": "Bash",
    "basic": "Basic",
    "clojure": "Clojure",
    "csharp": "C#",
    "crystal": "Crystal",
    "d": "D",
    "elixir": "Elixir",
    "erlang": "Erlang",
    "fsharp": "F#",
    "fortran": "Fortran",
    "go": "GO",
    "groovy": "Groovy",
    "haskell": "Haskell",
    "insect": "Insect",
    "java": "Java",
    "javascript": "Javascript",
    "js": "Javascript",
    "kotlin": "Kotlin",
    "ocaml": "OCaml",
    "octave": "Octave",
    "pascal": "Pascal",
    "perl": "Perl",
    "php": "PHP",
    "txt": "Plain Text",
    "prolog": "Prolog",
    "r": "R",
    "ruby": "Ruby",
    "rust": "Rust",
    "scala": "Scala",
    "swift": "Swift",
    "sql": "SQL",
    "mysql": "SQL",
    "typescript": "Typescript",
    "assembly": "Assembly",
    "lisp": "Lisp",
}
languages = dict()
with open('Api\\languages.json') as json_file:
    languages = json.load(json_file)

(pd.DataFrame.from_dict(data=convert_lang, orient='index')
   .to_csv('dict_file.csv', header=False))


@bot.event
async def on_ready():  # When the bot starts
    print(f"Bot online and logged in as {bot.user}")


@ bot.command(name="hello", aliases=["hi"])
async def hello(ctx):
    if(ctx.message.author.id == 360714746363904000):
        await ctx.send("Hello Master " + ctx.message.author.mention)
        await ctx.send(Emotes.yay)
    else:
        await ctx.send("Hi"+ctx.message.author.mention)


@ bot.command(name="embed")
async def embedi(ctx):
    embed = discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/",
                          description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
    await ctx.send(embed=embed)


@bot.command(name="languages", aliases=["lang", "langs"],
             brief="List of languages supported by the bot",
             description="List of languages and the compilers used by the bot")
async def langs(ctx):
    desc = """ 
+------------------+------------------+
| code Blocks lang | Compiler Lang    |
+------------------+------------------+
| cpp              | C++              |
+------------------+------------------+
| c                | C                |
+------------------+------------------+
| c++              | C++              |
+------------------+------------------+
| py               | Python           |
+------------------+------------------+
| python           | Python           |
+------------------+------------------+
| vbnet            | Visual Basic.Net |
+------------------+------------------+
| bash             | Bash             |
+------------------+------------------+
| basic            | Basic            |
+------------------+------------------+
| clojure          | Clojure          |
+------------------+------------------+
| csharp           | C#               |
+------------------+------------------+
| crystal          | Crystal          |
+------------------+------------------+
| d                | D                |
+------------------+------------------+
| elixir           | Elixir           |
+------------------+------------------+
| erlang           | Erlang           |
+------------------+------------------+
| fsharp           | F#               |
+------------------+------------------+
| fortran          | Fortran          |
+------------------+------------------+
| go               | GO               |
+------------------+------------------+
| groovy           | Groovy           |
+------------------+------------------+
| haskell          | Haskell          |
+------------------+------------------+
| insect           | Insect           |
+------------------+------------------+
| java             | Java             |
+------------------+------------------+
| javascript       | Javascript       |
+------------------+------------------+
| js               | Javascript       |
+------------------+------------------+
| kotlin           | Kotlin           |
+------------------+------------------+
| ocaml            | OCaml            |
+------------------+------------------+
| octave           | Octave           |
+------------------+------------------+
| pascal           | Pascal           |
+------------------+------------------+
| perl             | Perl             |
+------------------+------------------+
| php              | PHP              |
+------------------+------------------+
| txt              | Plain Text       |
+------------------+------------------+
| prolog           | Prolog           |
+------------------+------------------+
| r                | R                |
+------------------+------------------+
| ruby             | Ruby             |
+------------------+------------------+
| rust             | Rust             |
+------------------+------------------+
| scala            | Scala            |
+------------------+------------------+
| swift            | Swift            |
+------------------+------------------+
| sql              | SQL              |
+------------------+------------------+
| mysql            | SQL              |
+------------------+------------------+
| typescript       | Typescript       |
+------------------+------------------+
| assembly         | Assembly         |
+------------------+------------------+
| lisp             | Lisp             |
+------------------+------------------+
"""

    pages = []
    for i in range(len(desc)//761+1):
        s = desc[761*i:(761*(i+1))]
        pages.append(discord.Embed(title="List of Languages",
                     description="```\n"+s+"\n```",
                     colour=discord.Colour.orange()))
    # skip to start, left, right, skip to end
    buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]
    current = 0
    msg = await ctx.send(embed=pages[current])

    for button in buttons:
        await msg.add_reaction(button)

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=10.0)

        except asyncio.TimeoutError:
            # return print("test")
            embed = pages[current]
            embed.set_footer(text="Timed Out")
            await msg.clear_reactions()
            return print("test")

        else:
            previous_page = current
            if reaction.emoji == u"\u23EA":
                current = 0

            elif reaction.emoji == u"\u2B05":
                if current > 0:
                    current -= 1

            elif reaction.emoji == u"\u27A1":
                if current < len(pages)-1:
                    current += 1

            elif reaction.emoji == u"\u23E9":
                current = len(pages)-1

            for button in buttons:
                await msg.remove_reaction(button, ctx.author)

            if current != previous_page:
                await msg.edit(embed=pages[current])
        # await ctx.send("```\n"+s+"\n```")


@bot.command(name="compile",
             brief="Compiles code",
             description="""Compiles code given in code blocks "\\`\\`\\`lang\\`\\`\\`"
                            It takes the language given in the code block as a prameter
                            and the code given in the code block as source code.
                            It will ask for compiler options based on the language chosen and user input.
                        
                            Results include compiler output, stdin,stdout,stderr,time taken and memory used.
                            
                            check out ;languages for list of languages supported
                            """)
async def Compile(ctx):

    print(ctx.message.content)
    s = ctx.message.content[8:]
    s = s[4:len(s)-3]
    print(s)
    lang = (s.partition('\n')[0]).strip()
    print(lang)
    try:
        convert_lang[lang]
    except KeyError:
        return await ctx.send("Unkown language. Use `;languages` to get list of languages")
    await ctx.send("```language: %s```" % lang)

    code = s.join(s.split('\n', 1)[1:])
    code.strip()

    def message_check(m):
        return m.channel == ctx.channel and m.author == ctx.message.author

    def rxn_check(reaction, user):
        try:
            return user == ctx.message.author and emote_to_num[str(reaction.emoji)] <= len(opt)
        except KeyError:
            return False

    opt = dict()
    try:
        search(convert_lang[lang], opt)
    except KeyError:
        return await ctx.send("Unkown language. Use `;languages` to get list of languages")
    # print(opt)
    # description of the compiler embed
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
        await compile_bot(ctx, code, msg.content[3:len(msg.content)-3].replace('\n', "", 1), lang=int(compiler[0]))


def search(lang, opt):
    k = 1
    for language in languages:
        if ((language["name"].lower().startswith(lang.lower()+" ") or language["name"].lower() == lang.lower()) and
                (language["is_archived"] == False)):
            try:
                opt[k] = [language["id"], language["name"]]
            except:
                raise Exception("Unknown language")
            k += 1
    print(k)
    pp.pprint(opt)


bot.run(os.getenv('TOKEN'))
