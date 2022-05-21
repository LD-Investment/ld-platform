import logging

import environ
import torch
from torch import nn
from transformers import AutoTokenizer, AutoModelForSequenceClassification

env = environ.Env()

logger = logging.getLogger(__name__)


class CryptoDeberta:
    def __init__(self):
        # informative
        self.name = "crypto_deberta"
        self.detail = "Crypto DeBerta is AI model developed by LD Investment"

        # load models
        logger.info("Loading CryptoDeberta AI model...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=env("HUGGING_FACE_CRYPTO_DEBERTA_MODEL_NAME"),
            use_auth_token=env("HUGGING_FACE_CRYPTO_DEBERTA_AUTH_TOKEN"))
        self.model = AutoModelForSequenceClassification.from_pretrained(
            pretrained_model_name_or_path=env("HUGGING_FACE_CRYPTO_DEBERTA_MODEL_NAME"),
            use_auth_token=env("HUGGING_FACE_CRYPTO_DEBERTA_AUTH_TOKEN"),
            num_labels=3)
        self.model.eval()
        logger.info("Initialized CryptoDeberta AI model!")

    def calculate(self, title: str, content: str):
        """
        return: (bull, neutral, bear)jui
        """
        m = nn.Softmax(dim=1)
        inputs = self.tokenizer(title, content, return_tensors="pt")

        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = m(logits)
            probs = probs.detach().cpu().numpy().flatten()
        return probs
