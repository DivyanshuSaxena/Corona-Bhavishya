import json
import requests

json_url = "https://v1.api.covindia.com/district-date-total-data"
response = requests.get(url=json_url)
data = response.json()

with open('../data/district-data.json', 'w', encoding='utf-8') as f:
  json.dump(data, f, ensure_ascii=False, indent=4)
