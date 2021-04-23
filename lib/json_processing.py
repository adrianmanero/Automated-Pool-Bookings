from urllib import request
import json

# Function that reads the content of a web page
def read_url():
    with open('data.json') as fp:
        data = json.load(fp)

    return data


# Function that gets the ID of the desired
def read_timetables(timetable_url, day, month, year, time):

    # Get the timetables JSON
    req = request.urlopen(timetable_url)
    timetable_data = json.load(req)

    # Formatted date to compare to the timetables page
    date = year + '-' + month + '-' + day

    # Look for the desired eventid
    for i in range(len(timetable_data['monthly'])):
        if timetable_data['monthly'][i]['startdate'] == date and timetable_data['monthly'][i]['starttime'] == time:
            return timetable_data['monthly'][i]['id']

    return 0
