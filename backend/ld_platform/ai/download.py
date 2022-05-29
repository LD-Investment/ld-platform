import os
import logging

from transformers import AutoTokenizer, AutoModelForSequenceClassification

BASE_MODEL_PATH = "/models"
# FIXME: AUTH_TOKEN should be read from .envs/.local/.ai
AUTH_TOKEN = "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"
CRYPTODEBERTA_MODEL_NAME = "CryptoModel/cryptodeberta-base-all-finetuned"

model_save_path = os.path.join(BASE_MODEL_PATH, CRYPTODEBERTA_MODEL_NAME)

# TODO: Automatically download the new models
if not os.path.exists(os.path.join(model_save_path, "tokenizer_config.json")):
    tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path=CRYPTODEBERTA_MODEL_NAME, use_auth_token=AUTH_TOKEN
    )
    tokenizer.save_pretrained(model_save_path)

if not os.path.exists(os.path.join(model_save_path, "config.json")):
    model = AutoModelForSequenceClassification.from_pretrained(
        pretrained_model_name_or_path=CRYPTODEBERTA_MODEL_NAME,
        use_auth_token=AUTH_TOKEN,
        num_labels=3,
    )
    model.save_pretrained(model_save_path)
