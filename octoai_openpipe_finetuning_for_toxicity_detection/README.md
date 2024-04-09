# Toxicity classifier datasets
1. https://huggingface.co/datasets/lmsys/toxic-chat
2. https://huggingface.co/datasets/google/jigsaw_toxicity_pred
3. https://huggingface.co/datasets/OxAISH-AL-LLM/wiki_toxic (may be redundant with 2)
4. https://huggingface.co/datasets/unalignment/toxic-dpo-v0.2


# TODO:
- [v] Fine-tune Mistral to serve as toxicity classifier
  * [v] Use 50 samples
  * [v] Use 100 samples
- [wip] Include a subsample of hard examples
- [wip] Include a subsample of jailbreaking examples
- [v] Evaluate (precision/recall/accuracy/f1) against base mistral -> Hosted on OctoAI
- [v] Evaluate (precision/recall/accuracy/f1) against base mixtral -> Hosted on OctoAI
- [v] Evaluate (precision/recall/accuracy/f1) against gpt3.5
- [v] Evaluate (precision/recall/accuracy/f1) against gpt4
- [x] Evaluate (precision/recall/accuracy/f1) against llamaguard - https://octoai.cloud/text/chat?model=llamaguard-7b&mode=api


# On a side-note, some feedback for OpenPipe folks
- Absolutely zero information about why my training run failed!! How am I supposed to fix it if I have no clue what went wrong
- Not having the ability to save filtering rules is very annoying
- Can't stop the training of a model once started, don't know if deletion will help
- Would be helpful to be able to edit tags from UI
- Limited view for training, don't like it - I'd like to be reasured that you do it right, otherwise I'd prefer to train myself
- Filtering on the size of input/output tokens would be helpful


https://app.openpipe.ai/p/ofZ0kyrpYH/request-logs
https://platform.openai.com/usage








```
GPT4 scores
              precision    recall  f1-score   nr. of samples

   not toxic       0.70      1.00      0.82        16
       toxic       1.00      0.50      0.67        14

    accuracy                           0.77        30
   macro avg       0.85      0.75      0.74        30
weighted avg       0.84      0.77      0.75        30
```

```
Contender model (gpt-3.5-turbo) scores
              precision    recall  f1-score   support

   not toxic       0.85      0.69      0.76        16
       toxic       0.67      0.83      0.74        12

    accuracy                           0.75        28
   macro avg       0.76      0.76      0.75        28
weighted avg       0.77      0.75      0.75        28
```

```
Contender model (openpipe:toxicity-100-gpt4-prune) scores
              precision    recall  f1-score   support

   not toxic       0.70      0.88      0.78        16
       toxic       0.80      0.57      0.67        14

    accuracy                           0.73        30
   macro avg       0.75      0.72      0.72        30
weighted avg       0.75      0.73      0.73        30
```

```
Contender model (openpipe:toxicity-100-gpt4-noprune) scores
              precision    recall  f1-score   support

   not toxic       0.75      0.94      0.83        16
       toxic       0.90      0.64      0.75        14

    accuracy                           0.80        30
   macro avg       0.82      0.79      0.79        30
weighted avg       0.82      0.80      0.79        30
```

Mistral and Mixtral both follow the instructions very poorly and are prone to jailbreaking
```
Contender model (mistral-7b-instruct) scores
              precision    recall  f1-score   support

   not toxic       0.57      1.00      0.73        12
       toxic       0.00      0.00      0.00         9

    accuracy                           0.57        21
   macro avg       0.29      0.50      0.36        21
weighted avg       0.33      0.57      0.42        21
```

```
Contender model (mixtral-8x7b-instruct) scores
              precision    recall  f1-score   support

   not toxic       0.50      1.00      0.67        10
       toxic       0.00      0.00      0.00        10

    accuracy                           0.50        20
   macro avg       0.25      0.50      0.33        20
weighted avg       0.25      0.50      0.33        20
```