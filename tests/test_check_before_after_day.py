import pytest
from selenium import webdriver
from pages.home_page import HomePage
from pages.flight_search_result_page import FlightSearchResultPage
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger()

load_dotenv()
BASE_URL = os.getenv('BASE_URL')


@pytest.mark.check_before_after_day
def test_check_before_after_day():
    """
    Test case is:

                1. Open the enuygun.com home page and click round trip
                2. Enter flight origin and click origin autosuggestion option
                3. Enter flight destination and click destination autosuggestion option
                4. Click departure date and select departure date
                5. Click return date and select return date
                6. Click flight submit button
                7. Click next button and preview button
    """

    logger.info("1. Open the enuygun.com home page and click round trip")
    driver = webdriver.Chrome()
    driver.maximize_window()
    home_page = HomePage(driver)
    home_page.click_round_trip()

    logger.info("2. Enter flight origin and click origin autosuggestion option")
    home_page.enter_flight_origin("İstanbul")
    home_page.click_origin_autosuggestion_option()
    assert "İstanbul" in home_page.get_origin_text(), "Flight origin is not set correctly"

    logger.info("3. Enter flight destination and click destination autosuggestion option")
    home_page.enter_flight_destination("Ankara")
    home_page.click_destination_autosuggestion_option()
    assert "Ankara" in home_page.get_destination_text(), "Flight origin is not set correctly"

    logger.info("4. Click departure date and select departure date")
    home_page.click_departure_date()
    home_page.select_departure_date("Mayıs 2024", "30")
    assert "30 May" in home_page.get_departure_date(), "Departure date is not set correctly"

    logger.info("5. Click return date and select return date")
    home_page.click_return_date()
    home_page.select_return_date("Haziran 2024", "30")
    assert "30 Haz" in home_page.get_return_date(), "Return date is not set correctly"

    logger.info("6. Click flight submit button")
    home_page.click_flight_submit_button()
    assert home_page.is_flight_search_submitted(), "Flight search is not submitted"

    logger.info("7. Click next button and preview button")
    search_result_page = FlightSearchResultPage(driver)
    search_result_page.click_next_button()
    flight_list_date = search_result_page.get_flight_list_date()
    assert flight_list_date == "31 May 2024, Cum", "Flight list date does not match the expected value"
    search_result_page.click_preview_button()
    flight_list_date = search_result_page.get_flight_list_date()
    assert flight_list_date == "30 May 2024, Per", "Flight list date does not match the expected value"

    logger.info("Test completed successfully!")
    driver.quit()