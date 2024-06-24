# Structured Outputs Blog TK

This repository contains the necessary code to run and compare OctoAI Structured Generation with a DIY solution for converting product reviews to JSON payloads for JIRA. If you want to dive into more details about OctoAI's JSON mode/Structured Generation capabilities, check out [this blog post](https://octo.ai/blog/streamline-jira-ticket-creation-with-octoai-s-structured-outputs/).

Feel free to grab this code and an `OCTOAI_API_TOKEN`, and
build your LLM-powered applications today!


## Setup

Before running anything, please first install the necessary dependencies with `pip install -r requirements.txt` and make sure to specify your `OCTOAI_TOKEN` in the `.env` file.

## Dataset

The dataset used in this repository is [Amazon Reviews 2023](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023) from McAuley Lab. We specifically use `raw_meta_Magazine_Subscriptions` subsample for product descriptions and the `raw_review_Magazine_Subscriptions` subsample for corresponding product reviews.


## Running the demo

There are two similar files, `json_mode.py` and `no_json_mode.py`. Both will read the specified number of product descriptions, find the corresponding reviews, parse and group them by topic, and create JIRA ticket payloads. The JIRA REST API call is mocked, but the payload is valid.

Both scripts require most of the same parameters, provided via environment variables.

- `SAVE_BENCHMARK_RESULTS`: specifies the CSV file name where to store the benchmark results, like input and output token usage, number of retries, and so on. If empty, will not save the results to a file.
- `NUM_PRODUCTS`: number of products to process. This is not the number of unique reviews, but only of unique products. By default it's 5.
- `MODEL_NAME`: should be one of the supported OctoAI models. The supported models are: `mistral-7b-instruct`, `mixtral-8x7b-instruct`, `meta-llama-3-8b-instruct`, `meta-llama-3-70b-instruct`. The default value is `mistral-7b-instruct`.

Additionally, `no_json_mode.py` also has an additional environment variable `USE_PREFILL` to control whether to use a [prefilling prompt](https://docs.anthropic.com/en/docs/prefill-claudes-response) for the assistant response or not. If left empty, will not use prefilling. If set to one of these values: `1`, `yes`, `y`, `true` will enable prefilling.

Here's an example how to run `no_json_mode.py` using Meta Llama 3 8B parameter model, with prefilling enabled, process 10 products, and save the benchmark results into `llama_8b_no_json.csv`.

```bash
MODEL_NAME=meta-llama-3-8b-instruct USE_PREFILL=1 NUM_PRODUCTS=10 SAVE_BENCHMARK_RESULTS=llama_8b_no_json.csv python no_json_mode.py
```
