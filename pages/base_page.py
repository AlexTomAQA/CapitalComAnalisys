import logging
import time

import allure
from datetime import datetime

import pytest
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
    NoSuchAttributeException,
    ElementNotInteractableException,
    InvalidElementStateException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC

from pages.Capital.capital_locators import OnTrustLocators, Captcha
from pages.common import Common

# from src.src import (
#     CapitalComPageSrc,
# )


class HandleExcElementsDecorator(object):
    """A decorator that handles exceptions related to elements on a webpage."""

    def __init__(
            self,
            driver="self",
            timeout=0.5,
            title="title",
            value="value",
            property_atr="property",
            method="a",
            locator="b",
            index=0,
    ):
        """Initializes the object.

        Args:
            driver: WebDriver. Defaults to 'self'.
            timeout (optional): the time to wait for an element to be present on the
            page before throwing a TimeoutException. Defaults to 0.5.
            title (optional): the title of the page. Defaults to 'title'.
            value (optional): the value to send to the element. Defaults to 'value'.
            'property' (optional): the property of the element. Defaults to 'property'.
            method (optional): used for locating the element on the page. Defaults to 'a'.
            locator (optional): used with the specified method to find the element. Defaults to 'b'.
            index (optional): extract all elements of the list of individual lines of text starting from the
                ith element. Defaults to 0.
        """
        self.driver = driver
        self.timeout = timeout
        self.title = title
        self.value = value
        self.property_atr = property_atr
        self.method = method
        self.locator = locator
        self.index = index

    def __call__(self, func):
        """Define an inner function that wraps the original function or method.

        Args:
            func (function): the original function or method to be decorated.

        Raises:
            NoSuchElementException: if the elements are not found on the page
            TimeoutException: when there is no match with at least one element even after wait time
            NoSuchAttributeException: if the attribute of the elements is not found
            ElementNotInteractableException: if the elements are not currently interactable
            InvalidElementStateException: if the element are in an invalid state
            StaleElementReferenceException: if the elements are no longer attached to the DOM
            WebDriverException:  if an error occurs while initializing the WebDriver
        """
        decorator_self = self

        def inner_function(*args, **kwargs):
            self.driver = args[0].driver
            try:
                return func(*args, **kwargs)
            except NoSuchElementException as e:
                logging.error(
                    f"Could not find elements on page: {decorator_self.driver.current_url}"
                )
                logging.exception(e.msg)
            except TimeoutException as e:
                logging.error(
                    f"Elements not present after {decorator_self.timeout} "
                    f"seconds on page: {decorator_self.driver.current_url}"
                )
                logging.exception(e.msg)
            except NoSuchAttributeException as e:
                logging.error(
                    f"The attribute of elements could not be found on page: {decorator_self.driver.current_url}"
                )
                logging.exception(e.msg)
            except ElementNotInteractableException as e:
                logging.error(
                    f"The element is not currently interactable on page: {decorator_self.driver.current_url}"
                )
                logging.exception(e.msg)
            except InvalidElementStateException as e:
                logging.error(
                    f"The element is in an invalid state on page: {decorator_self.driver.current_url}"
                )
                logging.exception(e.msg)
            except StaleElementReferenceException as e:
                logging.error(
                    f"The elements are no longer attached to the DOM on page: {decorator_self.driver.current_url}"
                )
                logging.exception(e.msg)
            except WebDriverException as e:
                logging.error("Unable to initialize WebDriver")
                logging.exception(e.msg)

        return inner_function


