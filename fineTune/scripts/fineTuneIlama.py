import os
import torch
from datasets import load_dataset
from transformers import LlamaForCausalLM, LlamaTokenizer, Trainer, TrainingArguments

# Load the text dataset
dataset = load_dataset('text', data_files={'train': 'datasets.json'})

# Load the LLaMA tokenizer and model
tokenizer = LlamaTokenizer.from_pretrained('path_to_llama_tokenizer')
model = LlamaForCausalLM.from_pretrained('path_to_llama_model')

# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples['text'], return_special_tokens_mask=False, truncation=True, padding=True)

tokenized_dataset = dataset.map(tokenize_function, batched=True, num_proc=4, remove_columns=['text'])

# Define training arguments and checkpointing strategy
output_dir = './llama_finetune_checkpoints'
training_args = TrainingArguments(
    output_dir=output_dir,                     # Output directory for model and checkpoints
    overwrite_output_dir=True,                 # Overwrite the content of the output directory
    num_train_epochs=3,                        # Number of training epochs
    per_device_train_batch_size=2,             # Batch size per GPU/CPU for training
    save_steps=500,                            # Save checkpoint every 500 steps
    save_total_limit=2,                        # Keep only the last two checkpoints
    logging_steps=100,                         # Log info every 100 steps
    save_strategy="steps",                     # Save by steps
    logging_dir=f'{output_dir}/logs',          # Log directory
    report_to="none",                          # Don't report to online platforms (Tensorboard, etc.)
    load_best_model_at_end=False,              # Disable loading the best model (not needed here)
    evaluation_strategy="no",                  # No evaluation during training
    fp16=True if torch.cuda.is_available() else False,  # Enable mixed precision if GPU is available
)

# Dynamic checkpoint naming function
def save_checkpoint_callback(trainer, output_dir):
    step = trainer.state.global_step
    checkpoint_dir = os.path.join(output_dir, f"checkpoint-{step}")
    trainer.save_model(checkpoint_dir)  # Save the model checkpoint
    print(f"Saved checkpoint at step {step}: {checkpoint_dir}")

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset['train'],
    tokenizer=tokenizer
)

# Train and dynamically save checkpoints
trainer.add_callback(save_checkpoint_callback)
trainer.train()

# Save the final model
model.save_pretrained(f"{output_dir}/final_model")
tokenizer.save_pretrained(f"{output_dir}/final_model")


