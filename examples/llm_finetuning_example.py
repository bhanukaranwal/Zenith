import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, TaskType


def main():
    print("Zenith LLM Fine-tuning Example with LoRA")
    print("=" * 50)
    
    model_name = "gpt2"
    print(f"\nLoading base model: {model_name}")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=8,
        lora_alpha=32,
        lora_dropout=0.1,
        target_modules=["c_attn"]
    )
    
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    print("\nLoading dataset...")
    dataset = load_dataset("wikitext", "wikitext-2-raw-v1", split="train[:1000]")
    
    def tokenize_function(examples):
        return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=128)
    
    tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=["text"])
    
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=1,
        per_device_train_batch_size=4,
        save_steps=100,
        logging_steps=10,
        learning_rate=2e-4
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
    )
    
    print("\nStarting fine-tuning...")
    trainer.train()
    
    print("\nFine-tuning completed!")
    print("Model saved to ./results")


if __name__ == "__main__":
    main()
