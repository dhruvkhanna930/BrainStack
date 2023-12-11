
import google.generativeai as palm
import os
from dotenv import load_dotenv

load_dotenv()
api_key_env = os.environ['CHATBOT_API_KEY']

palm.configure(api_key=api_key_env)


defaults = {
  'model': 'models/chat-bison-001',
  'temperature': 0.25,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
}

prompt = "How to make tea"
context = "Speak like a helper"
examples = []

response = palm.chat(
  **defaults,
  messages=prompt,
  context=context,
  examples=examples,
)
print(response.last) 