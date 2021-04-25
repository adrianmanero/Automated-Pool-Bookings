"""
    Author: Adrián Manero Higuera
    Version: 1.0
    Description: Script to book slots in a swimming pool using Selenium
"""

from lib import json_processing
from lib import scraping

# Main web page URL
URL = 'https://shop.syrdall-schwemm.lu/event.html?eventId=3'

# Timetables URL
TIMETABLE_URL = 'https://shop.syrdall-schwemm.lu/reservation/ajax/calendar?eventId=3'

# Read JSON containig all the booking information
data = json_processing.read_url()

# Booking information
DAY_TO_BOOK = data['day']
MONTH_TO_BOOK = data['month']
YEAR_TO_BOOK = data['year']
TIME_TO_BOOK = data['start_time']
TICKETS_TO_BOOK = data['tickets_number']
NAME_TO_BOOK = data['name']
SURNAME_TO_BOOK = data['surname']
EMAIL_TO_BOOK = data['email']
PHONE_NUMBER_TO_BOOK = data['phone_number']


# Main function
def main():
    # Console prints
    print('SCRIPT DE RESERVA DE HORARIOS (v1.0)', '\n')
    print('Bienvenido, comenzando...', '\n')

    # Information obtained from the timetables URL, related to the day and time of the booking
    event_id = json_processing.read_timetables(TIMETABLE_URL, DAY_TO_BOOK, MONTH_TO_BOOK, YEAR_TO_BOOK, TIME_TO_BOOK)
    popup = 'div[data-eventid="' + str(event_id) + '"]'
    select_time = 'a[data-eventid="' + str(event_id) + '"]'

    # Check if the event is in the timetables page
    if event_id == 0:
        print('Esperando a que añadan nuevas horas...', '\n')
        while event_id == 0:
            event_id = json_processing.read_timetables(TIMETABLE_URL, DAY_TO_BOOK, MONTH_TO_BOOK, YEAR_TO_BOOK, TIME_TO_BOOK)
            popup = 'div[data-eventid="' + str(event_id) + '"]'
            select_time = 'a[data-eventid="' + str(event_id) + '"]'

    else:
        # Web scraping
        scraping.selenium_scraping(URL, popup, select_time, TICKETS_TO_BOOK, NAME_TO_BOOK, SURNAME_TO_BOOK, EMAIL_TO_BOOK, PHONE_NUMBER_TO_BOOK)

    # Wait for the user to interact with the console to exit
    done = input('Pulsa la tecla "enter" para salir')
    if done:
        exit(0)


if __name__ == '__main__':
    main()
