# https://docs.google.com/spreadsheets/d/1xdXB6KAzzXNl7fjlO-_LDWVMJfJiVMTFWM51mNRLUFw/edit#gid=0
import logging
import os
import glob
import time
import sys
from dotenv import load_dotenv
from octoai.client import Client
from openai import OpenAI
import tiktoken

from langchain_community.document_loaders import UnstructuredPDFLoader
from transformers import AutoTokenizer


load_dotenv()

SYSTEM_PROMPT = "You are a helpful financial and accounting specialist assistant. You will summarize any given document into 10 bullet points. Please note that your work will be reviewed, if done right, you will get a 100 USD performance bonus per summary."

# NOTE: The prices are up to date as of end of February 2024
COSTS = {"gpt3.5-new": {"input": 0.0005, "output": 0.0015},
         "gpt3.5": {"input": 0.001, "output": 0.002},
         "mixtral": {"input": 0.0003, "output": 0.0005},
         "nous-hermes": {"input": 0.0003, "output": 0.0005},
         "gpt4": {"input": 0.01, "output": 0.03},
         "mistral": {"input": 0.0001, "output": 0.00025},
         "llama2": {"input": 0.0006, "output": 0.0019}}


class AbstactModel:
    def __init__(self):
        self.client = NotImplemented
        self.slug_model_name = NotImplemented
        self.model_name = NotImplemented
        self.ctx_window_size = NotImplemented
        self.params = {
                "temperature": NotImplemented,
                "presence_penalty": NotImplemented,
                "top_p": NotImplemented,
                "stream": NotImplemented,
                "max_tokens": NotImplemented,
            }
        self.tokenizer = NotImplemented
    
    def chunk_text_iter(self, text):
        raise NotImplementedError()

    def get_num_tokens(self, text):
        return len(self.tokenizer.encode(text))
    
    def is_longer_than_ctx_window(self, text):
        return self.get_num_tokens(text) > self.ctx_window_size - self.get_num_tokens(SYSTEM_PROMPT) - self.params["max_tokens"] - 100

    def get_completions(self, user_prompt):
        if self.is_longer_than_ctx_window(user_prompt):
            completions = []
            for chunk in self.chunk_text_iter(user_prompt):
                completions.append(self.get_completions(chunk))

            final_completion = self.get_completions("\n".join(comp.choices[0].message.content for comp in completions))
            final_completion.usage.prompt_tokens += sum(comp.usage.prompt_tokens for comp in completions)
            final_completion.usage.completion_tokens += sum(comp.usage.completion_tokens for comp in completions)
            final_completion.usage.total_tokens += sum(comp.usage.total_tokens for comp in completions)
            return final_completion
        else:
            completions = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                **self.params
            )

            return completions


class OpenAIModel(AbstactModel):
    def __init__(self, model_name) -> None:
        self.client = OpenAI()
        self.slug_model_name = model_name
        self.ctx_window_size = 16385
        self.params = {
                "temperature": 0.75,
                "presence_penalty": 1,
                "top_p": 0.9,
                "stream": False,
                "max_tokens": 512,
            }
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        if self.slug_model_name == "gpt3.5":
            self.model_name = "gpt-3.5-turbo-1106"
            self.ctx_window_size = 16385
        if self.slug_model_name == "gpt3.5-new":
            self.model_name = "gpt-3.5-turbo-0125"
            self.ctx_window_size = 16385
        elif self.slug_model_name == "gpt4":
            self.model_name = "gpt-4-turbo"
            self.ctx_window_size = 128000

    def chunk_text_iter(self, text):
        max_size = self.ctx_window_size - self.get_num_tokens(SYSTEM_PROMPT) - self.params["max_tokens"] - 100
        current_size = self.get_num_tokens(text)

        n_chunks = current_size // max_size + 1

        text_tokens = self.tokenizer.encode(text)

        for idx in range(n_chunks):
            yield self.tokenizer.decode(text_tokens[idx * max_size: (idx + 1) * max_size])


class OctoAIModel(AbstactModel):
    def __init__(self, model_name) -> None:
        self.client = Client()
        self.slug_model_name = model_name
        self.params = {
                "temperature": 0.75,
                "presence_penalty": 1,
                "top_p": 0.9,
                "stream": False,
                "max_tokens": 512,
            }
        
        if self.slug_model_name.startswith("mixtral"):
            self.model_name = "mixtral-8x7b-instruct-fp16"
            self.tokenizer = AutoTokenizer.from_pretrained("mistralai/Mixtral-8x7B-Instruct-v0.1")
            self.ctx_window_size = 32768
        elif self.slug_model_name.startswith("mistral"):
            self.model_name = "mistral-7b-instruct-fp16"
            self.tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
            self.ctx_window_size = 32768
        elif self.slug_model_name.startswith("llama2"):
            self.model_name = "llama-2-70b-chat-fp16"
            self.tokenizer = AutoTokenizer.from_pretrained("NousResearch/Llama-2-70b-chat-hf")
            self.ctx_window_size = 4096
        elif self.slug_model_name.startswith("nous-hermes"):
            self.model_name = "nous-hermes-2-mixtral-8x7b-dpo-fp16"
            self.tokenizer = AutoTokenizer.from_pretrained("mistralai/Mixtral-8x7B-Instruct-v0.1")
            self.ctx_window_size = 32768

    def chunk_text_iter(self, text):
        max_size = self.ctx_window_size - self.get_num_tokens(SYSTEM_PROMPT) - self.params["max_tokens"] - 100
        current_size = self.get_num_tokens(text)

        n_chunks = current_size // max_size + 1

        text_tokens = self.tokenizer.encode(text)

        for idx in range(n_chunks):
            yield self.tokenizer.decode(text_tokens[idx * max_size: (idx + 1) * max_size], skip_special_tokens=True)


