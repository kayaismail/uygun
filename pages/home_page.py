from selenium.common import TimeoutException

from base.base_functions import Base
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

from pages.flight_search_result_page import FlightSearchResultPage


class HomePage(Base):
    """Home page of https://www.enuygun.com/"""
    ROUND_TRIP = (By.XPATH, '//*[@data-testid="search-round-trip-label"]')
    FLIGHT_ORIGIN = (By.XPATH, '//*[@data-testid="flight-origin-input-comp"]')
    FLIGHT_ORIGIN_INPUT =(By.XPATH, '//*[@data-testid="endesign-flight-origin-autosuggestion-input"]')
    FLIGHT_DESTINATION = (By.XPATH, '//*[@data-testid="flight-destination-input-comp"]')
    FLIGHT_DESTINATION_INPUT = (By.XPATH, '//*[@data-testid="endesign-flight-destination-autosuggestion-input"]')
    DEPARTURE_DATE = (By.XPATH, '//*[@data-testid="enuygun-homepage-flight-departureDate-datepicker-input"]')
    RETURN_DATE = (By.XPATH, '//*[@data-testid="enuygun-homepage-flight-returnDate-datepicker-input"]')
    DATE_PICKER = (By.XPATH, '//*[@data-testid="datepicker-active-day" and text()= "{}"]')
    ORIGIN_AUTOSUGGESTION_OPTION = (By.XPATH,
                                    '//*[@data-testid="endesign-flight-origin-autosuggestion-option-item-{}"]')
    DESTINATION_AUTOSUGGESTION_OPTION = \
        (By.XPATH, '//*[@data-testid="endesign-flight-destination-autosuggestion-option-item-{}"]')
    FLIGHT_SUBMIT_BUTTON = (By.XPATH, '//*[@data-testid="enuygun-homepage-flight-submitButton"]')
    WEG_LOADER = (By.XPATH, '//*[@data-testid="weg-loader"]')

    def __init__(self, driver):
        self.driver = driver
        driver.implicitly_wait(10)
        self.navigate_url("https://www.enuygun.com/")
        self.wait = WebDriverWait(self.driver, 10)
        self.check()

    def check(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.FLIGHT_ORIGIN),
                                                 'No "flight origin" element on the page!')
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.FLIGHT_DESTINATION),
                                                 'No "flight destination" element on the page!')
        except TimeoutException:
            print("Timeout: Elements not visible after 10 seconds")
            raise

    def click_flight_origin(self):
        """
        Clicks the flight origin input
        :return:
        """

        self.click_element(self.FLIGHT_ORIGIN)

    def enter_flight_origin(self, text):
        """
        Enters the text to the flight origin input
        :param text:
        :return:
        """

        self.enter_text(self.FLIGHT_ORIGIN_INPUT, text)
        time.sleep(0.5)

    def click_flight_destination(self):
        """
        Clicks the flight destination input
        :return:
        """

        self.click_element(self.FLIGHT_DESTINATION)
        time.sleep(0.5)

    def enter_flight_destination(self, text):
        """
        Enters the text to the flight destination input
        :param text:
        :return:
        """

        self.enter_text(self.FLIGHT_DESTINATION_INPUT, text)
        time.sleep(0.5)

    def click_round_trip(self):
        """
        Clicks the round trip button
        :return:
        """

        self.click_element(self.ROUND_TRIP)

    def click_departure_date(self):
        """
        Clicks the departure date area
        :return:
        """

        self.click_element(self.DEPARTURE_DATE)
        time.sleep(0.5)

    def click_return_date(self):
        """
        Clicks the return date area
        """

        self.click_element(self.RETURN_DATE)
        time.sleep(0.5)

    def click_origin_autosuggestion_option(self, option_number=0):
        locator = (
        By.XPATH, '//*[@data-testid="endesign-flight-origin-autosuggestion-option-item-{}"]'.format(option_number))
        self.click_element(locator)
        time.sleep(0.5)

    def click_destination_autosuggestion_option(self, option_number=0):
        """
        Clicks the destination autosuggestion option
        :param option_number: Index of the option you want to click
        """
        locator = (
        By.XPATH, '//*[@data-testid="endesign-flight-destination-autosuggestion-option-item-{}"]'.format(option_number))
        self.click_element_by_index(locator, 0)
        time.sleep(0.5)

    def select_departure_date(self, month_year, day):
        """
        Sets campaign's activation status, in other words activates or deactivates current personalization
        :param str month_year: Set month and year value as "Ağustos 2024", "Temmuz 2024" etc.
        :param str day: Set day value as "1", "2", "3" etc.

        """
        locator = (By.XPATH,
                   '//*[@data-testid="enuygun-homepage-flight-departureDate-month-name-and-year" and text()="{}"]'
                   '/following::button[@data-testid="datepicker-active-day" and text()="{}"]'
                   .format(month_year, day))
        self.click_element_by_index(locator=locator, index=0)
        time.sleep(0.5)

    def select_return_date(self, month_year, day):
        """
        Sets campaign's activation status, in other words activates or deactivates current personalization
        :param str month_year: Set month and year value as "Ağustos 2024", "Temmuz 2024" etc.
        :param str day: Set day value as "1", "2", "3" etc.

        """
        locator = (By.XPATH,
                   '//*[@data-testid="enuygun-homepage-flight-returnDate-month-name-and-year" and text()="{}"]'
                   '/following::button[@data-testid="datepicker-active-day" and text()="{}"]'
                   .format(month_year, day))
        self.click_element_by_index(locator=locator, index=0)
        time.sleep(0.5)

    def click_flight_submit_button(self):
        """
        Clicks the flight submit button
        """
        self.click_element(self.FLIGHT_SUBMIT_BUTTON)
        self.wait_for_element_invisible(self.WEG_LOADER)
        FlightSearchResultPage(self.driver)

    def get_origin_text(self):
        """
        Checks if the flight origin is set correctly
        :return: True if the flight origin is set correctly, False otherwise
        """
        return self.driver.find_element(*self.FLIGHT_ORIGIN_INPUT).get_attribute('value')

    def get_destination_text(self):
        """
        Checks if the flight destination is set correctly
        :return: True if the flight destination is set correctly, False otherwise
        """
        return self.driver.find_element(*self.FLIGHT_DESTINATION_INPUT).get_attribute('value')

    def get_departure_date(self):
        """
        Checks if the departure date is set correctly
        :return: True if the departure date is set correctly, False otherwise
        """
        return self.driver.find_element(*self.DEPARTURE_DATE).get_attribute('value')

    def get_return_date(self):
        """
        Checks if the return date is set correctly
        :return: True if the return date is set correctly, False otherwise

        """
        return self.driver.find_element(*self.RETURN_DATE).get_attribute('value')

    def is_flight_search_submitted(self):
        """
        Checks if the flight search is submitted
        :return: True if the flight search is submitted, False otherwise

        """
        return "ucak-bileti/istanbul-ankara" in self.driver.current_url
