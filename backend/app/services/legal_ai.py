from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Load once on first import
tokenizer = AutoTokenizer.from_pretrained("app/ai_model/fine_tuned")
model = AutoModelForSeq2SeqLM.from_pretrained("app/ai_model/fine_tuned")

def get_legal_explanation(text: str) -> str:
    try:
        input_ids = tokenizer(
            f"Explain this legal text: {text}",
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).input_ids

        output = model.generate(input_ids, max_new_tokens=256)
        explanation = tokenizer.decode(output[0], skip_special_tokens=True)

        return explanation
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"
