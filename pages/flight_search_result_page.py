from selenium.common import TimeoutException

from base.base_functions import Base
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import time


class FlightSearchResultPage(Base):
    """Flight search result page that https://www.enuygun.com/ucak-bileti/"""
    FILTERS = (By.CSS_SELECTOR, ".card-title")
    DEPARTURE_TIME_SLIDER_1 = (
        By.XPATH,
        '//div[@data-testid="departureDepartureTimeSlider"]//div[@class="rc-slider-handle rc-slider-handle-1"]')
    DEPARTURE_TIME_SLIDER_2 = (
        By.XPATH,
        '//div[@data-testid="departureDepartureTimeSlider"]//div[@class="rc-slider-handle rc-slider-handle-2"]')
    DEPARTURE_TIMES = (By.XPATH, '//*[@data-testid="departureTime"]')
    THY = (By.XPATH, '//*[@data-testid="Türk Hava Yolları"]')
    PRICE_LOCATOR = '//div[@data-testid="flightInfoPrice"]'
    PRICE_LOCATOR_BY_PROVIDER = '//div[@data-booking-provider="{}"]//div[@data-testid="flightInfoPrice"]'
    PREVIEW_NEXT_BUTTON = (By.CSS_SELECTOR, '.flight-list-date-btn')
    WEG_LOADER = (By.XPATH, '//*[@data-testid="weg-loader"]')
    FLIGHT_LIST_DATE = (By.XPATH, '//div[@data-testid="flight__list-departureDate"]')

    def __init__(self, driver):
        self.driver = driver
        self.check()

    def check(self):
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(self.FILTERS),
                                                 'No "filters" element on the page!')
        except TimeoutException:
            print("Timeout: Element not visible after 20 seconds")
            raise

    def click_filter(self, index):
        """
        Clicks the filter at the specified index
        :param index:
        :return:
        """
        self.click_element_by_index(self.FILTERS, index)
        time.sleep(1)

    def set_slider_value(self, slider_locator, value):
        """
        Sets the value of the slider to the given value
        :param slider_locator:
        :param value:
        :return:
        """
        try:
            wait = WebDriverWait(self.driver, 10)
            slider_element = wait.until(EC.element_to_be_clickable(slider_locator))
            current_value = int(slider_element.get_attribute("aria-valuenow"))
        except Exception as e:
            raise Exception(
                "Could not get the 'aria-valuenow' attribute of the slider element. Please make sure the element has this attribute.") from e

        min_value = int(slider_element.get_attribute("aria-valuemin"))
        max_value = int(slider_element.get_attribute("aria-valuemax"))

        value_per_pixel = (max_value - min_value) / 242

        offset = int((value - current_value) / value_per_pixel)

        actions = ActionChains(self.driver)
        actions.click_and_hold(slider_element)
        actions.move_by_offset(offset, 0)
        actions.release()
        actions.perform()
        time.sleep(2)

    def check_time_in_range(self, time_str, start_str, end_str):
        """
        Checks if the given time is in the specified range
        :param time_str:
        :param start_str:
        :param end_str:
        :return:
        """
        time_format = "%H:%M"
        time = datetime.strptime(time_str, time_format)
        start = datetime.strptime(start_str, time_format)
        end = datetime.strptime(end_str, time_format)
        print("time checked")

        assert start <= time <= end, f"{time_str} is not in the range between {start_str} and {end_str}"

    def get_departure_times(self):
        """
        Gets the departure times of the flights
        :return:
        """
        departure_time_elements = self.driver.find_elements(*self.DEPARTURE_TIMES)
        return [element.text for element in departure_time_elements]

    def get_prices(self):
        """
        Gets the prices of the flights
        :return:
        """
        price_elements = self.driver.find_elements(By.XPATH, self.PRICE_LOCATOR)
        prices = [element.get_attribute('data-price') for element in price_elements]
        return prices

    def get_prices_by_provider(self, provider):
        """
        Gets the prices of the flights by the given provider
        :param provider:
        :return:
        """
        PROVIDER = self.PRICE_LOCATOR_BY_PROVIDER.format(provider)
        try:
            wait = WebDriverWait(self.driver, 10)  # 10 saniye boyunca bekleyeceğiz
            price_elements = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, PROVIDER)))  # Element yüklenene kadar bekler
        except Exception as e:
            raise Exception("Could not load the elements within the given time.") from e

        prices = [element.get_attribute('data-price') for element in price_elements]
        print("pirces checked")
        return prices

    def click_next_button(self):
        self.click_element_by_index(self.PREVIEW_NEXT_BUTTON, 1)
        self.wait_for_element_invisible(self.WEG_LOADER)
        time.sleep(1)

    def click_preview_button(self):
        self.click_element_by_index(self.PREVIEW_NEXT_BUTTON, 0)
        time.sleep(1)

    def get_flight_list_date(self):
        """
        Gets the text of the flight list date element
        :return: The text of the flight list date element
        """
        flight_list_date_element = self.driver.find_element(*self.FLIGHT_LIST_DATE)
        return flight_list_date_element.text
