""""
-*- coding: utf-8 -*-
@Time    : 2024/07/05 22:00
@Author  : Alexander Tomelo
"""
from datetime import datetime
import time
#
# import pytest
# import allure
# from selenium.common.exceptions import ElementClickInterceptedException
from pages.base_page import BasePage
from pages.TradingView.tradingview import TradingView

page_tv = None
broker = "CAPITALCOM"


class TestTradingView:

    def test_analisys(self, d, cur_rnd_trading_instrument, file):
        """
        Полный алгоритм действий с полученным TI
        """
        global page_tv
        # Arrange
        href = "https://www.tradingview.com/"

        if d.current_url != href:
            page_tv = BasePage(d, href)
            page_tv.open_page()
            page_tv = TradingView(d, href)
            page_tv.go_to_search_markets_here()

        # Act
        page_tv.search_markets(cur_rnd_trading_instrument)
        # time.sleep(1)

        # Assert
        place, qty = page_tv.get_place_for_broker(broker)
        file.write(f"{datetime.now()}\t"
                   f"{cur_rnd_trading_instrument}:\t\t"
                   f"{broker} занимает {place} место из {qty}\n")

        print(f"{broker} занимает {place} место из {qty}")
