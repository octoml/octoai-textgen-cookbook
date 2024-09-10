
import base64
import json
import os
import pandas as pd
import requests
import streamlit as st

from openai import OpenAI
from audiorecorder import audiorecorder
from services.db_client import CouchbaseClient
from services.nlq_engine import CouchbaseNLQEngine


client = CouchbaseClient()
engine = CouchbaseNLQEngine(client)
with open(os.path.join("resources", "collection_schemas.json"), "r") as f:
    collection_schemas = json.load(f)

def transcribe_audio(file_path: str):
    """
    Takes the file path of an audio file and transcribes it to text.

    Returns a string with the transcribed text.
    """
    with open(file_path, "rb") as f:
        encoded_audio = str(base64.b64encode(f.read()), "utf-8")

        reply = requests.post(
            "https://whisper-demo-kk0powt97tmb.octoai.run/predict",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.environ["OCTOAI_API_TOKEN"]}",
            },
            json={"audio": encoded_audio},
            timeout=300,
        )
        try:
            transcript = reply.json()["transcription"]
        except Exception as e:
            print(e)
            print(reply.text)
            raise ValueError("The transcription could not be completed.")

    return transcript

def do_transcription(audio_file_path):
    with st.status("Transcribing the audio to text..."):
        try:
            transcript = transcribe_audio(audio_file_path)
        except Exception as e:
            results = None

    if transcript is None:
        st.error("Transcription failed.")
    else:
        return transcript

# Streamlit page title
st.set_page_config(layout="wide", page_title="Travel Assistant Powered by OctoAI & Couchbase")

st.write("## Travel Assistant Powered by OctoAI & Couchbase")
st.write("#### Powered by natural language to SQL++ translation")

with st.sidebar:
    st.write("Hit record to capture your voice request")
    audio = audiorecorder("Click to record", "Click to stop recording")

if len(audio) > 0:
    st.audio(audio.export().read())

    # To save audio to a file, use pydub export method:
    audio.export("audio.wav", format="wav")
    transcript = do_transcription("audio.wav")
    st.text(transcript)

    sql_query, results = engine.run_query(collection_schemas, transcript)
    data_frame = pd.DataFrame.from_records(results)

    client = OpenAI(
        base_url="https://text.octoai.run/v1",
        api_key=os.environ["OCTOAI_API_TOKEN"],
    )
    system_prompt = "You are a helpful travel agent. You are given a user request complemented by context retrieved from a database that contains relevant information. Please provide helpful advice to the user as much as possible."
    user_prompt = f"user requests:\n{transcript}\n\n\ncontext:\n{results}"

    stream = client.chat.completions.create(
        model="meta-llama-3.1-70b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0,
        max_tokens=4096,
        stream=True
    )

    # Display SQL++ query
    st.markdown("Couchbase SQL++ query:" + "\n```\n" + sql_query + "\n```\n")
    # Display Dataframe
    st.dataframe(data_frame)
    # Stream the response
    st.write_stream(stream)
