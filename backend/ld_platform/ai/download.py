import os
import logging

from transformers import AutoTokenizer, AutoModelForSequenceClassification

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.info("Checking if models exist...")

    base_model_path = os.environ["BASE_MODEL_PATH"]
    model_name = os.environ["HUGGING_FACE_CRYPTO_DEBERTA_MODEL_NAME"]
    auth_token = os.environ["HUGGING_FACE_CRYPTO_DEBERTA_AUTH_TOKEN"]

    model_save_path = os.path.join(base_model_path, model_name)

    # TODO: Automatically download the new models
    if not os.path.exists(os.path.join(model_save_path, "tokenizer_config.json")):
        logger.info("Starting downloading a tokenizer..." )
        tokenizer = AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=model_name, use_auth_token=auth_token
        )
        tokenizer.save_pretrained(model_save_path)

    if not os.path.exists(os.path.join(model_save_path, "config.json")):
        logger.info("Starting downloading a model..." )
        model = AutoModelForSequenceClassification.from_pretrained(
            pretrained_model_name_or_path=model_name,
            use_auth_token=auth_token,
            num_labels=3,
        )
        model.save_pretrained(model_save_path)
