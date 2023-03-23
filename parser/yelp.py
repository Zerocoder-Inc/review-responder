import requests
import json
import time
import datetime

api_key = "CYVE2spiKx1ePaM5kw4uunPYH_NoIe6nqy8qF2jUsjdTaqeVl6pTP9NhtTfhggRhwEQ87AjD1v6Nrc26WhQScqNPnbPm6AgRBcu9WbnYDNCmQuXeVPeKIDvZ0sUZZHYx"


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
    url = f"https://api.yelp.com/v3/businesses/{business_name}"

    response = requests.get(url, headers=headers)
    return json.loads(response.text)["id"]


# get business name from link
def get_name_by_link(link):
    return link.split("/")[-1]

# get last review from yelp
def get_reviews(business_id):
    url = f"https://api.yelp.com/v3/businesses/{business_id}/reviews?limit=20&sort_by=newest"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/graphql"
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    time_created = []

    for review in data["reviews"]:
        time_created.append(timestamp(review["time_created"]))
    # get the last review because even if you specify the newest in API, the reviews are still mixed
    last_review_num = time_created.index(max(time_created))
    url = data["reviews"][last_review_num]["url"]
    text = data["reviews"][last_review_num]["text"]
    rating = data["reviews"][last_review_num]["rating"]
    time_created = data["reviews"][last_review_num]["time_created"]
    name = data["reviews"][last_review_num]["user"]["name"]
    return url, text, rating, time_created, name


def main():
    link = "https://www.yelp.com/biz/general-sf-san-francisco-2"
    buss_id = get_business_id(get_name_by_link(link))
    get_reviews(buss_id)


if __name__ == "__main__":
    main()


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
