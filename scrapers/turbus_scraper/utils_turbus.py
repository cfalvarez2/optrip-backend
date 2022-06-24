from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def _set_options():
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--incognito")
    options.add_argument("--window-size=1920,1080")
    return options


def get_browser(wait=2):
    driver = webdriver.Firefox(
        service=Service(GeckoDriverManager().install()),
        options=_set_options()
    )

    driver.implicitly_wait(wait)

    return driver


class Scraper:
    def __init__(self):
        self.driver = None


    def navigate_to_tickets_page(self):
        raise NotImplementedError


    def get_tickets_information(self):
        raise NotImplementedError


    def scrape(self, options):
        try:
            self.navigate_to_tickets_page(options)
            return self.get_tickets_information()
        except Exception as e:
            print(e)
            self.driver.close()
            self.driver = get_browser()


    def wait_for_element_to_be_clickable(self, xpath, secs=10):
        WebDriverWait(self.driver, secs).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )


    def wait_for_element_to_be_present(self, xpath, secs=10):
        WebDriverWait(self.driver, secs).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )


class Date:
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year


class TripOptions:
    def __init__(self, origin, destination, departure_date):
        self.origin = origin
        self.destination = destination

        self.departure_date = departure_date
