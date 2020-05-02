"""Expose the API for the State Daily Data"""
# Reads the data from the state json file
import os
import json
from datetime import datetime as dt

script_dir = os.path.dirname(os.path.abspath(__file__))
state_data_dir = script_dir + '/../data/'
date_format = '%d/%m/%Y'


def convert_to_daily(data_list):
  """Convert cumulative data in list to daily data

  Arguments:
      data_list {List}
  """
  for _in in range(1, len(data_list)):
    data_list[-_in] = data_list[-_in] - data_list[-_in - 1]


def get_infection_start(state):
  """Get the date of infection start in the state

  Arguments:
      state {String} -- Name of the state

  Returns:
      String -- Start date of infection
  """
  with open(state_data_dir + 'state-data.json') as f:
    state_dict = json.load(f)

  start_date = '03/02/2020'
  for date, data in state_dict.items():
    if date == '03/02/2020':
      continue
    if state in data and dt.strptime(start_date, date_format) > dt.strptime(
        date, date_format):
      start_date = date

  return start_date


def get_state_data(state):
  """Returns the raw data of the given state in a list

  Arguments:
      state {String} -- State Name

  Returns:
      List -- [(date, count), (date, count), ..., (date, count)]
  """
  with open(state_data_dir + 'state-data.json') as f:
    state_dict = json.load(f)

  state_data = []
  for date, data in state_dict.items():
    if date == "03/02/2020":
      continue
    if state in data:
      state_data.append((date, data[state]))

  state_data.sort(key=lambda d: dt.strptime(d[0], date_format))
  return state_data


def get_state_time_series(state, start_date, cumulative=False, num_days=-1):
  """Return the time series data of the given state

  Arguments:
      state {String} -- Name of the state
      start_date {String} -- Start Date in format DD/MM/YYYY

  Keyword Arguments:
      cumulative {bool} -- Whether cumulative data is needed (default: {False})
      num_days {Integer} -- Number of days (default: {-1, to get all days data})

  Returns:
      List -- List of requisite numbers. Length = num_days
  """
  state_data = get_state_data(state)

  ret_list = []
  prev_date = dt.strptime(start_date, date_format)
  for obj in state_data:
    curr_date = dt.strptime(obj[0], date_format)
    # Condition to check if ret_list has been initiated.
    # Only then check if some days got missing in between.
    if ret_list:
      # Calculate number of days between prev_date and curr date
      days = (curr_date - prev_date).days
      if days > 1:
        # Append the last number again for those many days
        for _in in range(days - 1):
          ret_list.append(ret_list[-1])

    # Add data for the range given
    if curr_date >= dt.strptime(start_date, date_format):
      # Case: When the given start date is before the start of infections
      if not ret_list:
        initial_days = (curr_date - dt.strptime(start_date, date_format)).days
        for _in in range(initial_days):
          ret_list.append(0)
      ret_list.append(obj[1])

    prev_date = curr_date
    if len(ret_list) == num_days:
      break

  if not cumulative:
    convert_to_daily(ret_list)
  return ret_list


if __name__ == '__main__':
  start_date = get_infection_start('Uttar Pradesh')
  d = get_state_time_series('Uttar Pradesh', '04/03/2020', True)
  print(start_date, d)
