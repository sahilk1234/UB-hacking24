# chatbot.py

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load the pretrained model and tokenizer
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def get_diagnosis(user_input, conversation_history):
    """
    Generates a diagnosis or response based on user input and conversation history.
    Concatenates the conversation history with the current input for context.
    """
    # Concatenate the conversation history and the new user input
    full_input = " ".join(conversation_history + [user_input])
    
    # Tokenize the concatenated input and generate a response
    inputs = tokenizer.encode(full_input, return_tensors="pt")
    
    # Generate a response from the model
    with torch.no_grad():
        outputs = model.generate(inputs, max_length=200, num_return_sequences=1, no_repeat_ngram_size=2)

    # Decode the generated response
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return response_text
