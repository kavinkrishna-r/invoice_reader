import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

key=os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=key)
for m in genai.list_models():
    print(m.name)
