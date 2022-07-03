from utils_turbus import Scraper, Date, get_browser
from selenium.webdriver.common.by import By

from datetime import datetime


class TurbusDate(Date):
    def __init__(self, day, month, year):
        super().__init__(day, month, year)


class TurbusScraper(Scraper):
    URL = 'https://new.turbus.cl/turbuscl/inicio-compra'


    def __init__(self):
        self.driver = get_browser()


    def navigate_to_tickets_page(self, options):
        self.driver.get(self.URL)

        self.select_origin(options.origin)
        self.select_destination(options.destination)

        self.select_date(options.departure_date)

        self.click_search_button()


    def get_tickets_information(self):
        xpath = ".//h2[contains(text(), 'SELECCIONA TU PASAJE DE IDA')]"
        self.wait_for_element_to_be_present(xpath)

        return [
            self.get_ticket_info(ticket)
            for ticket in self.get_ticket_elements_list()
        ]


    def get_ticket_info(self, ticket):
        xpath = ".//div[@class='ticket-item']"
        self.wait_for_element_to_be_present(xpath)

        departure_time = self.get_ticket_departure_time(ticket)
        cost = self.get_ticket_cost(ticket)
        duration = self.get_ticket_trip_duration(ticket)

        # num_scales = self.get_ticket_number_of_scales(ticket)

        return {
            'departure_time': departure_time,
            'duration': duration,
            'cost': cost
        }


    def get_ticket_elements_list(self):
        xpath = ".//div[@class='itinerario-container']/div[@class='ticket-item']"
        return self.driver.find_elements(By.XPATH, xpath)


    def get_ticket_departure_time(self, ticket):
        xpath = ".//div[@class='ticket_time']"
        self.wait_for_element_to_be_present(xpath)
        return ticket.find_element(By.XPATH, xpath).text


    def get_ticket_cost(self, ticket):
        xpath = ".//div[@class='ticket_price-value']"
        self.wait_for_element_to_be_present(xpath)
        cost = ticket.find_element(By.XPATH, xpath).text
        return self.cost_formatting(cost)

    
    def cost_formatting(self, cost_string):
        return int(cost_string.strip().replace(".", "")[1:])


    def get_ticket_trip_duration(self, ticket):
        xpath = ".//div[@class='ticket_duration']"
        self.wait_for_element_to_be_present(xpath)
        duration = ticket.find_element(By.XPATH, xpath).text
        return self.duration_formatting(duration)


    def duration_formatting(self, duration_string):
        hours, minutes =  duration_string.strip().split()
        return 60 * int(hours[:-1]) + int(minutes[:-1])


    def get_ticket_number_of_scales(self, ticket):
        xpath = ".//div[@class='paradas']/span"
        return ticket.find_element(By.XPATH, xpath).text


    def select_origin(self, origin):
        # print("Selecting origin...")

        xpath = ".//input[@id='origen']"
        self.wait_for_element_to_be_present(xpath)
        self.wait_for_element_to_be_clickable(xpath)

        origin_input = self.driver.find_element(By.XPATH, xpath)
        origin_input.click()
        origin_input.send_keys(origin)

        xpath = f".//li[contains(text(), '{origin}')]"
        self.wait_for_element_to_be_clickable(xpath)

        origin_selection = self.driver.find_element(By.XPATH, xpath)
        origin_selection.click()


    def select_destination(self, destination):
        # print("Selection destination...")

        xpath = ".//input[@id='destino']"
        self.wait_for_element_to_be_clickable(xpath)
        destination_input = self.driver.find_element(By.XPATH, xpath)

        destination_input.click()
        destination_input.send_keys(destination)

        xpath = f".//li[contains(text(), '{destination}')]"
        self.wait_for_element_to_be_clickable(xpath)

        destination_selection = self.driver.find_element(By.XPATH, xpath)
        destination_selection.click()


    def advance_to_relevant_month(self, calendar, date):
        today = datetime.today().strftime("%d-%m-%Y")
        _, month, year = today.split("-")

        diff = 12 * (date.year - int(year)) + date.month - int(month)

        xpath = ".//span[@class='next']"
        next_arrow = calendar.find_element(By.XPATH, xpath)

        for _ in range(diff):
            next_arrow.click()


    def select_date(self, departure_date):
        # print("Selecting date...")

        xpath = ".//label[@class='form-input form-input-date input-modal']"
        self.wait_for_element_to_be_clickable(xpath)

        departure_date_label = self.driver.find_element(By.XPATH, xpath)
        departure_date_label.click()

        xpath = ".//div[@id='calendar']"
        self.wait_for_element_to_be_present(xpath)

        calendar = self.driver.find_element(By.XPATH, xpath)

        self.advance_to_relevant_month(calendar, departure_date)

        xpath = f".//div[contains(text(), '{departure_date.day}')]"
        self.wait_for_element_to_be_clickable(xpath)

        date_element = calendar.find_element(By.XPATH, xpath)

        for _ in range(2):
            date_element.click()


    def click_search_button(self):
        # print("Clicking search button...")

        xpath = ".//button[@id='buscarPasaje']"
        self.wait_for_element_to_be_clickable(xpath)

        search_button = self.driver.find_element(By.XPATH, xpath)
        search_button.click()
