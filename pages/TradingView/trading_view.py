"""
-*- coding: utf-8 -*-
@Time    : 2024/04/02 16:00
@Author  : Artem Dashkov
"""
from datetime import datetime

import allure
import pytest
from selenium.webdriver.common.by import By
# from selenium import webdriver

from pages.base_page import BasePage
from pages.common import Common
from test_data.tradingview_site_data import data


class TradingViewSiteLocators:
    APP_TITLE = ('css selector', '.tv-profile-header__username')
    BUTTON_SEARCH_MARKETS_HERE = (By.CSS_SELECTOR, "button.searchBar-PCujdK9L")
    SEARCH_TEXT_BOX = (By.CSS_SELECTOR, 'input[inputmode="search"]')
    CLEAR_BUTTON = (By.CSS_SELECTOR, "button.clearButton-KLRTYDjH")
    BROKER_LIST = (By.CSS_SELECTOR, ".itemRow-oRSs8UQo .exchangeName-oRSs8UQo")
    LIST_ALL_BROKERS = (By.CSS_SELECTOR, ".listContainer-dlewR1s1")


class TradingView(BasePage):
    @allure.step("Checking that the TradingView site has opened")
    def should_be_tradingview_page(self):
        """Check if the page is open"""
        print(f"{datetime.now()}   Checking that the TradingView page has opened =>")
        if self.current_page_url_contain_the(data["SITE_URL"]):
            print(f"{datetime.now()}   => TradingView page has opened\n")
            self.should_be_page_title_v3(data["PAGE_TITLE"])
            self.should_be_tradingview_site_app_title(data["APP_TITLE"])
            return True
        else:
            print(f"{datetime.now()}   TradingView site not opened")
            return False

    @allure.step("Checking that the TradingView site has expected app title")
    def should_be_tradingview_site_app_title(self, expected_app_title):
        """Check the app on the page has expected app title"""
        print(f"{datetime.now()}   Checking that the TradingView site has expected app title =>")
        current_app_title = self.get_text(0, *TradingViewSiteLocators.APP_TITLE)
        print(f"{datetime.now()}   The app title of current page is '{current_app_title}'")
        print(f"{datetime.now()}   The expected app title is '{expected_app_title}'")

        # Check that the app title of current page meets the requirements
        Common().assert_true_false(
            expected_app_title in current_app_title,
            f"{datetime.now()}   Expected title '{expected_app_title}' "
            f"but got '{current_app_title}' on page: {self.driver.current_url}"
        )
        print(f"{datetime.now()}   => The app title has expected title.\n")

    def go_to_search_markets_here(self):

        if not self.element_is_visible(TradingViewSiteLocators.BUTTON_SEARCH_MARKETS_HERE, 15):
            msg = "Проблема с главной кнопкой SEARCH MARKETS"
            print(msg)
            pytest.fail(msg)

        buttons = self.driver.find_elements(*TradingViewSiteLocators.BUTTON_SEARCH_MARKETS_HERE)
        if len(buttons) == 0:
            msg = "Нет кнопки Поиска Рынка"
            print(msg)
            pytest.fail(msg)

        buttons[0].click()

        if not self.element_is_visible(TradingViewSiteLocators.LIST_ALL_BROKERS, 15):
            msg = "Проблема со списком Брокеров"
            print(msg)
            pytest.fail(msg)

        return True

    def search_markets(self, ti):
        if not self.element_is_visible(TradingViewSiteLocators.CLEAR_BUTTON, 5):
            print("Проблема с кнопкой очистки строки поиска")
            return False

        button = self.driver.find_element(*TradingViewSiteLocators.CLEAR_BUTTON)
        button.click()

        buttons = self.driver.find_elements(*TradingViewSiteLocators.SEARCH_TEXT_BOX)
        if len(buttons) == 0:
            msg = "Нет поля Search"
            print(msg)
            pytest.fail(msg)

        buttons[0].send_keys(ti)
        return True

    def get_place_for_broker(self, broker):
        broker_list = self.driver.find_elements(*TradingViewSiteLocators.BROKER_LIST)
        qty = len(broker_list)
        place = 0
        for i in range(qty):
            if broker_list[i].text == broker:
                place = i + 1
                break
            # i += 1

        return place, qty
