import os
import sys
from dotenv import load_dotenv
from langchain.llms.octoai_endpoint import OctoAIEndpoint
from langchain.memory import ConversationBufferMemory
from langchain import PromptTemplate, LLMChain

import time
from termios import tcflush, TCIFLUSH

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory
os.chdir(current_dir)

# Load environment variables
load_dotenv()


def handle_exit():
    """Print a goodbye message and exit the program."""
    print("\nGoodbye!\n")
    sys.exit(1)


def ask():
    """Interactively ask questions to the language model."""
    print("Loading...")

    # Set up the language model and predictor
    llm = OctoAIEndpoint(
        endpoint_url="https://text.octoai.run/v1/chat/completions",
        model_kwargs={
            "model": "mixtral-8x7b-instruct-fp16",
            "messages": [
                {
                    "role": "system",
                    "content": "Below is an instruction that describes a task. Write a response that appropriately completes the request.",
                }
            ],
            "stream": False,
            "max_tokens": 256,
        },
    )

    chat_history = ConversationBufferMemory(memory_key="chat_history")

    # Define a prompt template
    template = """
You are now the guide of a turn by turn adventure set on earth, in the year 2050.
The objective for the player of this adventure is to successfully land on planet Mars.
You must navigate them through challenges, choices, and consequences,
dynamically adapting the story based on the player's decisions.
Your goal is to create a branching narrative experience where each choice
leads to a new path, ultimately determining the player's fate.

Here are some rules to follow at all costs:
1. Be concise, wait at every turn for me to provide a human prompt
2. On the first turn, let the player chose one of 3 character classes
3. Always present the player 3 choices labeled A, B and C
4. Have a few paths that lead to success
5. Have some paths that lead to mission failure: in that case, conclude the text with: "The End.", I will search for this text to end the game
6. Reach success or failure after 3 turns

Here is the chat history, use this to understand what to say next: {chat_history}

Human: {human_input}
AI: """

    prompt = PromptTemplate(
        template=template,
        input_variables=["chat_history", "human_input"]
    )

    # Set up the language model chain
    llm_chain = LLMChain(
        prompt=prompt,
        llm=llm,
        memory=chat_history
    )

    # Clear the screen
    os.system("clear")

    print("Ready! Let's start the game by typing \"start\"!")
    print("Press Ctrl+C to exit\n")

    try:
        tcflush(sys.stdin, TCIFLUSH)
        while True:
            # Collect user's prompt
            user_prompt = input("\nPrompt: ")
            if user_prompt.lower() == "exit":
                handle_exit()

            # Generate and print the response
            start_time = time.time()

            response = llm_chain.predict(human_input=user_prompt)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"\nResponse({round(elapsed_time, 1)} sec): {response}")
            if "The End." in response:
                handle_exit()
    except KeyboardInterrupt:
        handle_exit()


if __name__ == "__main__":
    # This code is used to interactively ask questions to the language model.
    # It uses the OctoAI-hosted language model to generate responses.
    ask()