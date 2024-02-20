# Docs summarization app

Comparing various OctoAI models and summarization methods for long text summarization.

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


