import requests
api_key = 'AIzaSyCNr4Mu6k9qPKIV-q9S-TzBGDF46cR5Ll4'
place_id = "ChIJ_bb5UY3MHkcRPFejsYcSLBE"
url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.status_code)
print(response.text)