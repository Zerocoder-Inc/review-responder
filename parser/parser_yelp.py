import json
import time
import datetime
from utils.request import get_requests_handler, post_requests_handler
import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()


api_key = os.getenv("YELP_API_KEY")
server_url = os.getenv("SERVER_URL")
yelp_url_business_id = os.getenv("YELP_URL_BUSINESS_ID")
xano_get_yelp_reviews = os.getenv("XANO_GET_YELP_REVIEWS")
yelp_get_reviews = os.getenv("YELP_GET_REVIEWS")
xano_get_company = os.getenv("XANO_GET_COMPANY")
xano_post_add_review = os.getenv("XANO_POST_ADD_REVIEW")
xano_access_token = os.getenv("XANO_ACCESS_TOKEN")

params_for_xano = {
    'access_token': xano_access_token,
}


# get timestamp
def timestamp(str_time):
    time_obj = datetime.datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
    unix_time = time.mktime(time_obj.timetuple())
    return int(unix_time)


# Get business id
def get_business_id(business_name):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/graphql"
    }
    url = yelp_url_business_id.format(business_name=business_name)
    response = get_requests_handler(url=url, headers=headers)
    if response["status"] == "success":
        return {"status": "success", "business_id": json.loads(response["info"])["id"]}
    else:
        return {"status": response["status"], "info": response["info"]}


# get business name from link
def get_alias_by_link(link):
    if "yelp.com/biz/" in link:
        if link[-1] == "/":
            link = link[:len(link) - 1]
        return link.split("/")[-1]
    else:
        return False


def last_review_id(yelp_id):
    url = quote(xano_get_yelp_reviews.format(yelp_id=yelp_id, access_token=xano_access_token), safe='/:?=&')
    response = get_requests_handler(url=url, headers={})
    if response["status"] == "success":
        if response["info"] == '[]':
            return {"status": "success", "review_id": ""}
        review_id = json.loads(response["info"])[0]["review_id"]
        return {"status": "success", "review_id": review_id}

    else:
        return response


# get last reviews from yelp
def get_reviews(business_id,last_id=None):
    if last_id is None:
        last_id = last_review_id(business_id)
        if last_id["status"] != "success":
            return last_id
        last_id = last_id["review_id"]
    url = yelp_get_reviews.format(business_id=business_id)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/graphql"
    }

    response = get_requests_handler(url=url, headers=headers)

    if response["status"] == "success":
        data = json.loads(response["info"])
        new_reviews = []
        # sort by timestamp
        data["reviews"] = sorted(data["reviews"], key=lambda x: timestamp(x['time_created']), reverse=True)
        for review in data["reviews"]:
            if review["id"] == last_id:
                break
            else:
                new_reviews.append(review)

        if not new_reviews:
            return {"status": "success", "info": "no new reviews"}
        else:
            return {"status": "success", "info": "need update reviews", "reviews": new_reviews}
    else:
        return response


# method that will parse reviews for all companies and look for new ones
def parse_yelp():
    r"""
        1) we take the yelp id of all the companies that are from xano
        2) we get the latest review for each id and parse if there are any new ones
        3) if there are new ones, we add them to the database.

    """

    # link for get all company
    url = quote(xano_get_company.format(access_token=xano_access_token), safe='/:?=&')
    companies_ids = []
    response_companies = get_requests_handler(url=url, headers={})

    if response_companies["status"] == "success":
        for company in json.loads(response_companies["info"]):
            if company["yelp_id"]:
                res = get_reviews(company["yelp_id"])

                if res["status"] == "success":
                    if res["info"] == "need update reviews":
                        for review in res["reviews"]:
                            # link for add review
                            url = xano_post_add_review
                            headers = {
                                'accept': 'application/json',
                                'Content-Type': 'application/json',
                            }

                            json_data = {
                              "company_id": company["id"],
                              "timestamp": timestamp(review["time_created"]),
                              "text": review['text'],
                              "review_id": review['id'],
                              "yelp_id": company["yelp_id"],
                              "rating": review['rating'],
                              "user_name": review["user"]["name"],
                              "status": "new" if review["text"] != "" else "no text"
                            }
                            json_data.update(params_for_xano)
                            response = post_requests_handler(url=url, headers=headers, json=json_data)

                            if response["status"] == "success":
                                pass



# Request to graphql api with public response which should response full text of review
# For this we need fusion vip api

# -----------------------------------------------------------------
# graph_url = "https://api.yelp.com/v3/graphql"
#
# data = '''
# {
#   reviews(business: "M1JJfYM_exJE9lqTIWg7FA", limit: 20) {
#     total
#     review {
#       id
#       rating
#       text
#       public_response {
#         text
#       }
#       time_created
#       url
#     }
#   }
# }
#
# '''
#
# response = requests.post(graph_url, headers=headers, data=data)
#
# print(response.status_code)
# print(response.text)