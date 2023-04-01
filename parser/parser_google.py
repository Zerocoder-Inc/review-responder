import requests
import json
from utils.request import get_requests_handler, post_requests_handler
import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
xano_get_google_reviews = os.getenv("XANO_GET_GOOGLE_REVIEWS")
google_get_reviews = os.getenv("GOOGLE_GET_REVIEWS")
xano_post_add_review = os.getenv("XANO_POST_ADD_REVIEW")
xano_get_company = os.getenv("XANO_GET_COMPANY")
xano_post_add_company = os.getenv("XANO_POST_ADD_COMPANY")
xano_access_token = os.getenv("XANO_ACCESS_TOKEN")

params_for_xano = {
    'access_token': xano_access_token,
}


def get_reviews(cid, company_id):
    xano = xano_get_google_reviews.format(cid=cid, access_token=xano_access_token)
    url = google_get_reviews.format(cid=cid, api_key=api_key)
    arr = []
    resp = get_requests_handler(url=xano, params=params_for_xano)

    if resp["status"] == "success":
        resp = json.loads(resp["info"])

        for key in resp:
            arr.append(key['timestamp'])
        response = get_requests_handler(url=url)

        if response["status"] == "success":
            response = json.loads(response["info"])['result']['reviews']
            for key in response:

                if key['time'] in arr:
                    pass
                else:
                    xano = xano_post_add_review
                    obj = {"timestamp": key['time'],
                           "google_cid": cid,
                           "text": key["text"],
                           "rating": key["rating"],
                           "user_name": key["author_name"],
                           "company_id": company_id,
                           "status": "new" if key["text"] != "" else "no text"
                           }
                    obj.update(params_for_xano)
                    requests.post(xano, json=obj)


def post_company(url):
    xano = xano_get_company.format(access_token=xano_access_token)
    # we get the cid from the link and convert it to Hexadecimal - this is the format of the cid in Google
    cid = int(url.split(":")[-1][0:url.split(":")[-1].find("!")], 16)
    companies = get_requests_handler(url=xano, headers={})
    if companies["status"] == "success":
        companies = json.loads(companies["info"])
        arr = []
        get_url = google_get_reviews.format(cid=cid, api_key=api_key)
        id = get_requests_handler(url=get_url)
        if id["status"] == "success":
            id = json.loads(id["info"])['result']['place_id']
            for key in companies:
                arr.append(key['google_cid'])
            if str(cid) in arr:
                pass
            else:
                xano = xano_post_add_company
                obj = {'google_link': url, 'google_cid': cid, 'company_google_id': id}
                obj.update(params_for_xano)
                res = post_requests_handler(url=xano, json=obj)
                if res["status"] == "success":
                    pass
            return cid


def parse_google():
    # link for get all company

    url = xano_get_company.format(access_token=xano_access_token)
    response_companies = get_requests_handler(url=url, params=params_for_xano)

    # get all google companies, parse reviews and add if there are new ones
    if response_companies["status"] == "success":
        for company in json.loads(response_companies["info"]):

            if company["google_cid"]:
                get_reviews(company["google_cid"], company["id"])

