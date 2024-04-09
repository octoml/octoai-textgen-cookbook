# Text summarization with OctoAI

Comparing various OctoAI models and summarization methods for long text summarization. If you want to check out the cost efficiency gains with OctoAI, check out [this blog post](https://octo.ai/blog/reduce-llm-costs-for-text-summarization-by-over-50-percent-with-mixtral-on-octoai/).

This repository implements three of the most popular summarization methods in an easy to follow way.

- Map-Reduce summarization
- Refined summarization
- Summarization with reranking

Feel free to grab this code and an `OCTOAI_API_TOKEN`, and 
build your LLM-powered applications today!

## Setup

Before running anything, please first install the necessary dependencies with `pip install -r requirements.txt` and make sure to specify your `OCTOAI_TOKEN` in the `.env` file.

## Benchmark

To run the benchmark, execute
```bash
python summarization_methods_app.py --use_model [mixtral, mistral, llama2, nous-hermes] --use_method [map-reduce, refine, rerank] --docs_path <relative or absolute path to your directory with pdfs>
```

## Interactive application

To run the Gradio app, execute
```bash
python summarization_methods_app.py --as_gradio_app
```


