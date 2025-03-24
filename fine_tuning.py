# fine_tuning.py
import os
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset

MODEL_NAME = "dbmdz/bert-base-turkish-cased"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def load_data(dataset_path):
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"❌ Dosya bulunamadı: {dataset_path}")
    dataset = load_dataset("json", data_files={"train": dataset_path, "test": dataset_path})
    return dataset

def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=512)

def fine_tune_model(dataset_path="training_data.jsonl", output_dir="./fine_tuned_model"):
    dataset = load_data(dataset_path)
    dataset = dataset.map(tokenize_function, batched=True)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
    training_args = TrainingArguments(
        output_dir=output_dir,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=3,
        weight_decay=0.01,
        logging_dir="./logs",
        logging_steps=10,
        fp16=torch.cuda.is_available()
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["test"],
        tokenizer=tokenizer
    )
    trainer.train()
    trainer.save_model(output_dir)
    return "✅ Model eğitildi ve kaydedildi!"

def predict_text(text, model_path="./fine_tuned_model"):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ Model bulunamadı: {model_path}")
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=1).item()
    return f"🧠 Tahmin Sonucu: {prediction}"