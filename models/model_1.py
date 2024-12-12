import requests
import time

# Configuration
API_KEY = "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"  
API_URL = "https://api-inference.huggingface.co/models/Qwen/QwQ-32B-Preview"

def generate_response(prompt, retries=5, delay=15):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    role_description = (
        "You are an expert chatbot assistant named 'InfoBot'. "
        "You can provide detailed, clear, and concise answers on a wide variety of topics, "
        "including science, technology, history, and current events. "
        "You respond in a funny , friendly and helpful tone."
    )
    payload = {
        "inputs":f"{role_description}\nUser: {prompt}\nChatBot:",
        "parameters": {
            "do_sample": True,
            "temperature": 0.5,
            "top_p": 0.9,
            "repetition_penalty": 1.5,
        },
    }

    for attempt in range(retries):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)

            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and "generated_text" in result[0]:
                    bot_response = result[0]["generated_text"].split("ChatBot:")[-1].strip()
                    return bot_response if bot_response else "I’m sorry, I couldn’t generate a response."

                return "Unexpected response format from the model."

            elif response.status_code in [503, 500]:
                print(f"Model busy. Retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})")
                time.sleep(delay)

            else:
                return f"Error {response.status_code}: {response.text}"

        except Exception as e:
            return f"An error occurred: {str(e)}"

    return "Sorry, I’m having trouble responding right now."
