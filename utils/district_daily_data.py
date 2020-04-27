"""Expose the API for the District Daily Data"""
# Reads the data from the district json file and returns values
import json
from datetime import datetime as dt

data_dir = '../data/'
date_format = '%d/%m/%Y'


def convert_to_daily(data_list):
  """Convert cumulative data in list to daily data

  Arguments:
      data_list {List}
  """
  for _in in range(1, len(data_list)):
    data_list[-_in] = data_list[-_in] - data_list[-_in - 1]


def get_district_data(district):
  """Returns the raw data of the given district in a list

  Arguments:
      district {String} -- District Name

  Returns:
      List -- [(date, count), (date, count), ..., (date, count)]
  """
  with open(data_dir + 'district-data.json') as f:
    district_dict = json.load(f)

  district_data = []
  for date, data in district_dict.items():
    if date == "03/02/2020":
      continue
    if district in data:
      district_data.append((date, data[district]['infected']))

  return district_data


def get_district_time_series(district, start_date, num_days, cumulative=True):
  """Return the time series data of the given district

  Arguments:
      district {String} -- Name of the district
      start_date {String} -- Start Date in format DD/MM/YYYY
      num_days {Integer} -- Number of days

  Keyword Arguments:
      cumulative {bool} -- Whether cumulative data is needed (default: {True})

  Returns:
      List -- List of requisite numbers. Length = num_days
  """
  district_data = get_district_data(district)

  ret_list = []
  prev_date = start_date
  for obj in district_data:
    # Condition to check if ret_list has been initiated.
    # Only then check if some days got missing in between.
    if ret_list:
      # Calculate number of days between prev_date and curr date
      days = (dt.strptime(obj[0], date_format) -
              dt.strptime(prev_date, date_format)).days
      if days > 1:
        # Append the last number again for those many days
        for _in in range(days - 1):
          ret_list.append(ret_list[-1])

    if obj[0] == start_date or ret_list:
      ret_list.append(obj[1])

    prev_date = obj[0]
    if len(ret_list) == num_days:
      break

  if not cumulative:
    convert_to_daily(ret_list)
  return ret_list


if __name__ == '__main__':
  d = get_district_time_series('Delhi', '04/03/2020', 7, True)
  print(d)
