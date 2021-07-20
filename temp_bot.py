import asyncio
import base64  # inbuilt module for encoding and decodingto base64
import html
import json  # builtin module for json handling
import os  # builtin module
import pprint as pp  # pip install pprintpp
import re  # regex
from io import StringIO
from sys import prefix

import discord  # pip install discord
from discord.ext import commands

import markdown  # pip install markdown
import requests  # pip install requests
import urllib3  # pip install urllib3
from bs4 import BeautifulSoup  # pip install beautifulsoup4
from dotenv import load_dotenv  # pip install python-dotenv
from markdown import Markdown  # pip install markdown

prefix = ';'

load_dotenv()
client = discord.Client()


def md_to_text(md):
    html = markdown.markdown(md)
    soup = BeautifulSoup(html, features='html.parser')
    return soup.get_text()


def substring_range(s, substring):
    for i in re.finditer(re.escape(substring), s):
        return (i.start(), i.end())


encoded = {
    "source_code": True,
    "language_id": False,
    "compiler_options": False,
    "command_line_arguments": False,
    "stdin": True,
    "stdout": True,
    "stderr": True,
    "expected_output": True,
    "cpu_time_limit": False,
    "cpu_extra_time": False,
    "wall_time_limit": False,
    "memory_limit": False,
    "stack_limit": False,
    "max_processes_and_or_threads": False,
    "enable_per_process_and_thread_time_limit": False,
    "enable_per_process_and_thread_memory_limit": False,
    "max_file_size": False,
    "redirect_stderr_to_stdout": False,
    "enable_network": False,
    "number_of_runs": False,
    "additional_files": True,
    "callback_url": False,
    "compile_output": True,
    "message": True,
    "exit_code": False,
    "exit_signal": False,
    "status": False,
    "created_at": False,
    "finished_at": False,
    "token": False,
    "time": False,
    "wall_time": False,
    "memory": False,
    "status_id": False,
    "language": False,

}
data = dict()
with open('languages.json') as json_file:
    data = json.load(json_file)
# print(data)


def encode(text: str):
    text_bytes = text.encode('utf-8')
    base64_bytes = base64.b64encode(text_bytes)
    base64_string = base64_bytes.decode("utf-8")
    return base64_string


def decode(b64_string: str):
    # print("recieved string: ", b64_string)
    # print("\n\n")
    base64_bytes = b64_string.encode("utf-8")

    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("utf-8")
    return sample_string


def compile_cpp_api(text: str, Input: str = None, language: str = "cpp"):

    url = "https://judge0-ce.p.rapidapi.com/submissions"
    querystring = {"base64_encoded": "true", "fields": "*"}
    if(Input is not None):
        payload = """{
                        \"language_id\": 54,
                        \"source_code\": \"%s\",
                        \"stdin\": \"%s\"
                    }""" % (encode(text), encode(str(Input)))
    else:
        payload = """{
                        \"language_id\": 54,
                        \"source_code\": \"%s\"
                    }""" % (encode(text))

    headers = {
        'content-type': "application/json",
        'x-rapidapi-key': "23e08b8c15msh855c063c63e9ffbp1113d6jsn35b0994c372f",
        'x-rapidapi-host': "judge0-ce.p.rapidapi.com"
    }

    response = requests.request(
        "POST", url, data=payload, headers=headers, params=querystring)
    status_code = response.status_code
    print("POST response code: ", status_code)
    # print(" POST response text: " + response.text)
    if(status_code >= 400):
        return response.text
    token = (json.loads(response.text))['token']
    # print("Submission token: %s" % token)

    # Getting the submission
    headers = {
        'x-rapidapi-key': "23e08b8c15msh855c063c63e9ffbp1113d6jsn35b0994c372f",
        'x-rapidapi-host': "judge0-ce.p.rapidapi.com"
    }
    # Get response from the API
    response = requests.request(
        "GET", url+'/'+str(token), headers=headers, params=querystring)

    print("Get response code: ", response.status_code)

    # Handle the basic errors
    if(response.status_code == 401):
        return "Authentication Failed"

    elif(response.status_code == 400):
        return "some attributes for this submission cannot be converted to UTF-8, use base64_encoded=true query parameter"

    # get the relevant info in json format
    received_response = json.loads(response.text)

    # dump it into a file
    with open("encode.json", "w") as outfile:
        outfile.write(response.text)

    # print the dict
    pp.pprint(received_response)
    # print("compile_output:\n ", received_response['compile_output'])

    # decode the stuff line by line which are encodes in b64
    for key in received_response:
        if(encoded[key] == True and received_response[key] is not None):
            temp = received_response[key]
            temp = temp.splitlines()
            received_response[key] = ""
            for i in range(len(temp)):
                received_response[key] += (decode(temp[i]))

    pp.pprint(received_response)
    json_object = json.dumps(received_response, indent=4)

    # dump the decoded response
    with open("decode.json", "w") as outfile:
        outfile.write(json_object)
        return received_response


