# Docs summarization app

Comparing the cost-efficiency of OpenAI and OctoAI models.

Before running anything, please first install the necessary dependencies with `pip install -r requirements.txt` and make sure to specify your `OCTOAI_TOKEN` and `OPENAI_API_KEY` in the `.env` file.

## Benchmark

To run the benchmark, execute
```bash
python contract_summarizer_harness.py --use_model [gpt4, gpt3.5, gpt3.5-new, mixtral, mistral, llama2, nous-hermes] --docs_path <relative or absolute path to your directory with pdfs>
```

## Interactive application

To run the Gradio app, execute
```bash
python contract_summarizer_harness.py --as_gradio_app
```


