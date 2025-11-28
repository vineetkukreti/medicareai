import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("Testing all available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Testing {m.name}...")
            try:
                model = genai.GenerativeModel(m.name)
                response = model.generate_content("Hello")
                print(f"SUCCESS with {m.name}")
                print(f"Response: {response.text}")
                break
            except Exception as e:
                print(f"FAILED {m.name}: {e}")
except Exception as e:
    print(f"Error listing models: {e}")
