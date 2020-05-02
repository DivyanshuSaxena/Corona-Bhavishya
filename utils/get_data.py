import json
import requests

def get_district_data():
  json_url = "https://v1.api.covindia.com/district-date-total-data"
  response = requests.get(url=json_url)
  data = response.json()

  with open('../data/district-data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

def get_state_data():
  json_url = "https://v1.api.covindia.com/state-date-total-data"
  response = requests.get(url=json_url)
  data = response.json()

  with open('../data/state-data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
  get_district_data()
  get_state_data()