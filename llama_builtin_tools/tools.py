import os
import sys
from io import StringIO
import contextlib

from brave import Brave
from wolframalpha import Client
import nest_asyncio


import json
import requests

import base64


# Brave search definition
def brave_search(query: str) -> str:
    brave = Brave(os.environ["BRAVE_API_KEY"])
    results = brave.search(q=query, count=10)
    return str(results)


# Need to run this for Wolfram client lib
nest_asyncio.apply()

# Wolfram Alpha definition
def wolfram_alpha(query: str) -> str:
    client = Client(os.environ["WOLFRAM_APP_ID"])
    a = str(client.query(query))
    print(a)
    return a


# Helper for Code Interpreter
@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


# Code interpreter definition
def code_interpreter(code: str) -> str:
    with stdoutIO() as s:
        exec("{}".format(code))
    return s.getvalue()


def photogen(query: str) -> str:
    url = "https://image.octoai.run/generate/sdxl"

    headers = {
        "Authorization": f"Bearer {os.environ["OCTOAI_TOKEN"]}",
        "Content-Type": "application/json",
    }

    # Define the data payload
    data = {
        "prompt": f"A beautiful image of {query}",
        "checkpoint": "octoai:lightning_sdxl",
        "width": 1024,
        "height": 1024,
        "num_images": 1,
        "sampler": "DPM_PLUS_PLUS_SDE_KARRAS",
        "steps": 8,
        "cfg_scale": 3,
        "use_refiner": False,
        "style_preset": "base",
    }

    # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Parse the JSON response
    response_json = response.json()
    image_b64 = response_json["images"][0]["image_b64"]

    # Decode the base64 image and save it to a file
    image_data = base64.b64decode(image_b64)

    # write image to disk
    filename = "result.jpg"
    with open(filename, "wb") as f:
        f.write(image_data)

    return filename
