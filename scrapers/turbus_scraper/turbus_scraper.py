from time import sleep
from scraper import Scraper, Date, get_browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TurbusDate(Date):
    def __init__(self, day, month, year):
        super().__init__(day, month, year)


class TurbusScraper(Scraper):
    URL = 'https://new.turbus.cl/turbuscl/inicio-compra'


    def __init__(self):
        self.driver = get_browser()


    def navigate_to_tickets_page(self, options):
        self.driver.get(self.URL)

        sleep(2)

        self.select_origin(options.origin)
        self.select_destination(options.destination)

        self.select_dates(options.departure_date, options.return_date)

        # self.select_trip_type(options.type_)

        self.click_search_button()

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='ticket-item']")
            )
        )


    def get_ticket_elements_list(self):
        xpath = "//div[@class='itinerario-container']/div[@class='ticket-item']"
        return self.driver.find_elements(By.XPATH, xpath)


    def get_ticket_departure_time(self, ticket):
        xpath = ".//div[@class='ticket_time']"
        return ticket.find_element(By.XPATH, xpath).text


    def get_ticket_cost(self, ticket):
        xpath = ".//div[@class='ticket_price-value']"
        cost = ticket.find_element(By.XPATH, xpath).text
        return self.cost_formatting(cost)

    
    def cost_formatting(self, cost_string):
        return int(cost_string.strip().replace(".", "")[1:])


    def get_ticket_trip_duration(self, ticket):
        xpath = ".//div[@class='ticket_duration']"
        duration = ticket.find_element(By.XPATH, xpath).text
        return self.duration_formatting(duration)

    
    def duration_formatting(self, duration_string):
        hours, minutes =  duration_string.strip().split()
        return 60 * int(hours[:-1]) + int(minutes[:-1])


    def get_ticket_number_of_scales(self, ticket):
        xpath = ".//div[@class='paradas']/span"
        return ticket.find_element(By.XPATH, xpath).text


    def get_ticket_info(self, ticket):
        departure_time = self.get_ticket_departure_time(ticket)
        cost = self.get_ticket_cost(ticket)
        duration = self.get_ticket_trip_duration(ticket)

        # num_scales = self.get_ticket_number_of_scales(ticket)

        return {
            'departure_time': departure_time,
            'duration': duration,
            'cost': cost
        }


    def get_tickets_information(self):
        return [
            self.get_ticket_info(ticket)
            for ticket in self.get_ticket_elements_list()
        ]


    def find_trip_type_button(self, type_):
        if type_ == "round":
            return self.get_round_trip_button()
        return self.get_one_way_trip_button()


    def find_one_way_trip_button(self):
        xpath = "//input[@id='checkRadioIda']"
        return self.driver.find_element(By.XPATH, xpath)


    def find_round_trip_button(self):
        xpath = "//input[@id='checkRadioIdaVuelta']"
        return self.driver.find_element(By.XPATH, xpath)


    def select_trip_type(self, type_):
        button = self.get_trip_type_button(type_)
        button.click()


    def select_origin(self, origin):
        xpath = "//input[@id='origen']"

        # WebDriverWait(self.driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, xpath))
        # )

        origin_input = self.driver.find_element(By.XPATH, xpath)

        origin_input.click()
        origin_input.send_keys(origin)

        sleep(1)

        xpath = f"//li[contains(text(), '{origin}')]"
        origin_selection = self.driver.find_element(By.XPATH, xpath)

        origin_selection.click()


    def select_destination(self, destination):
        xpath = "//input[@id='destino']"
        destination_input = self.driver.find_element(By.XPATH, xpath)

        destination_input.click()
        destination_input.send_keys(destination)

        sleep(1)

        xpath = f"//li[contains(text(), '{destination}')]"
        destination_selection = self.driver.find_element(By.XPATH, xpath)

        destination_selection.click()


    def select_dates(self, departure_date, return_date=None):
        xpath = "//label[@class='form-input form-input-date input-modal']"
        departure_date_label = self.driver.find_element(By.XPATH, xpath)
        departure_date_label.click()

        calendar = self.find_calendar()

        xpath = f"//div[contains(text(), '{departure_date.day}')]"
        calendar.find_element(By.XPATH, xpath).click()

        sleep(2)

        if return_date is None:
            return

        xpath = f"//div[contains(text(), '{return_date.day}')]"
        calendar.find_element(By.XPATH, xpath).click()


    def find_calendar(self):
        xpath = "//div[@id='calendar']"
        return self.driver.find_element(By.XPATH, xpath)


    def click_search_button(self):
        xpath = "//button[@id='buscarPasaje']"
        search_button = self.driver.find_element(By.XPATH, xpath)
        search_button.click()
