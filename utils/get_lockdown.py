"""Expose the API for getting the district lockdown level"""
import os
import json
from datetime import datetime as dt

script_dir = os.path.dirname(os.path.abspath(__file__))
lockdown_json = os.path.join(script_dir, './lockdown.json')
date_format = '%d/%m/%Y'


def get_district_lockdown(district, date):
  """Get the lockdown level for the district on the given date

  Arguments:
      district {String} -- District Name
      date {String} -- DD/MM/YYYY

  Returns:
      Integer -- {0, 1, 2, 3, 4, 5}
  """
  with open(lockdown_json) as f:
    lockdown_data = json.load(f)

  query_date = dt.strptime(date, date_format)
  prev_level = 0
  for start_date, data in lockdown_data.items():
    if query_date < dt.strptime(start_date, date_format):
      return prev_level
    if district in data:
      prev_level = data[district]
    if 'Nation' in data:
      prev_level = data['Nation']

  return prev_level


def get_lockdown_history(district):
  """Get the lockdown history of a district

  Arguments:
      district {String}

  Returns:
      List -- [(date, level), (date, level), ..., (date, level)]
  """
  with open(lockdown_json) as f:
    lockdown_data = json.load(f)

  district_data = []
  for start_date, data in lockdown_data.items():
    if district in data:
      district_data.append((start_date, data[district]))
    if 'Nation' in data:
      district_data.append((start_date, data['Nation']))

  return district_data


def get_lockdown_series(district, start_date, num_days=-1):
  """Get the time series of lockdown levels for a district

  Arguments:
      district {String}
      start_date {String} -- DD/MM/YYYY

  Keyword Arguments:
      num_days {int} -- Number of days from the start date (default: {-1})

  Returns:
      List -- List of lockdown levels. Length = num_days
  """
  district_history = get_lockdown_history(district)

  ret_list = []
  prev_level = 0
  prev_date = dt.strptime(start_date, date_format)
  for obj in district_history:
    curr_date = dt.strptime(obj[0], date_format)

    # Count number of days between previous date in lockdown history and current
    # date. Append the previous lockdown level for all intervening dates.
    if prev_date <= curr_date:
      days = (curr_date - prev_date).days
      for _in in range(days):
        ret_list.append(prev_level)

      # Update prev date and prev level
      prev_level = obj[1]
      prev_date = curr_date
    else:
      # Update prev level
      prev_level = obj[1]

    if num_days != -1 and len(ret_list) >= num_days:
      ret_list = ret_list[:num_days]
      break

  present_date = dt.today()
  days_till_today = (present_date - prev_date).days
  for _in in range(days_till_today):
    ret_list.append(prev_level)
  if num_days != -1 and len(ret_list) >= num_days:
    ret_list = ret_list[:num_days]

  return ret_list


if __name__ == '__main__':
  d = get_lockdown_history('Bangalore')
  print(d)
  level = get_district_lockdown('Delhi', '11/05/2020')
  print(level)
  s = get_lockdown_series('Bangalore', '9/03/2020', 21)
  print(s)
