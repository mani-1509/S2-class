import requests
import time

# Configuration
API_KEY = "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"  # Replace with your HuggingFace API key
API_URL = "https://api-inference.huggingface.co/models/Qwen/QwQ-32B-Preview"

# Function to generate chatbot responses
def generate_response(prompt, retries=5, delay=15):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "do_sample": True,
            "temperature": 0.7,
            "top_p": 0.9,
            "repetition_penalty": 1.5,
        },
    }

    for attempt in range(retries):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)

            if response.status_code == 200:
                result = response.json()
                # Validate and clean output
                if isinstance(result, list) and "generated_text" in result[0]:
                    # Extract chatbot response after 'ChatBot:'
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
