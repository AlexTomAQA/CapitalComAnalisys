"""
-*- coding: utf-8 -*-
@Time    : 2024/04/02 16:00
@Author  : Artem Dashkov
"""
# from datetime import datetime

# import allure
import pytest
from selenium.webdriver.common.by import By
# from selenium import webdriver

from pages.base_page import BasePage
# from pages.common import Common


class TradingViewLocators:
    APP_TITLE = ('css selector', '.tv-profile-header__username')
    BUTTON_SEARCH_MARKETS_HERE = (By.CSS_SELECTOR, "button.searchBar-PCujdK9L")
    SEARCH_TEXT_BOX = (By.CSS_SELECTOR, 'input[inputmode="search"]')
    CLEAR_BUTTON = (By.CSS_SELECTOR, "button.clearButton-KLRTYDjH")
    BROKER_LIST = (By.CSS_SELECTOR, ".itemRow-oRSs8UQo .exchangeName-oRSs8UQo")
    LIST_ALL_BROKERS = (By.CSS_SELECTOR, ".listContainer-dlewR1s1")


class TradingView(BasePage):
    def go_to_search_markets_here(self):

        if not self.element_is_visible(TradingViewLocators.BUTTON_SEARCH_MARKETS_HERE, 10):
            self.driver.refresh()
            if not self.element_is_visible(TradingViewLocators.BUTTON_SEARCH_MARKETS_HERE, 10):
                msg = "Проблема с главной кнопкой SEARCH MARKETS"
                print(msg)
                pytest.fail(msg)

        buttons = self.driver.find_elements(*TradingViewLocators.BUTTON_SEARCH_MARKETS_HERE)
        if len(buttons) == 0:
            msg = "Нет кнопки Поиска Рынка"
            print(msg)
            pytest.fail(msg)

        buttons[0].click()

        if not self.element_is_visible(TradingViewLocators.LIST_ALL_BROKERS, 15):
            msg = "Проблема со списком Брокеров"
            print(msg)
            pytest.fail(msg)

        return True

    def search_markets(self, ti):
        if not self.element_is_visible(TradingViewLocators.CLEAR_BUTTON, 5):
            print("Проблема с кнопкой очистки строки поиска")
            return False

        button = self.driver.find_element(*TradingViewLocators.CLEAR_BUTTON)
        button.click()

        buttons = self.driver.find_elements(*TradingViewLocators.SEARCH_TEXT_BOX)
        if len(buttons) == 0:
            msg = "Нет поля Search"
            print(msg)
            pytest.fail(msg)

        buttons[0].send_keys(ti)
        return True

    def get_place_for_broker(self, broker):
        broker_list = self.driver.find_elements(*TradingViewLocators.BROKER_LIST)
        qty = len(broker_list)
        place = 0
        for i in range(qty):
            if broker_list[i].text == broker:
                place = i + 1
                break
            # i += 1

        return place, qty
