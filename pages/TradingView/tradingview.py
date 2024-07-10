"""
-*- coding: utf-8 -*-
@Time    : 2024/04/02 16:00
@Author  : Artem Dashkov
"""
from datetime import datetime

import allure
import pytest
# from selenium import webdriver

from pages.base_page import BasePage
from pages.common import Common
from test_data.tradingview_site_data import data


class TradingViewSiteLocators:
    APP_TITLE = ('css selector', '.tv-profile-header__username')
    BUTTON_SEARCH_MARKETS_HERE = ("css selector", "button.searchBar-PCujdK9L")
    SEARCH_TEXT_BOX = ("css selector", 'input[inputmode="search"]')
    CLEAR_BUTTON = ("css selector", "button.clearButton-KLRTYDjH")
    BROKER_LIST = ("css selector", ".itemRow-oRSs8UQo .exchangeName-oRSs8UQo")


class TradingView(BasePage):
    @allure.step("Checking that the TradingView site has opened")
    def should_be_tradingview_page(self, d):
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
        buttons = self.driver.find_elements(*TradingViewSiteLocators.BUTTON_SEARCH_MARKETS_HERE)
        if len(buttons) == 0:
            msg = "Нет кнопки Поиска Рынка"
            print(msg)
            pytest.fail(msg)

        buttons[0].click()

        return True

    def search_markets(self, ti):
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
