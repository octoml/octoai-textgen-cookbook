const { Client } = require("@octoai/client")

const client = new Client(process.env.OCTO_CLIENT_TOKEN);

export default async function handler(req, res) {
  const body = JSON.parse(req.body);
  console.log(body.text)
  const completion = await client.chat.completions.create( {
    "messages": [
      {
        "role": "system",
        "content": "You are a tool that summarizes text. This tool is a web appliation that extracts text from a PDF document and produces a formatted list of the main points in the given text. Do not communicate with the user directly."
      },
      {
        "role": "assistant",
        "content": `text:\n${body.text}`
      },
    ],
    "model": "mixtral-8x7b-instruct-fp16",
    "presence_penalty": 0,
    "temperature": 0.1,
    "top_p": 0.9
  });   
  res.status(200).json({ message: completion.choices[0].message })
}