class BasePage:
    """This class used as a base class for other page classes that represent specific pages on a website"""

    def __init__(self, driver, link="", bid=""):
        """
        Initializes the object.

        Args:
            driver: WebDriver
            link: URL
            bid: ID bug
        """
        self.driver = driver
        self.link = link
        self.bid = bid

    # @allure.step(f"Load page {self.link}")
    def open_page(self):
        """
        Navigates to a page given by the URL.
        """
        print(f"{datetime.now()}   Current page URL = {self.driver.current_url}")
        print(f"{datetime.now()}   self.link = {self.link}")
        link = self.link
        print(f"{datetime.now()}   driver.get({link}) =>")
        self.driver.get(link)
        time.sleep(1)
        print(f"{datetime.now()}   => Loaded page {self.driver.current_url}")

    @HandleExcElementsDecorator()
    def button_accept_all_cookies_click(self):
        allure.step(f"{datetime.now()}   Start Accepting all cookies")

        time_out = 30
        print(f"\n{datetime.now()}   Step 'Click button [Accept all cookies]'")

        # self.is_captcha()

        print(f"{datetime.now()}   Is Visible Button [Accept all cookies]? =>")
        button = self.element_is_visible(OnTrustLocators.BUTTON_ACCEPT_ALL_COOKIE, time_out)
        if not button:
            print(f"{datetime.now()}   => Button [Accept all cookies] is not visible after {time_out} sec.")
            print(f"{datetime.now()}   => Cur url = {self.driver.current_url}")
            assert False, f"Button [Accept all cookies] is not visible after {time_out} sec."
        else:
            print(f"{datetime.now()}   => Button [Accept all cookies] is visible")

        time.sleep(0.5)

        print(f"{datetime.now()}   Is clickable Button [Accept all cookies] =>")
        button = self.driver.find_element(*OnTrustLocators.BUTTON_ACCEPT_ALL_COOKIE)
        button = self.element_is_clickable(button, time_out)
        if not button:
            print(f"{datetime.now()}   => Button [Accept all cookies] is not clickable after {time_out} sec.")
            print(f"{datetime.now()}   => Cur url = {self.driver.current_url}")
            assert False, f"Button [Accept all cookies] is not clickable after {time_out} sec."
        else:
            print(f"{datetime.now()}   => Button [Accept all cookies] is clickable")

        print(f"{datetime.now()}   Click Button [Accept all cookies] =>")
        button = self.driver.find_element(*OnTrustLocators.BUTTON_ACCEPT_ALL_COOKIE)
        button.click()
        print(f"{datetime.now()}   => Button [Accept all cookies] is clicked")
        print(f"{datetime.now()}   => Accepted All Cookies")
        time.sleep(0.5)

    @allure.step(f"{datetime.now()}   Reject all cookies")
    @HandleExcElementsDecorator()
    def button_reject_all_cookies_click(self):
        print(f"\n"
              f"{datetime.now()}   Is visible BUTTON_REJECT_ALL_COOKIE? =>")
        self.element_is_visible(OnTrustLocators.BUTTON_REJECT_ALL_COOKIE, 30)
        print(f"{datetime.now()}   Find BUTTON_REJECT_ALL_COOKIE =>")
        button = self.driver.find_element(*OnTrustLocators.BUTTON_REJECT_ALL_COOKIE)
        print(f"{datetime.now()}   Is clickable BUTTON_REJECT_ALL_COOKIE? =>")
        self.element_is_clickable(button, 30)
        time.sleep(1)
        print(f"{datetime.now()}   Click BUTTON_REJECT_ALL_COOKIE =>")
        button.click()
        print(f"{datetime.now()}   => Rejected All Cookies")

    @HandleExcElementsDecorator()
    def element_is_present(self, method, locator):
        """
        Find an element given a By method and locator.

        Args:
            method: used for locating the element on the page
            locator: used with the specified method to find the element

        Returns:
            bool: True if the element is located in a page. False if the element could not be found
        Raises:
            InvalidElementStateException: if the element is in an invalid state
            NoSuchElementException: if the element cannot be found on the page
            WebDriverException:  if an error occurs while initializing the WebDriver
        """
        return self.driver.find_element(method, locator)

    @HandleExcElementsDecorator()
    def elements_are_present(self, method, locator):
        """
        Find elements given a By method and locator.

        Args:
            method: used for locating the element on the page
            locator: used with the specified method to find the element

        Returns:
            list[selenium.webdriver.remote.webelement.WebElement]:
                list of found WebElement or empty if elements are not found
        Raises:
            NoSuchElementException: if the elements are not found on the page
            StaleElementReferenceException: if the elements are no longer attached to the DOM
            WebDriverException: if an error occurs while initializing the WebDriver
        """
        return self.driver.find_elements(method, locator)

    @HandleExcElementsDecorator()
    def send_keys(self, value, method, locator):
        """
        Sends keys to an element given a By method and locator.

        Args:
            value: the value to send to the element
            method: used for locating the element on the page
            locator: used with the specified method to find the element
        """
        list_of_elements = self.driver.find_elements(method, locator)
        if len(list_of_elements) == 0:
            print(f"{datetime.now()}   => TextBox with '{locator}' locator is not present")
            return False
        list_of_elements[0].send_keys(value)
        return True

    @HandleExcElementsDecorator()
    def get_attribute(self, attribute, method, locator):
        """
        Gets the given property of the element.

        Args:
            attribute: name of the attribute to retrieve
            method: used for locating the element on the page
            locator: used with the specified method to find the element
        Returns:
            str | bool | WebElement | dict: the value of the attribute with the given name or None,
                if there's no attribute
                with that name
        """
        return self.driver.find_element(method, locator).get_attribute(attribute)

    @HandleExcElementsDecorator()
    def get_property(self, property_atr, method, locator):
        """
        Gets the given property of the element.

        Args:
            property_atr: name of the property to retrieve
            method: used for locating the element on the page
            locator: used with the specified method to find the element
        Returns:
            str | bool | WebElement | dict: the value of a property with the given name or None if there's no property
                with that name
        """
        return self.driver.find_element(method, locator).get_property(property_atr)

    @HandleExcElementsDecorator()
    def element_is_visible(self, locator, timeout=1):
        """
        Check that an element is present on the DOM of a page and visible.
        Visibility means that the element is not only displayed but also has a height and width that is greater than 0.

        Args:
            locator: used to find the element; a tuple of 'by' and 'path'
            timeout (optional): specified time duration before throwing a TimeoutException. Defaults to 1.

        Returns:
            selenium.webdriver.remote.webelement.WebElement: it is located and visible
            None: if not
        """
        return Wait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @HandleExcElementsDecorator()
    def element_visibility_of(self, web_element, timeout=1):
        """
        Check that an element is present on the DOM of a page and visible.
        Visibility means that the element is not only displayed but also has a height and width that is greater than 0.

        Args:
            web_element: web element
            timeout (optional): specified time duration before throwing a TimeoutException. Defaults to 1.

        Returns:
            selenium.webdriver.remote.webelement.WebElement: it is located and visible
            None: if not
        """
        return Wait(self.driver, timeout).until(
            EC.visibility_of(web_element)
        )

    def element_is_present_and_visible(self, locator, timeout=5):
        self.go_to_element(self.element_is_presented(locator))
        return Wait(self.driver, timeout).until(EC.visibility_of_element_located(locator),
                                                message=f"Can't see element by locator {locator}")

    @HandleExcElementsDecorator()
    def element_is_present_and_visible_v2(self, locator, name_of_element, timeout=5):
        """
        Check that an element is present on the DOM of a page and visible. For v2: Add time-code for message.
        Visibility means that the element is not only displayed but also has a height and width that is greater than 0.

        Example of used:
            BLOCK_NAME = '"What is your sentiment?" block'
            BLOCK_LOCATOR = (By.CSS_SELECTOR, '.sentiment[data-type="bullBearWidget"]')

            element_is_present_and_visible_v2(BLOCK_LOCATOR, BLOCK_NAME, 3)

        Args:
            locator: used with the specified method to find the element
            name_of_element: name of web element that we are testing
            timeout (optional): specified time duration before throwing a TimeoutException. Defaults to 1.

        Returns:
            'True' if element is present and visible
            pytest_fail(msg) - if not present or not visible
        """
        print(f"{datetime.now()}   IS {name_of_element} present on this page? =>")
        if len(self.driver.find_elements(*locator)) == 0:
            msg = f"{name_of_element} is NOT present on this page"
            print(f"{datetime.now()}   => {msg}\n")
            Common().pytest_fail(msg)
        print(f"{datetime.now()}   => {name_of_element} present on this page!\n")

        self.driver.execute_script(
            'return arguments[0].scrollIntoView({block: "center", inline: "nearest"});',
            self.driver.find_elements(*locator)[0]
        )

        print(f"{datetime.now()}   IS {name_of_element} visible on this page? =>")
        if not self.element_is_visible(locator, timeout):
            msg = f"{name_of_element} is NOT visible on this page!"
            print(f"{datetime.now()}   => {msg}\n")
            Common().pytest_fail(msg)
        print(f"{datetime.now()}   => {name_of_element} is visible on this page!\n")
        return True

    @HandleExcElementsDecorator()
    def element_is_clickable(self, loc_or_elem, timeout=1):
        """
        Check that an element is present on the DOM of a page and enabled such that you can click it..
        Visibility means that the element is not only displayed but also has a height and width that is greater than 0.

        Args:
            loc_or_elem: used to find the element; a tuple of 'by' and 'path' or webelement
            timeout (optional): specified time duration before throwing a TimeoutException. Defaults to 1.
        Returns:
            selenium.webdriver.remote.webelement.WebElement: it is located and visible
            False: not clickable
        """
        return Wait(self.driver, timeout).until(
            EC.element_to_be_clickable(loc_or_elem),
            message=f"Can't click element by locator {loc_or_elem}"
        )

    @HandleExcElementsDecorator()
    def elements_are_located(self, locator, timeout=5):
        """
        Check that there is at least one element, located by the locator, present on a web page.

        Args:
            locator: used to find the element; a tuple of 'by' and 'path'
            timeout (optional): specified time duration before throwing a TimeoutException. Defaults to 5.
        Returns:
            list[selenium.webdriver.remote.webelement.WebElement]: the list of all matched WebElements
        """
        return Wait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    @HandleExcElementsDecorator()
    def element_is_located(self, locator, timeout=1):
        """
        Check that an element is present on the DOM of a page.

        Args:
            locator: used to find the element; a tuple of 'by' and 'path'
            timeout (optional): specified time duration before throwing a TimeoutException. Defaults to 1.
        Returns:
            selenium.webdriver.remote.webelement.WebElement: returns the WebElement located
        """
        return Wait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    @HandleExcElementsDecorator()
    def current_page_is(self, link):
        print(f"{datetime.now()}   current_page = {self.driver.current_url}")
        print(f"{datetime.now()}   link = {link}")
        return link == self.driver.current_url

    @HandleExcElementsDecorator()
    def current_page_url_contain_the(self, host):
        cur_url = self.driver.current_url
        result = host in cur_url
        return result

    @HandleExcElementsDecorator()
    @allure.step("Check the current page has URL: '{link}'")
    def check_current_page_is(self, link):
        print(f"{datetime.now()}   Cur page is {link}? =>")
        assert (self.driver.current_url == link), f"Expected page: {link}. Actual page: {self.driver.current_url}"
        print(f"{datetime.now()}   => Cur page is {link}")

    @HandleExcElementsDecorator()
    @allure.step("Check the current page has expected URL")
    def check_current_page_is_v2(self, expected_url):
        """
        Check that the current page has the expected URL.

        Args:
            expected_url: expected page's URL
        """
        print(f"{datetime.now()}   Checking that the current page has URL: {expected_url} =>")
        current_url = self.driver.current_url
        print(f"{datetime.now()}   => The current page URL is {current_url}")
        # Checks that the page URL meets the requirements
        Common.assert_true_false(
            current_url in expected_url,
            f"{datetime.now()}   Expected page: {expected_url}. Actual page: {self.driver.current_url}"
        )

    @HandleExcElementsDecorator()
    @allure.step("Check, that the link provided is in the current URL of the browser")
    def should_be_link(self, link):
        """
        Check that the link provided is in the current URL of the browser.

        Args:
            link: link browser
        """
        assert (
                link == self.driver.current_url
        ), f"Expected link {link} not found in URL {self.driver.current_url}"

    @HandleExcElementsDecorator()
    def should_be_page_title(self, title, method, locator):
        """
        Check that the page has the expected title given a By method and locator.

        Args:
            title: page's title
            method: used for locating the element on the page
            locator: used with the specified method to find the element
        """
        el_title = self.driver.find_element(method, locator)
        # Gets the page title element
        assert el_title, f"Title element not found on page: {self.driver.current_url}"
        # Checks that the page title element meets the requirements
        assert (
                el_title.text == title
        ), f"Expected title {title} but got {el_title.text} on page: {self.driver.current_url}"

    @HandleExcElementsDecorator()
    @allure.step(f"{datetime.now()}   Check that the page has the expected title - ver 2")
    def should_be_page_title_v2(self, title):
        """
        Check that the page has the expected title.

        Args:
            title: expected page's title
        """
        print(f"\n{datetime.now()}"
              f"   1. Checking that the Trading platform (or TradingView site) page has valid title =>")
        el_title = self.driver.title
        print(f"{datetime.now()}   => The title of current page is '{el_title}'")
        # Checks that the page title meets the requirements
        if title not in el_title:
            msg = f"Bug # ??? Expected title '{title}' but got '{el_title}' on page: {self.driver.current_url}"
            Common().assert_true_false(False, msg)

    @HandleExcElementsDecorator()
    @allure.step(f"{datetime.now()}   Check that the page has the expected title - ver 3")
    def should_be_page_title_v3(self, expected_title):
        """
        Check that the page has the expected title.

        Args:
            expected_title: expected page's title
        """
        print(f"\n{datetime.now()}"
              f"   Checking that the page has expected title =>")
        current_title = self.driver.title
        print(f"{datetime.now()}   The title of current page is '{current_title}'")
        print(f"{datetime.now()}   The expected title is '{expected_title}'")
        # Check that the page title meets the requirements
        Common().assert_true_false(
            expected_title in current_title,
            f"{datetime.now()}   "
            f"=> Expected title '{expected_title}' but got '{current_title}' on page: {self.driver.current_url}\n"
        )
        print(f"{datetime.now()}   => The page has expected title.\n")

    @HandleExcElementsDecorator()
    def get_text(self, i, method, locator):
        """
        Extract a specific part of the text from the element given a By method and locator.

        Args:
            i: extract all elements of the list of individual lines of text starting from the ith element
            method: used for locating the element on the page
            locator: used with the specified method to find the element
        Returns:
            str: the text of the element
        """
        return "".join(self.driver.find_element(method, locator).text.split("\n")[i:])

    @HandleExcElementsDecorator()
    def click_button(self, method, locator):
        """
        Clicks the element given a By method and locator.

        Args:
            method: used for locating the element on the page
            locator: used with the specified method to find the element
        """
        self.driver.find_element(method, locator).click()

    @HandleExcElementsDecorator()
    def get_src(self, i, method, locator):
        """
        Extract the src attribute of an element given a By method and locator.
        The src attribute specifies the URL of an image or other media file.

        Args:
            i: extract all elements of the list of individual lines of text starting from the ith element
            method: used for locating the element on the page
            locator: used with the specified method to find the element
        Returns:
            str: the src of the element
        Raises:
            NoSuchElementException: if the element cannot be found on the page
            NoSuchAttributeException: if the attribute of the element is not found
            StaleElementReferenceException: if the elements are no longer attached to the DOM
            InvalidElementStateException: if the element is in an invalid state
            WebDriverException: if an error occurs while initializing the WebDriver
        """
        return "".join(
            self.driver.find_element(method, locator)
            .get_property("src")
            .split("\n")[i:]
        )

    @HandleExcElementsDecorator()
    def get_text_elements(self, i, method, locator):
        """
        Extract the substrings of the text from the elements given a By method and locator.
        Args:
            i: substring starts at the i-th character and continues to the end of the text
            method: used for locating the element on the page
            locator: used with the specified method to find the element
        Returns:
            list[str]: the list of substring of the element's text
        Raises:
            NoSuchElementException: if the elements are not found on the page
            StaleElementReferenceException: if the elements are no longer attached to the DOM
            WebDriverException:  If an error occurs while initializing the WebDriver
        """
        list_prices = self.driver.find_elements(method, locator)
        return list(map(lambda element: element.text[i:], list_prices))

    @HandleExcElementsDecorator()
    def wait_for_change_url(self, cur_link, timeout=1):
        """
        Waiting for url change
        Args:
            cur_link: the current url that needs to change
            timeout (optional): specified time duration before throwing a TimeoutException. Defaults to 1.

        """
        return Wait(self.driver, timeout).until(
            EC.url_changes(cur_link)
        )

    @HandleExcElementsDecorator()
    def wait_for_target_url(self, link, timeout=1):
        """
        Waiting for target url
        Args:
            link: the target url that we are waiting for
            timeout (optional): specified time duration before throwing a TimeoutException. Defaults to 1.

        """
        return Wait(self.driver, timeout).until(
            EC.url_contains(link)
        )

    @HandleExcElementsDecorator()
    def is_captcha(self):
        if self.elements_are_visible(Captcha.CAPTCHA_IFRAME, 1):
            pytest.fail("Captcha on the page")

    # def flatten(self, mylist):
    #     """
    #     Unpacks list of lists of elements into a single, flat list of elements
    #
    #     Args:
    #         mylist: the list of the lists of WebElements.
    #     Returns:
    #         list[selenium.webdriver.remote.webelement.WebElement]: the list of WebElements.
    #     """
    #     return [item for sublist in mylist for item in sublist]
    #

    def go_to_element(self, element):
        self.driver.execute_script(
            'return arguments[0].scrollIntoView({block: "center", inline: "nearest"});', element)

    def element_is_presented(self, locator, timeout=10):
        return Wait(self.driver, timeout).until(EC.presence_of_element_located(locator),
                                                message=f"Element not present by locator {locator}")

    def elements_are_visible(self, locator, timeout=5):
        return Wait(self.driver, timeout).until(EC.visibility_of_any_elements_located(locator),
                                                message=f"Can't see element by locator {locator}")

    @HandleExcElementsDecorator()
    def element_is_selected(self, method, locator):
        """
       Shows that element is selected By method and locator.

        Args:
            method: used for locating the element on the page
            locator: used with the specified method to find the element
        """
        return self.driver.find_element(method, locator).is_enabled()

    @HandleExcElementsDecorator()
    def specific_locator(self, locator, number):
        """
        Creates new locator with use specific item number of element from all found elements

        Args:
            locator: used to find all elements on the page; a tuple of 'by' and 'path'
            number: specific item number of element from all found elements
        Returns:
            selenium.webdriver.remote.webelement.WebElement: returns the WebElement located
        """
        if locator[0] == By.XPATH:
            new_locator = (locator[0], f'{locator[1]}[{number}]' )
            return new_locator
        else:
            pass
