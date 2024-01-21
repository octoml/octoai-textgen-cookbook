require('dotenv').config()
const { Client } = require("@octoai/client");
const pdf = require('pdf-parse');
const prompts = require('prompts');
const fs = require('fs/promises');
const path = require('path');
prompts.override(require('yargs').argv);

const client = new Client(process.env.OCTOAI_TOKEN);

(async () => {


const completion = await client.chat.completions.create( {
		"messages": [
		{
			"role": "system",
			"content": "You are a helpful assistant. Keep your responses limited to one short paragraph if possible."
		},
		{
			"role": "user",
			"content": "Hello world"
		}
		],
		"model": "llama-2-13b-chat-fp16",
		"max_tokens": 128,
		"presence_penalty": 0,
		"temperature": 0.1,
		"top_p": 0.9
	});

	console.log(completion.choices[0].message.content)
}
)();