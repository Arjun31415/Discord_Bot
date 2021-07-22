import asyncio
import datetime
import json  # builtin module for json handling
import os  # builtin module
import pprint as pp  # pip install pprintpp
import subprocess
import sys
import time
from io import StringIO
from typing import Text

import discord  # pip install discord
import pandas as pd
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from dotenv import load_dotenv  # pip install python-dotenv

from Api.judge0_api import compile_bot

prefix = ';'

load_dotenv()

help_command = commands.DefaultHelpCommand(
    no_category='Misc Commands'
)

bot = commands.Bot(
    prefix, description="A fun bot that currently compiles over 40 different languages",
    case_insensitive=True,
    help_command=help_command)


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

# (pd.DataFrame.from_dict(data=convert_lang, orient='index')
#    .to_csv('dict_file.csv', header=False))

# Change only the no_category default string


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


@bot.command(name="fetch")
async def fetch(ctx, msgid: int):
    if(msgid is None):
        return await ctx.send(embed=discord.Embed(
            description="Message id is missing",
            timestamp=datetime.datetime.utcnow(),
            color=0xfc3503))
    if(not isinstance(msgid, int)):
        return await ctx.send(embed=discord.Embed(
            description="Message id must be an integer",
            timestamp=datetime.datetime.utcnow(),
            color=0xfc3503))
    msg = None
    try:
        msg = await ctx.fetch_message(msgid)

    except Exception:
        pass

    if(not msg):
        for channel in bot.get_all_channels():
            if(msg):
                break
            if channel.type != discord.ChannelType.text:
                continue
            try:
                msg = await channel.fetch_message(msgid)
            except Exception:
                pass
    if(msg is None):
        return await ctx.send(
            embed=discord.Embed(
                description="Message not found",
                color=discord.Colour.red()
            )
        )
    author = msg.author
    embed = discord.Embed(
        timestamp=msg.created_at,
        description="[jump to message\n](%s)" % msg.jump_url + msg.content,
        color=discord.Colour.blurple())
    embed.set_author(
        icon_url=author.avatar_url,
        name="{user}".format(user=author.name))
    print(author.avatar_url)
    return await ctx.send(embed=embed)

# @bot.command()
# async def args(ctx, arg1, arg2):
#     await ctx.send('You sent {} and {}'.format(arg1, arg2))


@ bot.command(name="embed")
async def embedi(ctx):
    embed = discord.Embed(
        title="Sample Embed", url="https://realdrewdata.medium.com/",
        description="```This is an embed that will show how to build an embed and the different components```",
        color=0xFF5733)
    embed.set_footer(text="1/1")
    await ctx.send(embed=embed)


class Code_Compilation(commands.Cog, name="Code Compilation", description="Commands which are involved in code compiltaion and execution"):
    @ commands.command(
        name="languages", aliases=["lang", "langs"],
        brief="List of languages supported by the bot",
        description="List of languages and the compilers used by the bot")
    async def langs(self, ctx):
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
        temp = desc.splitlines()
        n = (len(temp)+29)//30
        print(n)
        for i in range(n):
            s = "\n".join(temp[i*30:(1+i)*30])
            pages.append(discord.Embed(
                title="List of Languages",
                description="```\n"+s+"\n```",
                colour=discord.Colour.orange()))
            pages[i].set_footer(text=f"{1+i}/{n}")
        # skip to start, left, right, skip to end
        buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]
        current = 0
        msg = await ctx.send(embed=pages[current])

        for button in buttons:
            await msg.add_reaction(button)

        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons,
                                                    timeout=300.0)

            except asyncio.TimeoutError:

                await msg.clear_reactions()
                return print("timed out")

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

    @commands.cooldown(2, 30, commands.BucketType.user)
    @commands.command(
        name="compile",
        brief="Compiles code",
        description="""Compiles code given in code blocks "\\`\\`\\`lang\\`\\`\\`"
                        It takes the language given in the code block as a prameter
                        and the code given in the code block as source code.
                        It will ask for compiler options based on the language chosen and user input.
                    
                        Results include compiler output, stdin,stdout,stderr,time taken and memory used.
                        
                        check out ;languages for list of languages supported
                                """)
    async def Compile(self, ctx):

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

        # description of the compiler embed
        desc = ""
        for i in opt.keys():
            desc += num_to_emote[i] + " "+opt[i][1]+"\n"

        embed = discord.Embed(
            title="Choose Compiler Options", description=desc)
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

    @Compile.error
    async def command_name_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(
                title=f"Slow it down bro!",
                description=f"Try again in {error.retry_after:.2f}s.",
                color=discord.Color.dark_red()
            )
            await ctx.send(embed=em, delete_after=error.retry_after)

    @commands.command(
        name="eval", aliases=["evaluate"], breif="Only Trusted people and bot devs can use this command",
        description="Uses compile() to run python code"
    )
    async def evaluate(self, ctx):
        if(ctx.message.author.id != 360714746363904000):
            return
        s = ctx.message.content
        temp = s.lower()
        print(temp)
        if(temp.startswith(";evaluate")):
            s = s[len(";evaluate")+1:]
            print(s)
        else:
            s = s[len(";eval")+1:]
            s = s[3:len(s)-3]
            print(s)
            lang = (s.partition('\n')[0]).strip()
            print(lang)
            if(not (lang == 'py' or lang == 'python')):
                return await ctx.send("Must be in python")
            code = s.join(s.split('\n', 1)[1:])
            print(code)
            orig = sys.stdout

            try:
                codeObejct = compile(code, "temp", "exec")
            except Exception as e:
                print(e)
                await ctx.send("Compile error: ")
                return await ctx.send(e)

            try:
                sys.stdout = open(
                    "C:\\ARJUN\\Coding\\Discord_Bot\\output.txt", "w")
                ldict = dict()
                exec(codeObejct, globals(), {"ctx": ctx, "bot": bot})
            except Exception as e:
                print(e)
                await ctx.send("Runtime error: ")
                return await ctx.send(e)
            else:
                sys.stdout = orig
                s = ""
                with open("output.txt", "r") as f:
                    s += f.read()
                print("output.txt: ", s)
                try:
                    await ctx.send(s)
                except discord.errors.HTTPException as e:
                    if(e.status == 400):
                        await ctx.send("Empty stdout")
                    else:
                        await ctx.send(e.text)
                await ctx.send(ldict)
            finally:
                sys.stdout = orig


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


bot.add_cog(Code_Compilation())
bot.run(os.getenv('TOKEN'))
