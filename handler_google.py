import time
import json
from chat_gpt.chat_gpt import responses_from_ai
import os
from dotenv import load_dotenv
from urllib.parse import quote
from utils.request import get_requests_handler, post_requests_handler

load_dotenv()

xano_access_token = os.getenv("XANO_ACCESS_TOKEN")
xano_get_reviews = os.getenv("XANO_GET_REVIEWS")
xano_add_responses = os.getenv("XANO_ADD_RESPONSES")

params_for_xano = {
    'access_token': xano_access_token,
}


while True:
    url = quote(xano_get_reviews.format(access_token=xano_access_token), safe='/:?=&')
    response_companies = get_requests_handler(url=url)
    if response_companies["status"] == "success":
        for review in json.loads(response_companies["info"]):
            if review["google_cid"]:
                if review["status"] == "new":
                    responses = responses_from_ai(review)
                    json_data = {
                      "company_id": review["company_id"],
                      "review_id": review["id"],
                      "status": "new",
                      "responses": [
                            {
                              "id": 0,
                              "response": responses[0]
                            },
                            {
                              "id": 1,
                              "response": responses[1]
                            },
                          {
                              "id": 2,
                              "response": responses[2]
                          },
                          ]
                    }
                    json_data.update(params_for_xano)
                    res = post_requests_handler(url=xano_add_responses, json=json_data)
                    if res["status"] == "success":
                        pass
                        # send sms
                        # update status

    time.sleep(60)