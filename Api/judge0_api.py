import json  # builtin module for json handling
import os
import pprint as pp  # pip install pprintpp

import requests  # pip install requests
import urllib3  # pip install urllib3
from Utility.utils import decode, encode

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


def compile_api(text: str, Input: str = None, language: int = 54):

    if(not isinstance(language, int)):
        raise Exception("""language has to be an integer not %s""" %
                        (type(language)))

    url = "https://judge0-ce.p.rapidapi.com/submissions"
    querystring = {"base64_encoded": "true", "fields": "*"}
    if(Input is not None):
        payload = """{
                        \"language_id\": %s,
                        \"source_code\": \"%s\",
                        \"stdin\": \"%s\"
                    }""" % (str(language), encode(text), encode(str(Input)), )
    else:
        payload = """{
                        \"language_id\": %s,
                        \"source_code\": \"%s\"
                    }""" % (str(language), encode(text))

    headers = {
        'content-type': "application/json",
        'x-rapidapi-key': "%s" % (os.getenv('x-rapidapi-key')),
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
        'x-rapidapi-key': "%s" % os.getenv('x-rapidapi-key'),
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
    with open("Api\\encode.json", "w") as outfile:
        outfile.write(response.text)

    # print("compile_output:\n ", received_response['compile_output'])

    # decode the stuff line by line which are encodes in b64
    for key in received_response:
        if(encoded[key] is True and received_response[key] is not None):
            temp = received_response[key]
            temp = temp.splitlines()
            received_response[key] = ""
            for i in range(len(temp)):
                received_response[key] += (decode(temp[i]))

    pp.pprint(received_response)
    json_object = json.dumps(received_response, indent=4)

    # dump the decoded response
    with open("Api\\decode.json", "w") as outfile:
        outfile.write(json_object)
    return received_response


async def compile_bot(ctx, code, Input=None, lang=54):

    output = compile_api(code, Input, lang)
    s = ""
    if(isinstance(output, (str, int, float))):
        await ctx.send("```"+output+"```")
    elif (isinstance(output, dict)):
        s += ("```Source Code Received: \n```" + "```" +
              "\n" + output["source_code"]+"\n```")
        await ctx.send(s)
        s = ""

        s += ("```Status id : %s" %
              output["status"]["id"] + '\n' + output["status"]["description"]+"\n```")

        # if there is some compile output
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

        await ctx.send(s)
