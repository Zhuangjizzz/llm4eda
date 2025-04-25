# -*- coding: utf-8 -*-
import os
import wandb
from transformers import Trainer, TrainingArguments, DataCollatorForLanguageModeling
from model import get_model
from dataset import get_dataset_and_tokenizer

# trainer.py: Launch training and evaluate after training

# Set WandB to offline mode
os.environ["WANDB_MODE"] = "offline"
# HF_DATASETS_CACHE should be set externally via env variable

# Initialize WandB
wandb.init(
    project="gpt2-small-train",
    name="bookcorpus-bsz2-epoch3",
    config={
        "model": "GPT2-small",
        "dataset": "small",
        "epochs": 5,
        "batch_size": 2
    }
)

print("[DEBUG] Start training script")
checkpoint_dir = "./logs/checkpoint-last"
resume_ckpt = checkpoint_dir if os.path.exists(checkpoint_dir) else None
if resume_ckpt:
    print(f"[DEBUG] Found checkpoint: {resume_ckpt}. Will resume.")
else:
    print("[DEBUG] No checkpoint found. Training will start from scratch.")

# Load tokenizer and datasets
tokenizer, train_dataset, val_dataset = get_dataset_and_tokenizer(
    dataset_name="small",
    dataset_path="/home/jzhuang/Desktop/llm4eda/hw1_llm_training/small-117M/",
    val_split=0.05,
    block_size=128,
    debug=True
)

print(f"[DEBUG] Train blocks: {len(train_dataset)}, Val blocks: {len(val_dataset)}")

# Build the model
model = get_model(vocab_size=tokenizer.vocab_size)
print(f"[DEBUG] Model initialized with vocab_size={tokenizer.vocab_size}")

# Training arguments (no built-in evaluation)
training_args = TrainingArguments(
    output_dir="./logs",
    overwrite_output_dir=False,
    num_train_epochs=5,
    per_device_train_batch_size=2,
    learning_rate=5e-5,
    weight_decay=0.01,
    warmup_steps=500,
    save_steps=500,
    save_total_limit=3,
    logging_steps=100,
    fp16=True,
    report_to="wandb",
)
print(f"[DEBUG] TrainingArguments: {training_args}")

# Data collator
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Trainer (no eval_dataset)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
)
print("[DEBUG] Trainer initialized")

# Start training
if resume_ckpt:
    print(f"[DEBUG] Training resumed from {resume_ckpt}")
    trainer.train(resume_from_checkpoint=resume_ckpt)
else:
    print("[DEBUG] Training from scratch")
    trainer.train()

# Save final model
trainer.save_model("./logs/final_model")
print("[DEBUG] Training complete. Model saved to ./logs/final_model")

# Evaluate on validation set after training
print("[DEBUG] Evaluating on validation set...")
eval_results = trainer.evaluate(eval_dataset=val_dataset)
print(f"[DEBUG] Validation results: {eval_results}")
