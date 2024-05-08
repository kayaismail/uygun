from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class Base():

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def click_element(self, locator):
        """
        Clicks the element
        :param locator: element locator

        """
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            print(locator,"Element clicked successfully.")
        except Exception as e:
            print("An error occurred while clicking the element:", str(e))
            print("Failed at locator:", locator)
            raise AssertionError("Clicking the element failed at locator:", locator)

    def navigate_url(self, url):
        """
        Browse current window to requested url.
        :param str url: Requested URL of the site to be redirected

        """
        self.driver.get(url)

    def enter_text(self, locator, text):
        """
        Enters the text to the element
        :param locator: element locator
        :param text: text to be entered

        """
        try:
            element = self.wait_for_element_to_be_visible(locator)
            element.clear()
            element.send_keys(text)
            print("Text entered successfully.")
        except Exception as e:
            print("An error occurred while entering text:", str(e))
            print("Failed at locator:", locator)
            raise AssertionError("Text entry failed at locator:", locator)

    def click_element_by_index(self, locator, index=0):
        """
        Clicks the element at the specified index if multiple elements are found.
        If only one element is found, clicks that element.
        :param locator: Locator of the elements.
        :param index: Index of the element to click.

        """
        try:
            elements = self.wait_for_elements_to_be_visible(locator)
            if len(elements) > 1:
                elements[index].click()
            elif elements:
                elements[0].click()
        except IndexError:
            print(f"No element found with index {index}")
        except Exception as e:
            raise Exception("An error occurred while trying to click the element.") from e

    def wait_for_element_to_be_visible(self, locator, timeout=10):
        """
        Wait for element to be visible
        :param locator: element locator
        :param timeout: int Maximum time you want to wait for the element

        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except Exception as e:
            raise Exception("Element not visible after {} seconds".format(timeout)) from e

    def wait_for_elements_to_be_visible(self, locator, timeout=10):
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_any_elements_located(locator)
            )
            return elements
        except Exception as e:
            raise Exception("Elements not visible after {} seconds".format(timeout)) from e

    def wait_for_element_invisible(self, locator, timeout=20):
        """
        Wait for element to be invisible
        :param locator: locator of the element to find
        :param int timeout: Maximum time you want to wait for the element

        """
        try:
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
            print("Element is now invisible.")
        except TimeoutException:
            print("Element is still visible after {} seconds.".format(timeout))
