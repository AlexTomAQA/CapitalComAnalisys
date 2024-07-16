"""
-*- coding: utf-8 -*-
@Time    : 2024/07/15 22:00
@Author  : Alexander Tomelo
"""

import pytest
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.TradingView.trading_view import TradingViewLocators

class MainMenuLocators():
    MENU_BROKERS = (By.CSS_SELECTOR, "[data-main-menu-root-track-id='brokers']")
    SEARCH_BOX = (By.CSS_SELECTOR, ".tv-header-search-container__text")


class MainMenu(BasePage):

    def move_focus_onto_menu_markets_and_click(self):

        if not self.element_is_visible(MainMenuLocators.MENU_BROKERS, 10):
            print("Проблема с Menu")
            return False
        menu = self.driver.find_element(*MainMenuLocators.MENU_BROKERS)
        menu.click()

    def move_focus_onto_search_box_and_click(self):
        if not self.element_is_visible(MainMenuLocators.SEARCH_BOX, 10):
            msg = "Отсутствует поле поиска 'Search (Ctrl+K)'"
            print(msg)
            pytest.fail(msg)

        search_box = self.driver.find_element(*MainMenuLocators.SEARCH_BOX)
        search_box.click()

        if not self.element_is_visible(TradingViewLocators.LIST_ALL_BROKERS, 10):
            msg = "Проблема со списком Брокеров"
            print(msg)
            pytest.fail(msg)

        return True
