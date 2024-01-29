# How to build a simple summarizer using Next JS and OctoAI Mixtral 8x7B LLM.

OctoAI LLMs such as Mixtral 8x7B LLM are very capable open source large language models (LLMs) that can be used to power text manipulation apps.

In this example, you will build a simple NextJS app powered by OctoAI Mixtral 8x7B LLM.

## Instructions

1. Download or clone this project:
2. Install dependencies

```
$ npm install
```


### Environment setup

To run our example app, first we need to set up our environment variable, we can do this by:

- Get an OctoAI API token by following [these instructions](https://octo.ai/docs/getting-started/how-to-create-octoai-api-token/).
- Paste your API token in the file called `.env` in this directory.

```bash
OCTO_CLIENT_TOKEN=<your key here>
```

### Running the application

Run `dev` script to fire up server.
```bash
npm run dev
```

That's it! if you head to `localhost:3000` you should see the app running.
### Example usage
Upload a PDF file using the Upload button, and see both the current pdf text on the left, and the summarized version on the right.

You can tweak the parameters of the LLM in the `api/summarize` file.

```js
const { Client } = require("@octoai/client")

const client = new Client(process.env.OCTO_CLIENT_TOKEN);

export default async function handler(req, res) {
  const body = JSON.parse(req.body);
  console.log(body.text)
  const completion = await client.chat.completions.create( {
    "messages": [
      {
        "role": "system",
        "content": `Summarize the following text:${body.text}`
      },
    ],
    "model": "mixtral-8x7b-instruct-fp16",
    "presence_penalty": 0,
    "temperature": 0.1,
    "top_p": 0.9
  });   
  res.status(200).json({ message: completion.choices[0].message })
}

```

## License

This project is licensed under the MIT License.