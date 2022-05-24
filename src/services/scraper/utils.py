from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


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
        pass

    def navigate_to_tickets_page(self):
        raise NotImplementedError

    def get_trips(self):
        raise NotImplementedError


class TripOptions:
    def __init__(self, origin, destination, departure_date, return_date=None):
        self.origin = origin
        self.destination = destination

        self.departure_date = departure_date
        self.return_date = return_date

        self.type_ = 'round' if return_date is not None else 'one_way'
