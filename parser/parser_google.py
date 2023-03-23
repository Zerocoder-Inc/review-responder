import googlemaps
import pandas as pd
import json

gmaps = googlemaps.Client(key='AIzaSyCNr4Mu6k9qPKIV-q9S-TzBGDF46cR5Ll4')
places_name = 'https://goo.gl/maps/Bpmp7uQe2oawPGEm9'
place_result = gmaps.places(places_name)
print(place_result)
# for i in range(0, len(place_result['results']))
# place_id = place_result['results'][0]['place_id']
# place = gmaps.place(place_id=place_id)
# place = place['result']['reviews']
# with open('response.json', 'w', encoding='utf-8') as file:
#     json.dump(place, file, ensure_ascii=False, indent=4)