async def compile_cpp(message, code, Input=None, lang="cpp"):

    output = compile_cpp_api(code, Input, lang)
    s = ""
    if(isinstance(output, (str, int, float))):
        await message.channel.send("```"+output+"```")
    elif (isinstance(output, dict)):
        s += ("```Source Code Received: \n```" + "```" +
              lang+"\n" + output["source_code"]+"\n```")

        s += ("```Status id : %s" %
              output["status"]["id"] + '\n' + output["status"]["description"]+"\n```")

        # if there is some comiple output
        if(output["compile_output"] is not None):
            s += ("```compiler output:\n" +
                  output["compile_output"]+'\n'+'```')

        # If there was some user input
        if(output["stdin"] is not None):
            s += ("```Input:\n "+output["stdin"]+"\n```")
        else:
            s += ("```No Input\n```")

        # If there is some program output
        if(output["stdout"] is not None):
            s += ("```Output:\n" + output["stdout"]+"\n```")
        else:
            s += ("```No Output\n```")

        #  If there is some standard Error output
        if(output["stderr"] is not None):
            s += ("```Standard Error\n" + output["stderr"]+"\n```")

        # Time taken by program to run
        if(output["time"] is not None):
            s += ("```Time Taken (ms): " +
                  str(float(output["time"])*1000)+"\n```")

        # Memory utilised by the program
        if(output["memory"] is not None):
            s += ("```Memory Used (KB): " + str(output["memory"])+"\n```")

        await message.channel.send(s)


@ client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower() == prefix+'hello':
        await message.channel.send('Hello!')
        return
    print(list(message.content.replace('\n', '').replace(" ", '')))
    temp = message.content.replace('\n', '').replace(" ", '').lower()
    print("temp: ", temp)
    if temp.startswith(prefix+'compile'):
        # temp_remove = substring_range(temp, prefix+'compile')
        s = message.content[len(prefix+'compile'):].lstrip()
        print(list(s))
        if s.startswith("```cpp", 0, 6):
            await message.channel.send("C++ code")
            s = s[3:len(s)-3]
            # print(s)
            lang = (s.partition('\n')[0]).strip()
            # print(lang)
            await message.channel.send("```language: %s```" % lang)
            code = s.join(s.split('\n', 1)[1:])
            code.strip()
            # print(code)
            temp = await message.channel.send("User Input (give in code blocks) (wait time of 60 sec) (send 👎 to cancel input): ")
            # await temp.add_reaction('👎')

            def message_check(m):
                return m.channel == message.channel and m.author == message.author

            msg = ""
            try:
                msg = await client.wait_for('message', timeout=60.0, check=message_check)
                if "👎" in msg.content:
                    await message.channel.send("`No User Input`")
                    return await compile_cpp(message, code)

            except asyncio.TimeoutError:
                await message.channel.send("`No user input recieved (Timeout)`")
                await compile_cpp(message, code)

            else:
                await message.channel.send("User input recieved 👍")
                print(msg.content)
                await compile_cpp(message, code, msg.content[3:len(msg.content)-3])

client.run(os.getenv('TOKEN'))
