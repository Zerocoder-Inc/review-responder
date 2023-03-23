import openai
import os
from dotenv import load_dotenv

load_dotenv()


def get_responses():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    def get_answers():
        array = []
        for i in range(1,4):
            response = openai.Completion.create(
                model="text-davinci-003",
                # PROMT - field for entering a request
                prompt='5 plus 5',  
                temperature=0.7,
                max_tokens=500,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            array.append(response['choices'][0]['text'])
        trigger = input('''If you want to close generation, write - 1.
If you want to continue generation, write - 0.
Anser - ''')
        if trigger == 1:
            get_answers()
        elif trigger == 0:
            return array
    responses = get_answers()
    return responses

print(get_responses())
        
            
        