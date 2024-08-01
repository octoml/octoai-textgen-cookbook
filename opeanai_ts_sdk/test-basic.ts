import OpenAI from 'openai';

const openai = new OpenAI({
    baseURL: 'https://text.octoai.run/v1',
    apiKey: process.env.OCTOAI_API_KEY
});

async function main() {
  const completion = await openai.chat.completions.create({
    model: 'meta-llama-3.1-8b-instruct',
    messages: [{ role: 'user', content: 'count to ten' }],
    tools: [],
  });
  console.log(completion.choices[0]?.message?.content);
}

main();
