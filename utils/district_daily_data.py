"""Expose the API for the District Daily Data"""
# Reads the data from the district json file and returns values
import os
import json
from datetime import datetime as dt

script_dir = os.path.dirname(os.path.abspath(__file__))
district_data_dir = script_dir + '/../data/'
date_format = '%d/%m/%Y'


def convert_to_daily(data_list):
  """Convert cumulative data in list to daily data

  Arguments:
      data_list {List}
  """
  for _in in range(1, len(data_list)):
    data_list[-_in] = data_list[-_in] - data_list[-_in - 1]


def get_infection_start(district):
  """Get the date of infection start in the district

  Arguments:
      district {String} -- Name of the district

  Returns:
      String -- Start date of infection
  """
  with open(district_data_dir + 'district-data.json') as f:
    district_dict = json.load(f)

  for date, data in district_dict.items():
    if district in data:
      return date


def get_district_data(district):
  """Returns the raw data of the given district in a list

  Arguments:
      district {String} -- District Name

  Returns:
      List -- [(date, count), (date, count), ..., (date, count)]
  """
  with open(district_data_dir + 'district-data.json') as f:
    district_dict = json.load(f)

  district_data = []
  for date, data in district_dict.items():
    if date == "03/02/2020":
      continue
    if district in data:
      district_data.append((date, data[district]['infected']))

  return district_data


def get_district_time_series(district,
                             start_date,
                             cumulative=False,
                             num_days=-1):
  """Return the time series data of the given district

  Arguments:
      district {String} -- Name of the district
      start_date {String} -- Start Date in format DD/MM/YYYY

  Keyword Arguments:
      cumulative {bool} -- Whether cumulative data is needed (default: {False})
      num_days {Integer} -- Number of days (default: {-1, to get all days data})

  Returns:
      List -- List of requisite numbers. Length = num_days
  """
  district_data = get_district_data(district)

  ret_list = []
  prev_date = dt.strptime(start_date, date_format)
  for obj in district_data:
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


def get_all_districts():
  """Get the list of all the districts in the district-data api

  Returns:
      Set -- Set of all districts
  """
  with open(district_data_dir + 'district-data.json') as f:
    district_dict = json.load(f)
  districts = set([])

  for date, data in district_dict.items():
    if date == '03/02/2020':
      continue
    districts.update(data.keys())

  # Remove unnecessary points
  districts.remove('total-infected')
  districts.remove('max-legend-value')
  districts.remove('splitPoints')
  return districts


if __name__ == '__main__':
  d = get_district_time_series('Alappuzha', '04/03/2020', True)
  print(d)
  s = get_all_districts()
  print(len(s))
