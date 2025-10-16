import sys
import os

# Add project root to the path to allow imports from src
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Check if the key is loaded
if not os.getenv("OPENAI_API_KEY"):
    print("ERROR: OPENAI_API_KEY is not set. Please create a .env file in the project root and add your key.")
    print("Example .env file content:")
    print("OPENAI_API_KEY=\"sk-xxxxxxxxxxxxxxxxxxxxxxxx\"")
    sys.exit(1)

from src.tools.laravel_assistant import laravel_5_6_assistant

query = "Laravel make:configの使い方を教えて。日本語で答えて"

print(f"--- Calling Tool with Query: \"{query}\" ---")

# Access the wrapped function using .fn
response = laravel_5_6_assistant.fn(query=query)

print("\n--- AI Assistant Response ---")
print(response)
