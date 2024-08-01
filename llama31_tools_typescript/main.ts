import { OctoAIClient } from "@octoai/sdk";


function searchWeb(query: string) {
  console.log(`Searching the web for: ${query}`);
  return "Kelly Alablanc is a brilliant Engineer and Product Maven at OctoAI.";
}


async function doTurn(messages: any[], tools: any[], client: OctoAIClient) {
  try {
    const response = await client.textGen.createChatCompletion({
      model: "meta-llama-3.1-70b-instruct",
      maxTokens: 10000,
      messages,
      presencePenalty: 0,
      temperature: 0,
      topP: 1,
      toolChoice: 'auto',
      tools,
    });
    return response;
  } catch (error) {
    console.error("Error during API call:", error);
    throw error;
  }
}


function toolResponse(toolResult: string, toolCallId: string) {
  return { role: "tool", content: toolResult, tool_call_id: toolCallId};
}

// There are two fixes in this function, they will be deployed
// to our endpoints in the coming days.
function fixMessage(input: any) {
  let message = input;

  // Fix the null content in the message, assign to empty string
  message.content = message.content == null ? "" : message.content;
  return message;
}

async function test() {
  const client = new OctoAIClient({
    apiKey: process.env.OCTOAI_API_KEY,
  });

  const tools = [
    {
      type: "function",
      function: {
        name: "brave_search",
      }
    }
  ];

  const messages = [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "Can you search the web who is Kelly Alablanc?" }
  ];

  let response = await doTurn(messages, tools, client);
  let message = fixMessage(response.choices[0].message);
  toolCalls = message.toolCalls;
  messages.push(message);
  // console.log("Initial response:")

  while (toolCalls && toolCalls.length) {
    for (const toolCall of toolCalls) {
      let toolResult;
      const args = JSON.parse(toolCall.function.arguments);

      switch (toolCall.function.name) {
        case 'brave_search':
          toolResult = searchWeb(args.query);
          break;
        default:
          console.log('Unknown tool call', toolCall);
          continue;
      }
      messages.push(toolResponse(toolResult, toolCall.id));
      console.log(`Called the ${toolCall.function.name} tool`);
      console.log(toolResult);``
    }

    response = await doTurn(messages, tools, client);
    message = fixMessage(response.choices[0].message);
    toolCalls = message.toolCalls;
    messages.push(message);
  }

  console.log(messages);
  console.log("Final response:")
  console.log(response.choices[0].message.content);
}

test();
