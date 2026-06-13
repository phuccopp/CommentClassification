# predict.py

import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

# ==========================================================
# CONFIG
# ==========================================================

MODEL_PATH = "./model_phobert"

LABELS = [
    "design_negative",
    "design_neutral",
    "design_positive",
    "experience_negative",
    "experience_neutral",
    "experience_positive",
    "irrelevant"
]

# ==========================================================
# LOAD MODEL
# ==========================================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Loading model...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH
)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)

model.to(device)
model.eval()

print("Model loaded!")
print("Device:", device)

# ==========================================================
# PREDICT BATCH
# ==========================================================

def predict_batch(
    texts,
    threshold=0.5,
    batch_size=32
):
    """
    texts: list[str]

    return:
    [
        ["design_positive"],
        ["experience_negative"],
        ...
    ]
    """

    all_results = []

    for i in range(
        0,
        len(texts),
        batch_size
    ):

        batch_texts = texts[
            i:i+batch_size
        ]

        inputs = tokenizer(
            batch_texts,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=256
        )

        inputs = {
            k: v.to(device)
            for k, v in inputs.items()
        }

        with torch.no_grad():

            outputs = model(**inputs)

            probs = torch.sigmoid(
                outputs.logits
            ).cpu().numpy()

        for row in probs:

            labels = [
                LABELS[idx]
                for idx, score in enumerate(row)
                if score > threshold
            ]

            all_results.append(
                labels
            )

    return all_results

# ==========================================================
# PREDICT ONE TEXT
# ==========================================================

def predict(text):

    result = predict_batch(
        [text]
    )

    return result[0]

# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    while True:

        text = input(
            "\nNhập comment: "
        )

        labels = predict(text)

        print(
            "Prediction:",
            labels
        )