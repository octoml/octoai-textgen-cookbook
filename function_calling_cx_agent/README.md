# Function Calling for Customer Support Agent

This repository contains the necessary code to run the OctoAI Function Calling with a DIY solution for converting product reviews to JSON payloads for JIRA and interacting with the customer that posted the review. If you want to dive into more details about OctoAI's Function Calling capabilities, check out [this blog post](...).

Feel free to grab this code and an `OCTOAI_API_TOKEN`, and
build your LLM-powered applications today!


## Setup

Before running anything, please first install the necessary dependencies with `pip install -r requirements.txt` and make sure to specify your `OCTOAI_TOKEN` in the `.env` file.

## Dataset

The dataset used in this repository is [Amazon Reviews 2023](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023) from McAuley Lab. We specifically use `raw_meta_Magazine_Subscriptions` subsample for product descriptions and the `raw_review_Magazine_Subscriptions` subsample for corresponding product reviews.


## Running the demo

See `agent.py` file. It will read the specified number of product descriptions, find the corresponding reviews, parse and group them by topic, and depending on the review it may thank the customer, ask for clarifications, or apologize and create a JIRA ticket. The JIRA REST API call is mocked, but the payload is valid.

Both scripts require most of the same parameters, provided via environment variables.

- `NUM_PRODUCTS`: number of products to process. This is not the number of unique reviews, but only of unique products. By default it's 5.
- `MODEL_NAME`: should be one of the supported OctoAI models. The supported models are: `mistral-7b-instruct`, `mixtral-8x7b-instruct`, `meta-llama-3-8b-instruct`, `meta-llama-3-70b-instruct`. The default value is `mistral-7b-instruct`.


Here's an example how to run `agent.py` using Meta Llama 3 8B parameter model and process the reviews from 10 products.

```bash
MODEL_NAME=meta-llama-3-8b-instruct NUM_PRODUCTS=10 python agent.py
```
