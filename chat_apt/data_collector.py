import openai
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


class Data:
    """
    Class for databases responses
    """

    def __init__(self, quiz, company, company_id, last_responses):
        self.quiz = quiz
        self.company = company
        self.company_id = company_id
        self.last_responses = last_responses

# def get_quiz():
#     URL = 'https://x8ki-letl-twmt.n7.xano.io/api:DcstfPN7/quiz'
#     quiz = requests.get(url=URL)
#     quiz = json.loads(quiz.text)
#     answers = []
#     for item in quiz:
#         answers.append(item['answer'])
#     print(answers)

# get responses: https://x8ki-letl-twmt.n7.xano.io/api:DcstfPN7/responses
# get responses_id: https://x8ki-letl-twmt.n7.xano.io/api:DcstfPN7/responses/{responses_id}



def last_responses():
    URL = 'https://x8ki-letl-twmt.n7.xano.io/api:DcstfPN7/responses'
    arr = []
    company_id = None
    responses = requests.get(URL)
    responses = json.loads(responses.text)
    for items in responses:
        if items['company_id'] == '456':
            arr.append(items)
    print(arr)
last_responses()