def load_parse_pdf(filename):
    loader = UnstructuredPDFLoader(filename)
    data = loader.load()
    return data[0].page_content


def benchmark_one(document, doc_name, model):
    doc_input_tokens = model.get_num_tokens(document)
    print(f"Loaded {doc_name} of size {doc_input_tokens} tokens")

    start_time = time.perf_counter()
    completions = model.get_completions(document)
    time_spent_seconds = time.perf_counter() - start_time
    response = completions.choices[0].message.content

    return {"num_input_tokens": completions.usage.prompt_tokens,
                    "time_to_summarize_seconds": time_spent_seconds,
                    "num_output_tokens": completions.usage.completion_tokens,
                    "input_text_len": len(document),
                    "model_name": model.slug_model_name,
                    "ctx_window_size": model.ctx_window_size}, response

def total_cost(stats_dict):
    model_name_mapper = {
                "mixtral": "mixtral",
                "mistral": "mistral",
                "llama2": "llama2",
                "nous-hermes": "nous-hermes",
                "llama2-70b": "llama2",
                "mixtral-8x7b": "mixtral",
                "mistral-7b-v0.2": "mistral",
                "nous-hermes-2-mixtral": "nous-hermes",
                "gpt3.5": "gpt3.5",
                "gpt3.5-new": "gpt3.5-new",
                "gpt4": "gpt4"
            }
    return (stats_dict['num_input_tokens'] * COSTS[ model_name_mapper[stats_dict['model_name']] ]['input'] / 1000
           + stats_dict['num_output_tokens'] * COSTS[ model_name_mapper[stats_dict['model_name']] ]['output'] / 1000)


def as_html_spec(stats_dict):
    # make html table
    return f"""
    <table>
      <tr>
        <th># input tokens</th>
        <th># output tokens</th>
        <th>Total cost</th>
      </tr>
      <tr>
        <td>{stats_dict['num_input_tokens']}</td>
        <td>{stats_dict['num_output_tokens']}</td>
        <td>{total_cost(stats_dict):0.5f} USD</td>
      </tr>
    </table>
    """

def as_html_diff_summary(lhs_stats_dict, rhs_stats_dict):
    return f"<h2>OctoAI would cost {total_cost(rhs_stats_dict) / total_cost(lhs_stats_dict):0.3f}x less than OpenAI.</h2>"


if __name__ == "__main__":  
    import argparse

    model_choices = ["gpt4", "gpt3.5", "gpt3.5-new", "llama2", "mixtral", "mistral", "nous-hermes"]

    parser = argparse.ArgumentParser()
    parser.add_argument("--use_model", choices=model_choices)
    parser.add_argument("--docs_path", type=str)

    parser.add_argument("--as_gradio_app", action="store_true")
    args = parser.parse_args()

    if not args.as_gradio_app:
        use_oai = True if args.use_model.startswith("gpt") else False
        model = OpenAIModel(args.use_model) if use_oai else OctoAIModel(args.use_model)

        for doc_name in glob.glob(os.path.join(args.docs_path, "*.pdf")):
            document = load_parse_pdf(doc_name)
            stats, summary = benchmark_one(document, doc_name, model)
            print(stats)
            print("Summarization cost:", total_cost(stats), "USD")
            print("-*--*-" * 12)
    else:
        import gradio as gr


        def compare_models(doc_name, octo_model_name, openai_model_name):
            document = load_parse_pdf(doc_name)
            octo_model = OctoAIModel(octo_model_name)
            octo_stats, octo_summary = benchmark_one(document, doc_name, octo_model)

            openai_model = OpenAIModel(openai_model_name)
            openai_stats, openai_summary = benchmark_one(document, doc_name, openai_model)

            return octo_summary, openai_summary, as_html_spec(octo_stats), as_html_spec(openai_stats), as_html_diff_summary(octo_stats, openai_stats)

        
        with gr.Blocks() as demo:
            gr.Markdown("# Docs summarization app")
            gr.Markdown("Comparing the cost-efficiency of OpenAI and OctoAI.")
            document_content = gr.File()

            octoai_model_pick = gr.Dropdown(value="mixtral-8x7b", label="OctoAI Model", show_label=True, choices=["llama2-70b", "mixtral-8x7b", "mistral-7b-v0.2", "nous-hermes-2-mixtral"])
            openai_model_pick = gr.Dropdown(value="gpt3.5", label="OpenAI Model", show_label=True, choices=["gpt4", "gpt3.5-new", "gpt3.5"])

            summarize_btn = gr.Button(value="Summarize")

            with gr.Row():
                with gr.Column():
                    octoai_summary = gr.Text(label="OctoAI Summary", show_label=True)
                    octoai_stats = gr.HTML(label="OctoAI Stats", show_label=True)

                with gr.Column():
                    openai_summary = gr.Text(label="OpenAI Summary", show_label=True)
                    openai_stats = gr.HTML(label="OpenAI Stats", show_label=True)
            
            stats_diff = gr.HTML(label="Stats Diff")

            summarize_btn.click(compare_models, [document_content, octoai_model_pick, openai_model_pick], [octoai_summary, openai_summary, octoai_stats, openai_stats, stats_diff])

        demo.launch()
