import os
import sys
from dotenv import load_dotenv
from langchain.llms.octoai_endpoint import OctoAIEndpoint
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
            "model": "llama-2-70b-chat-fp16",
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

    # Define a prompt template
    template = "{question}"
    prompt = PromptTemplate(template=template, input_variables=["question"])

    # Set up the language model chain
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    # Clear the screen
    os.system("clear")

    print("Ready! Let's start the conversation. Ask me anything!")
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

            response = llm_chain.invoke(user_prompt)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Response({round(elapsed_time, 1)} sec): {response}")
    except KeyboardInterrupt:
        handle_exit()


if __name__ == "__main__":
    # This code is used to interactively ask questions to the language model.
    # It uses the OctoAI-hosted language model to generate responses.
    ask()
