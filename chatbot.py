import openai

openai.api_key = "your_openai_api_key"

def get_diagnosis(user_input):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Diagnose based on the following symptoms: {user_input}",
        max_tokens=100
    )
    return response.choices[0].text.strip()
