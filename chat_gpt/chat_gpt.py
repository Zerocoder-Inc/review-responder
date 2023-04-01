import requests
import json
import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import StringPromptTemplate
from pydantic import BaseModel
from utils.request import get_requests_handler
from urllib.parse import quote
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
xano_access_token = os.getenv('XANO_ACCESS_TOKEN')
xano_get_responses = os.getenv('XANO_GET_RESPONSES')
xano_get_quiz_answers = os.getenv("XANO_GET_QUIZ_ANSWERS")
xano_get_reviews = os.getenv("XANO_GET_REVIEWS")
xano_get_sms = os.getenv('XANO_GET_SMS')


class FunctionExplainerPromptTemplate(StringPromptTemplate, BaseModel):
    # def validate_input_variables(cls, v):
    #     """ Validate that the input variables are correct. """
    #     if len(v) != 1 or "function_name" not in v:
    #         raise ValueError("function_name must be the only input_variable.")
    #     return v

    def format(self, sms, answers, review) -> str:
        # Get the source code of the function

        # Generate the prompt to be sent to the language model
        prompt = f"""
        Imagine that you are the owner of the establishment, give a response to the review.
        The nature of the response: {answers}
        Your last reply: {sms}
        Feedback to be answered: {review}
        """
        return prompt

    def _prompt_type(self):
        return "function-explainer"

    def data_collector(new_review):
        '''
        {
        "id": 14,
        "created_at": 1680267235234,
        "timestamp": 1679905523,
        "company_google_id": "",
        "text": "Needed a water heater replaced in our multi-unit building. During the work, we identified the other water heater was also leaking and likely to fail in the...",
        "review_id": "L_Xf0EnIp-P65MB4CAUq_A",
        "yelp_id": "M1JJfYM_exJE9lqTIWg7FA",
        "rating": "5",
        "user_name": "Craig D.",
        "google_cid": "",
        "status": "",
        "company_id": 6
        }
        '''
        company_id = new_review['company_id']
        xano_sms = quote(xano_get_sms.format(access_token=xano_access_token), safe='/:?=&')
        response = get_requests_handler(url=xano_sms)

        if response["status"] == "success":
            resp = json.loads(response['info'])
            sms = []
            for key in resp:
                if company_id == key['company_id']:
                    sms.append(key)
                else:
                    pass
            # response = json.loads(response["info"])
            # print(response)
            # responses = []
            # for key in response:
            #     if company_id == key['company_id']:
            #         responses.append(key)
            #     else:
            #         pass
            xano_qa = quote(xano_get_quiz_answers.format(access_token=xano_access_token), safe='/:?=&')
            answers = []
            # resp = json.loads(requests.get(xano_qa).text)
            resp = get_requests_handler(url=xano_qa)
            if resp["status"] == "success":
                resp = json.loads(resp["info"])
                for key in resp:

                    if company_id == key['company_id']:
                        answers.append(key['answer'])
                    else:
                        pass

                review = new_review['text']

                return sms[-1]['response_text'], answers, review



def requests_gpt(api_key, promt):
    llm = OpenAI(openai_api_key=api_key, temperature=0.7)
    answers = []
    for result in range(3):
        answers.append(llm(promt))
    return answers


def responses_from_ai(new_review):
    fn_explainer = FunctionExplainerPromptTemplate
    sms, answers, review = fn_explainer.data_collector(new_review=new_review)
    return requests_gpt(api_key=api_key,
                 promt=fn_explainer.format(self=fn_explainer,review=review, answers=answers, sms=sms))


