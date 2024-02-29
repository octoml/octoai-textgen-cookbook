# TK
import logging
import os
import glob
import time
import sys
from dotenv import load_dotenv
from octoai.client import Client
import tiktoken

from langchain_community.document_loaders import UnstructuredPDFLoader
from transformers import AutoTokenizer


load_dotenv()

SYSTEM_PROMPT = "You are a helpful financial and accounting specialist assistant. You will summarize any given document into 10 bullet points. Please note that your work will be reviewed, if done right, you will get a 100 USD performance bonus per summary."

# NOTE: The prices are up to date as of end of February 2024
COSTS = {"mixtral": {"input": 0.0003, "output": 0.0005},
         "nous-hermes": {"input": 0.0003, "output": 0.0005},
         "mistral": {"input": 0.0001, "output": 0.00025},
         "llama2": {"input": 0.0006, "output": 0.0019}}


class AbstractOctoAIModel:
    def __init__(self, model_name, system_prompt=None):
        self.system_prompt = system_prompt or SYSTEM_PROMPT
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
        max_size = self.ctx_window_size - self.get_num_tokens(self.system_prompt) - self.params["max_tokens"] - 100
        current_size = self.get_num_tokens(text)

        n_chunks = current_size // max_size + 1

        text_tokens = self.tokenizer.encode(text)

        for idx in range(n_chunks):
            yield self.tokenizer.decode(text_tokens[idx * max_size: (idx + 1) * max_size], skip_special_tokens=True)

    def get_num_tokens(self, text):
        return len(self.tokenizer.encode(text))
    
    def is_longer_than_ctx_window(self, text):
        return self.get_num_tokens(text) > self.ctx_window_size - self.get_num_tokens(self.system_prompt) - self.params["max_tokens"] - 100

    def get_completions(self, user_prompt):
        raise NotImplementedError()


class OctoAIRefinerSummarizer(AbstractOctoAIModel):
    def get_completions(self, user_prompt):
        if self.is_longer_than_ctx_window(user_prompt):
            current_chunk = next(self.chunk_text_iter(user_prompt))

            chunk_summary = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt,
                    },
                    {
                        "role": "user",
                        "content": current_chunk
                    }
                ],
                **self.params
            )

            while True:
                user_prompt = f"Summary so far:\n{chunk_summary.choices[0].message.content}\nText: {user_prompt[len(current_chunk):]}"
                current_chunk = next(self.chunk_text_iter(user_prompt))

                next_chunk_summary = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": self.system_prompt,
                        },
                        {
                            "role": "user",
                            "content": current_chunk
                        }
                    ],
                    **self.params
                )

                next_chunk_summary.usage.prompt_tokens += chunk_summary.usage.prompt_tokens
                next_chunk_summary.usage.completion_tokens += chunk_summary.usage.completion_tokens
                next_chunk_summary.usage.total_tokens += chunk_summary.usage.total_tokens

                chunk_summary = next_chunk_summary

                if not self.is_longer_than_ctx_window(user_prompt):
                    break


            return chunk_summary
        else:
            completions = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                **self.params
            )

            return completions


class OctoAIMapReduceSummarizer(AbstractOctoAIModel):
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
                        "content": self.system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                **self.params
            )

            return completions


class OctoAIMapReduceFinalRerankerSummarizer(AbstractOctoAIModel):
    def get_completions(self, user_prompt, is_final=False):
        if self.is_longer_than_ctx_window(user_prompt):
            completions = []
            for chunk in self.chunk_text_iter(user_prompt):
                completions.append(self.get_completions(chunk))

            final_completion = self.get_completions("\n".join(comp.choices[0].message.content for comp in completions), is_final=True)
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
                        "content": self.system_prompt if not is_final else ("You are a helpful financial and accounting specialist assistant."
                                    " You will pick the top 10 most important items from the given list of bullet points."
                                    " Please note that your work will be reviewed, if done right, you will get a 100 USD performance bonus."),
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                **self.params
            )

            return completions


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
                "nous-hermes-2-mixtral": "nous-hermes"
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


if __name__ == "__main__":  
    import argparse

    model_choices = ["llama2", "mixtral", "mistral", "nous-hermes"]
    method_choices = ["map-reduce", "refine", "rerank"]

    parser = argparse.ArgumentParser()
    parser.add_argument("--use_model", choices=model_choices)
    parser.add_argument("--use_method", choices=method_choices)
    parser.add_argument("--docs_path", type=str)

    parser.add_argument("--as_gradio_app", action="store_true")
    args = parser.parse_args()

    if not args.as_gradio_app:
        if args.use_method == "map-reduce":
            octo_model = OctoAIMapReduceSummarizer(args.use_model)
        elif args.use_method == "rerank":
            octo_model = OctoAIMapReduceFinalRerankerSummarizer(args.use_model)
        elif args.use_method == "refine":
            octo_model = OctoAIRefinerSummarizer(args.use_model)
        else:
            raise ValueError("Invalid summarization method was provided, was expecting one of ['map-reduce', 'refine', 'rerank'], but got:", args.use_method)

        for doc_name in glob.glob(os.path.join(args.docs_path, "*.pdf")):
            document = load_parse_pdf(doc_name)
            stats, summary = benchmark_one(document, doc_name, octo_model)
            print(stats)
            print("Summarization cost:", total_cost(stats), "USD")
            print("-*--*-" * 12)
    else:
        import gradio as gr


        def compare_models(doc_name, octo_model_name, summarization_method_pick):
            document = load_parse_pdf(doc_name)
            if summarization_method_pick == "map-reduce":
                octo_model = OctoAIMapReduceSummarizer(octo_model_name)
            elif summarization_method_pick == "rerank":
                octo_model = OctoAIMapReduceFinalRerankerSummarizer(octo_model_name)
            elif summarization_method_pick == "refine":
                octo_model = OctoAIRefinerSummarizer(octo_model_name)
            else:
                raise ValueError("Invalid summarization method was provided, was expecting one of ['map-reduce', 'refine', 'rerank'], but got:", summarization_method_pick)
            octo_stats, octo_summary = benchmark_one(document, doc_name, octo_model)

            return octo_summary, as_html_spec(octo_stats)


        with gr.Blocks() as demo:
            gr.Markdown("# Text summarization with OctoAI")
            gr.Markdown("Comparing the cost-efficiency of various long-text summarization methods with OctoAI.")
            document_content = gr.File()

            octoai_model_pick = gr.Dropdown(value="mixtral-8x7b", label="OctoAI Model", show_label=True, choices=["llama2-70b", "mixtral-8x7b", "mistral-7b-v0.2", "nous-hermes-2-mixtral"])
            summarization_method_pick = gr.Dropdown(value="map-reduce", label="Summarization Method", show_label=True, choices=method_choices)

            summarize_btn = gr.Button(value="Summarize")

            with gr.Row():
                with gr.Column():
                    octoai_summary = gr.Text(label="OctoAI Summary", show_label=True)
                with gr.Column():
                    octoai_stats = gr.HTML(label="OctoAI Stats", show_label=True)

            summarize_btn.click(compare_models, [document_content, octoai_model_pick, summarization_method_pick], [octoai_summary, octoai_stats])

        demo.launch()
