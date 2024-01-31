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
