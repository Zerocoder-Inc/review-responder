import time
import requests
import json


def get_reviews(api_key, cid):
    xano = "https://xxmt-33mi-qlwk.n7.xano.io/api:u3yroEiZ/reviews"
    url = f"https://maps.googleapis.com/maps/api/place/details/json?cid={cid}&key={api_key}&reviews_sort=newest&reviews_no_translations=true"
    payload = {}
    headers = {}
    arr = []
    resp = json.loads(requests.get(xano).text)
    for key in resp:
        arr.append(key['timestamp'])
    response = requests.get(url, headers=headers, data=payload)
    response = json.loads(response.text)['result']['reviews']
    for key in response:
        print(key)
        if key['time'] in arr:
            pass
        else:
            xano = "https://xxmt-33mi-qlwk.n7.xano.io/api:u3yroEiZ/reviews"
            obj = {"timestamp": key['time'], "company_id": cid, "review": key["text"]}
            requests.post(xano, json=obj)
        # print(key['time'])



def cid_from_url(url):
    xano = 'https://xxmt-33mi-qlwk.n7.xano.io/api:u3yroEiZ/company'

    cid = int(url.split(":")[-1][0:url.split(":")[-1].find("!")], 16)
    companies = json.loads(requests.get(xano).text)
    arr = []
    for key in companies:
        arr.append(key['google_id'])

    if str(cid) in arr:
        pass
    else:
        xano = 'https://xxmt-33mi-qlwk.n7.xano.io/api:u3yroEiZ/company'
        obj = {'yalp_link': '', 'google_link': url, 'yalp_id': '', 'google_id': cid, 'company_id': cid}
        requests.post(xano, json=obj)
    return cid


def main():
    api_key = 'AIzaSyCNr4Mu6k9qPKIV-q9S-TzBGDF46cR5Ll4'
    url = 'https://www.google.com/maps/place/Vapiano/@52.2280939,21.0057561,17z/data=!3m1!4b1!4m6!3m5!1s0x471ecc8d51f9b6fd:0x112c1287b1a3573c!8m2!3d52.2280939!4d21.0057561!16s%2Fg%2F119vj0k32'
    # cid_from_url(url)
    get_reviews(api_key=api_key, cid=cid_from_url(url))


if __name__ == '__main__':
    time_start = time.time()
    main()
    print(f'All time {time.time() - time_start}')
