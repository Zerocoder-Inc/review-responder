from langchain.llms import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

llm = OpenAI(model_name='text-davinci-003', n=2, best_of=2)
print(llm('Create me python script for gpt 3.5 turbo and simple ask answer model'))