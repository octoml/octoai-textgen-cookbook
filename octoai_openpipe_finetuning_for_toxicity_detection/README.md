# Toxicity classification at 125x lower costs and better-than-GPT 4 quality, with fine-tuneed Mistral 7B

This repository contains the necessary code to collect a dataset from GPT-4 responses and then to evaluate a fine-tuned model against various OctoAI and OpenAI models. If you want to check out the cost efficiency gains from fine-tuning, check out [this blog post](...).

Feel free to grab this code and an `OCTOAI_API_TOKEN`, and
build your LLM-powered applications today!


## Setup

Before running anything, please first install the necessary dependencies with `pip install -r requirements.txt` and make sure to specify your `OCTOAI_TOKEN`, `OPENAI_API_KEY`, and `OPENPIPE_API_KEY` in the `.env` file.

## Dataset

The dataset used in this repository is a LMSys ToxicChat, but for fine-tuning we use the GPT-4 annotations instead of the provided human labels. Also, it includes not only human annotated toxic/non-toxic user queries, but also various jailbreaking attempts. This is especially interesting because it allows to test the performance of the toxicity detection models when faced with jailbreaking prompts.


## Running data collection

To collect a dataset of GPT-4 responses, execute the following command in your terminal:
```bash
python collect_classify_toxic_text.py -m [gpt4, gpt3.5, openpipe:some-previously-tuned-model] --ds-offset 0 --ds-max-size 100
```

Once you have collected the dataset, please follow the instructions on how to tune the model on OpenPipe, available in [this blog post](https://octo.ai/blog/what-you-need-to-know-about-fine-tuning-llm-models/).

## Running evaluation

To evaluate your model, execute the following command in your terminal:
```bash
python evaluate_classify_toxic_text.py -m [gpt4, gpt3.5, openpipe:some-previously-tuned-model, mistral-7b, mixtral-8x7b, llamaguard] --eval-file eval_outputs.jsonl
```

Note that you can also evaluate against "base"/"not tuned" models from OctoAI and OpenAI too.

`LlamaGuard` is not available yet for this benchmark, but soon will become available.


## Appendix A: `classification_report` results for various models


```
GPT4 scores
              precision    recall  f1-score   nr. of samples

   not toxic       0.70      1.00      0.82        16
       toxic       1.00      0.50      0.67        14

    accuracy                           0.77        30
   macro avg       0.85      0.75      0.74        30
weighted avg       0.84      0.77      0.75        30
```

---

```
Contender model (gpt-3.5-turbo) scores
              precision    recall  f1-score   support

   not toxic       0.85      0.69      0.76        16
       toxic       0.67      0.83      0.74        12

    accuracy                           0.75        28
   macro avg       0.76      0.76      0.75        28
weighted avg       0.77      0.75      0.75        28
```

---

```
Contender model (openpipe:toxicity-100-gpt4-prune) scores
              precision    recall  f1-score   support

   not toxic       0.70      0.88      0.78        16
       toxic       0.80      0.57      0.67        14

    accuracy                           0.73        30
   macro avg       0.75      0.72      0.72        30
weighted avg       0.75      0.73      0.73        30
```

---

```
Contender model (openpipe:toxicity-100-gpt4-noprune) scores
              precision    recall  f1-score   support

   not toxic       0.75      0.94      0.83        16
       toxic       0.90      0.64      0.75        14

    accuracy                           0.80        30
   macro avg       0.82      0.79      0.79        30
weighted avg       0.82      0.80      0.79        30
```

---

**Note**: Mistral and Mixtral both follow the instructions very poorly and are prone to jailbreaking
```
Contender model (mistral-7b-instruct) scores
              precision    recall  f1-score   support

   not toxic       0.57      1.00      0.73        12
       toxic       0.00      0.00      0.00         9

    accuracy                           0.57        21
   macro avg       0.29      0.50      0.36        21
weighted avg       0.33      0.57      0.42        21
```

---

```
Contender model (mixtral-8x7b-instruct) scores
              precision    recall  f1-score   support

   not toxic       0.50      1.00      0.67        10
       toxic       0.00      0.00      0.00        10

    accuracy                           0.50        20
   macro avg       0.25      0.50      0.33        20
weighted avg       0.25      0.50      0.33        20
```


