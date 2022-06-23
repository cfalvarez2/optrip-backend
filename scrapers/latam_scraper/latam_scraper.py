from scraper import Scraper, get_browser

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep


class LatamDate:
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year


    def month_mapping(self, month_num):
        return [
            "enero", 
            "febrero", 
            "marzo", 
            "abril", 
            "mayo", 
            "junio", 
            "julio", 
            "agosto", 
            "septiembre", 
            "octubre", 
            "noviembre", 
            "diciembre"
        ][month_num - 1]


    def __str__(self):
        month_name = self.month_mapping(self.month)
        return f"{self.day} de {month_name} de {self.year}"


class LatamScraper(Scraper):
    URL = 'https://www.latamairlines.com/cl/es'


    def __init__(self):
        self.driver = get_browser()


    def get_trip_type_button(self):
        return self.driver.find_element(
            By.XPATH,
            "//button[@id='btnTripTypeCTA']"
        )


    def select_trip_type(self, type_):
        num_selector = int(type_ == 'round')

        button = self.get_trip_type_button()
        button.click()

        sleep(1)

        selector = self.driver.find_element(
            By.ID, 
            f"itemTripType_{num_selector}"
        )

        selector.click()


    def select_origin(self, origin):
        origin_input = self.driver.find_element(
            By.XPATH,
            "//input[@id='txtInputOrigin_field']"
        )

        origin_input.send_keys(origin)

        sleep(1)

        origin_selection = self.driver.find_element(By.ID, "lstItem_0")
        origin_selection.click()


    def select_destination(self, destination):
        destination_input = self.driver.find_element(
            By.XPATH,
            "//input[@id='txtInputDestination_field']"
        )

        destination_input.send_keys(destination)

        sleep(1)

        destination_selection = self.driver.find_element(By.ID, "lstItem_0")
        destination_selection.click()


    def select_departure_date(self, date):
        departure_date_selection_button = self.driver.find_element(
            By.XPATH,
            "//input[@id='departureDate']"
        )

        departure_date_selection_button.click()

        sleep(1)

        date_selection = self.driver.find_element(
            By.XPATH,
            f"//td[contains(@aria-label, '{date}')]"
        )

        date_selection.click()


    def select_return_date(self, date):
        pass


    def click_search_button(self):
        search_button = self.driver.find_element(
            By.XPATH, 
            "//button[@id='btnSearchCTA']"
        )

        search_button.click()


    def navigate_to_tickets_page(self, options):
        self.driver.get(self.URL)

        self.select_trip_type(options.type_)

        self.select_origin(options.origin)
        self.select_destination(options.destination)

        self.select_departure_date(options.departure_date)
        if options.return_date:
            self.select_return_date(options.return_date)

        self.click_search_button()

        WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located(
                (By.XPATH, "//ol[contains(@aria-label, 'Vuelos disponibles')]")
            )
        )


    def get_flight_elements_list(self):
        return self.driver.find_element(
            By.XPATH, "//ol[contains(@aria-label, 'Vuelos disponibles')]"
        )


    def get_flight_cards_list(self, flight_elements_list):
        return flight_elements_list.find_elements(
            By.TAG_NAME, "li"
        )

    
    def get_flight_departure_time(self, card):
        return card.find_element(
            By.XPATH,
            ".//div[contains(@class, 'flight-information')]/span[1]"
        ).text

    
    def duration_formatting(self, duration_string):
        return [int(s) for s in duration_string.split() if s.isdigit()]


    def get_flight_duration(self, card):
        duration = card.find_element(
            By.XPATH,
            ".//div[contains(@class, 'flight-duration')]/span[2]"
        ).text

        hours, mins = self.duration_formatting(duration)
        return 60 * hours + mins


    def cost_formatting(self, cost_string):
        return int(cost_string[4:].replace(".", ""))


    def get_flight_cost(self, card):
        cost = card.find_element(
            By.XPATH,
            ".//span[contains(@aria-label, 'Pesos chilenos')]"
        ).text

        return self.cost_formatting(cost)


    def get_flight_info(self, card):
        departure_time = self.get_flight_departure_time(card)
        duration = self.get_flight_duration(card)
        cost = self.get_flight_cost(card)

        return {
            'departure_time': departure_time,
            'duration': duration,
            'cost': cost
        }


    def get_tickets_information(self):
        flight_elements_list = self.get_flight_elements_list()
        cards = self.get_flight_cards_list(flight_elements_list)

        flights_info = []

        for card in cards:
            try:
                flight_info = self.get_flight_info(card)
                flights_info.append(flight_info)

            except NoSuchElementException:
                pass

        return flights_info
