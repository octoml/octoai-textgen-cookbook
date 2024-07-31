import OpenAI from 'openai'; // Assuming openai SDK is imported
import { ChatCompletionMessageParam, ChatCompletionTool } from 'openai/resources/chat';


export function greenOutput(message: string) {
    console.log(`\x1b[32m${message}\x1b[0m`);
  }

export function blueOutput(message: string) {
    console.log(`\x1b[34m${message}\x1b[0m`);
  }


export function redOutput(message: string) {
    console.log(`\x1b[31m${message}\x1b[0m`);
  }

// Define a type for the weather function's parameters for better type checking
export interface WeatherFunctionParams {
  location: string;
  unit: 'celsius' | 'fahrenheit';
}

// Function to simulate fetching weather information
export async function getCurrentWeather(params: WeatherFunctionParams): Promise<string> {
  // Simulate an API call to get weather
  // Placeholder response with dynamic temperature based on unit
  const temperature = params.unit === 'celsius' ? '24°C' : '75°F';
  return `sunny with a high of ${temperature}.`;
}

export interface searchWebParams {
    query: string;
    }
function searchWeb(params: searchWebParams) {
    return {
      "result": "Avogadro's number is 6.022 x 10^23",
    };
  }

export interface calculatorParams {
    expression: string;
    }
function calculator(params: calculatorParams) {
    return {
      "comment": 'calculating 4 * 6.022 x 10^23',
      "result": 24.088e23,
    };
  }


// Function to handle tool messages
export async function handleToolMessage(toolName: string, parameters: string): Promise<string|any> {
  switch (toolName) {
    case 'getCurrentWeather':
      const jsonObject = JSON.parse(parameters);
      const weather_params: WeatherFunctionParams = jsonObject as WeatherFunctionParams;
      greenOutput(`** Fetching weather for ${weather_params.location} in ${weather_params.unit}`);
      return getCurrentWeather(weather_params);
    case 'searchWeb':
        const searchWebParams = JSON.parse(parameters);
        const search_params: searchWebParams = searchWebParams as searchWebParams;
        greenOutput(`** Searching the web for: ${search_params.query}`);
        return searchWeb(search_params);
    case 'calculator':
        const calculatorParams = JSON.parse(parameters);
        const calc_params: calculatorParams = calculatorParams as calculatorParams;
        greenOutput(`** Calculating: ${calc_params.expression}`);
        return calculator(calc_params);

    default:
      return `No handler for tool ${toolName}`;
  }
}

// Function to issue request to llm
export async function getLlmResponse(messages: Array<ChatCompletionMessageParam>, tools: Array<ChatCompletionTool>, model: string = "meta-llama-3.1-8b-instruct", llm: OpenAI): Promise<any> {
  const response = await llm.chat.completions.create({
    model: model,
    messages: messages,
    tools: tools,
    tool_choice: "auto",
  });
  return response;
}

export async function logToolResponse(messages: Array<ChatCompletionMessageParam>, response: any, id: string) {
  let content_string = response instanceof Object ? JSON.stringify(response) : response;
  messages.push({"role": "tool", "content":  content_string, "tool_call_id": id});
}

export async function multiTurn(model_name: string, messages: Array<ChatCompletionMessageParam>, tools: Array<ChatCompletionTool>, llm: OpenAI) {
    blueOutput(`Model: ${model_name}\nLast user question:`)
    // Find and print the most likely user message for this request in messages:
    let i = messages.length - 1;
    while (messages[i].role != "user") {
        i--;
    }
    console.log(`${messages[i]["content"]}`);
    let response = await getLlmResponse(messages, tools, model_name, llm);
    let new_message = response.choices[0].message;

    // OctoAI specific fix:
    new_message.content = new_message.content == null ? "" : new_message.content;

    // Record the first response from LLM
    messages.push(response.choices[0].message);

    if (response.choices[0].message.tool_calls != null) {
      let tool_calls = response.choices[0].message.tool_calls

      for (let i = 0; i < tool_calls.length; i++) {
        let tool_call = tool_calls[i];
        let tool_response = await handleToolMessage(tool_call.function.name, tool_call.function.arguments);
        await logToolResponse(messages, tool_response, tool_call.id);
      }
    }

    response = await getLlmResponse(messages, tools, model_name, llm);
    messages.push(response.choices[0].message);
    blueOutput(`Final answer:`)
    // console.log(messages);
    // console.log(response.choices[0].message);
    console.log(response.choices[0].message.content);
    console.log("--------------------------------------------------")
    return messages;
  }
