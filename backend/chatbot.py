import openai
import os
import traceback
from openai import OpenAI

client = OpenAI()

# Ensure your OpenAI API key is loaded from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_diagnosis(user_input, conversation_history):
    """
    Generates a response using the updated OpenAI Chat API.
    """
    baseString="Assume you are doctor. Answer the below question in short simple english and if you get any query other than medical field then don't reply \n"
    # Prepare the conversation in the format required by the API
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    messages.extend({"role": "user", "content": msg} for msg in conversation_history)
    messages.append({"role": "user", "content": baseString+user_input})

    try:
        # Call the OpenAI Chat API
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        # Access the content attribute directly
        response_text = completion.choices[0].message.content

        return response_text

    except Exception as e:
        print("Error during API call:", e)
        traceback.print_exc()  # Print the full stack trace
        return "I'm sorry, but I encountered an error."
