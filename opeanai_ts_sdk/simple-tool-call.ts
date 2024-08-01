import OpenAI from 'openai';
import { ChatCompletionMessageParam, ChatCompletionTool } from 'openai/resources/chat';

// The following are support functions defined in ./utils.ts
// WeatherFunctionParams: a class to help parse the parameters for the weather function
// getCurrentWeather: a function to simulate fetching weather information
// getLlmResponse: a function to issue a request to the LLM
// logToolResponse: a function to append tool messages to the message history
import { WeatherFunctionParams, getCurrentWeather, getLlmResponse, logToolResponse } from './utils';

// Main function to run a full round-trip of function calling.
async function main(messages: Array<ChatCompletionMessageParam> , tools: Array<ChatCompletionTool>, model_name: string) {
  // Create client
  const llm = new OpenAI({
    baseURL: 'https://text.octoai.run/v1',
    apiKey: process.env.OCTOAI_API_KEY
  });

  // Get first response from LLM
  let response = await getLlmResponse(messages, tools, model_name, llm);
  let new_message = response.choices[0].message;

  // OctoAI specific fix:
  new_message.content = new_message.content == null ? "" : new_message.content;
  messages.push(new_message);

  // Handle tool calls in message
  if (response.choices[0].message.tool_calls != null) {
    console.log("Tool calls detected:")
    let tool_calls = response.choices[0].message.tool_calls

    for (let i = 0; i < tool_calls.length; i++) {
      let tool_call = tool_calls[i];
      const jsonObject = JSON.parse(tool_call.function.arguments);
      const params: WeatherFunctionParams = jsonObject as WeatherFunctionParams;
      console.log(`** Fetching weather for ${params.location} in ${params.unit}`);
      let tool_response = await getCurrentWeather(params);
      await logToolResponse(messages, tool_response, tool_call.id);
    }
  }

  // Get final response from LLM
  response = await getLlmResponse(messages, tools, model_name, llm);
  console.log("Final answer:");
  console.log(response.choices[0].message.content);
}

// Define the model name, messages and tools
const model_name = "meta-llama-3.1-8b-instruct"
let messages: Array<ChatCompletionMessageParam> = [{ "role": "user", "content": "What's the weather like in Boston today?" }];
const tools: Array<ChatCompletionTool> = [
    {
      "type": "function",
      "function": {
        "name": "getCurrentWeather",
        "description": "Get the current weather in a given location",
        "parameters": {
          "type": "object",
          "properties": {
            // Define properties for location and unit
            "location": {
              "type": "string",
              "description": "The location to get the weather for"
            },
            "unit": {
              "type": "string",
              "enum": ["celsius", "fahrenheit"],
              "description": "The unit of temperature (Celsius or Fahrenheit)"
            }
          },
          "required": ["location", "unit"]
        }
      }
    }
  ];

main(messages, tools, model_name);
