from utils_latam import Scraper, get_browser, Date

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import re
from time import sleep
from datetime import datetime


class LatamDate(Date):
    def __init__(self, day, month, year):
        super().__init__(day, month, year)


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


    def date_string(self):
        return f"{str(self.day).zfill(2)}-{str(self.month).zfill(2)}-{self.year}"


    def __str__(self):
        month_name = self.month_mapping(self.month)
        return f"{self.day} de {month_name} de {self.year}"


class LatamScraper(Scraper):
    URL = 'https://www.latamairlines.com/cl/es'


    def __init__(self):
        self.driver = get_browser()


    def navigate_to_tickets_page(self, options):
        self.driver.get(self.URL)

        print(f"Title: {self.driver.title}")

        self.select_one_way_trip_type()

        self.select_origin(options.origin)
        self.select_destination(options.destination)

        self.select_date(options.departure_date)

        self.click_search_button()


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


    def select_one_way_trip_type(self):
        print("Selecting one way trip type...")

        xpath = ".//button[@id='btnTripTypeCTA']"
        self.wait_for_element_to_be_clickable(xpath)

        button = self.driver.find_element(By.XPATH, xpath)
        button.click()

        print("Found one way button...")

        xpath = ".//li[@id='itemTripType_0']"
        self.wait_for_element_to_be_clickable(xpath)

        selector = self.driver.find_element(By.XPATH, xpath)
        selector.click()


    def select_origin(self, origin):
        xpath = ".//input[@id='txtInputOrigin_field']"
        self.wait_for_element_to_be_present(xpath)

        origin_input = self.driver.find_element(By.XPATH, xpath)
        origin_input.send_keys(origin)

        sleep(1)

        xpath = ".//li[@id='lstItem_0']"
        self.wait_for_element_to_be_clickable(xpath)

        origin_selection = self.driver.find_element(By.XPATH, xpath)
        origin_selection.click()


    def select_destination(self, destination):
        xpath = ".//input[@id='txtInputDestination_field']"
        self.wait_for_element_to_be_present(xpath)

        destination_input = self.driver.find_element(By.XPATH, xpath)
        destination_input.send_keys(destination)

        sleep(1)

        xpath = ".//li[@id='lstItem_0']"
        self.wait_for_element_to_be_clickable(xpath)

        destination_selection = self.driver.find_element(By.XPATH, xpath)
        destination_selection.click()


    def select_date(self, date):
        xpath = ".//input[@id='departureDate']"
        self.wait_for_element_to_be_clickable(xpath)

        selection_button = self.driver.find_element(By.XPATH, xpath)
        selection_button.click()

        self.advance_to_relevant_month(date)

        # sleep(1)

        xpath = f".//td[contains(@aria-label, '{date}')]"
        self.wait_for_element_to_be_clickable(xpath)

        date_selection = self.driver.find_element(By.XPATH, xpath)
        date_selection.click()


    def advance_to_relevant_month(self, date):
        advs = self.get_necessary_advances(date)
        self.advance_months(advs)


    def advance_months(self, num):
        xpath = ".//div[contains(@aria-label, 'Avanza al mes de')]"
        self.wait_for_element_to_be_present(xpath)

        next_month_arrow = self.driver.find_element(By.XPATH, xpath)

        for _ in range(num):
            next_month_arrow.click()


    def get_necessary_advances(self, date):
        today = self.today()
        return self.get_months_difference(today, date.date_string())


    def today(self):
        return datetime.today().strftime("%d-%m-%Y")


    def get_months_difference(self, date1, date2):  # date1 <= date2
        _, month1, year1 = date1.split("-")
        _, month2, year2 = date2.split("-")

        return 12 * (int(year2) - int(year1)) + int(month2) - int(month1)


    def click_search_button(self):
        xpath = ".//button[@id='btnSearchCTA']"
        self.wait_for_element_to_be_clickable(xpath)

        button = self.driver.find_element(By.XPATH, xpath)
        button.click()


    def get_flight_elements_list(self):
        xpath = ".//ol[contains(@aria-label, 'Vuelos disponibles')]"
        self.wait_for_element_to_be_present(xpath)

        return self.driver.find_element(By.XPATH, xpath)


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
        return int(re.sub("[^0-9]", "", cost_string))


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
