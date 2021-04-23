from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
import time

# Web scraping with selenium
def selenium_scraping(url, url_popup, select_time, tickets_to_book, name_to_book, surname_to_book, email_to_book, phone_number_to_book):

    # Boolean to end while loop
    success = False

    # Web driver and options to suppress some console prints
    options = ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = Chrome(executable_path='lib/chromedriver', options=options)
    driver.get(url)

    # Variables to create some stats
    current_time = time.time()
    number_of_reloads = 0

    while not success:
        try:
            # Get to the popup that shows the full timetable of the day
            WebDriverWait(driver, 1).until(ec.element_to_be_clickable((By.CSS_SELECTOR, url_popup)))
            elem_is_red = driver.find_elements_by_css_selector(url_popup + '[style="background:#c31414"]')

            # Console prints
            print('#----- Intento Número', number_of_reloads, '-----#')
            number_of_reloads += 1
            print('· Han pasado', round(time.time() - current_time, 2), 'segundos')
            print('· Son las', time.strftime('%H:%M:%S', time.localtime()), '\n')

            # If the slot is not red, it means that it is available
            if not elem_is_red:

                # End the loop
                success = True

                print('La hora deseada está disponible', '\n')

                # Since the slot is available, it clicks on it
                popup = driver.find_element_by_css_selector(url_popup)
                popup.click()

                print('Seleccionando la hora...', '\n')

                # Once the popup is displayed, select the correct time
                WebDriverWait(driver, 1).until(ec.element_to_be_clickable((By.CSS_SELECTOR, select_time)))
                time_select = driver.find_element_by_css_selector(select_time)
                ActionChains(driver).move_to_element(time_select).click().perform()

                # Console prints
                print('Rellenando el formulario con los siguientes datos:', '\n')
                print('\t', '- Número de Tickets:', tickets_to_book, '\n')
                print('\t', '- Nombre:', name_to_book, '\n')
                print('\t', '- Apellido(s):', surname_to_book, '\n')
                print('\t', '- Email:', email_to_book, '\n')
                print('\t', '- Teléfono:', phone_number_to_book, '\n')

                # Fulfill the form
                # Number of tickets
                ticket_number = driver.find_element_by_name('quantity_1_1_11_3_2_0')
                ticket_number.send_keys(tickets_to_book)

                # Name
                name = driver.find_element_by_name('ev_specialform_1')
                name.send_keys(name_to_book)

                # Surname
                surname = driver.find_element_by_name('ev_specialform_2')
                surname.send_keys(surname_to_book)

                # Email
                email = driver.find_element_by_name('ev_specialform_3')
                email.send_keys(email_to_book)

                # Phone Number
                phone_number = driver.find_element_by_name('ev_specialform_5')
                phone_number.send_keys(phone_number_to_book)

                # COVID-19 acceptance
                checkbox = driver.find_element_by_name('checkAGB')
                checkbox.click()

                # Confirmation button
                confirm = driver.find_element_by_name('submit_btn')
                confirm.click()

                print('LA RESERVA HA SIDO HECHA', '\n \n')

            else:
                driver.refresh()

        except ElementNotInteractableException:
            print('El elemento seleccionado no está disponible, por lo que no se puede interactuar no él', '\n')
            driver.refresh()

        except TimeoutException:
            print('El horario aún no está disponible...', '\n')
            driver.refresh()

    driver.quit()
