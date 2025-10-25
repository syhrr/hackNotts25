import os
from dotenv import load_dotenv
load_dotenv()
print("here is ur key:",os.getenv("OPENAI_API_KEY"))
