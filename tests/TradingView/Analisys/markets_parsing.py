""""
-*- coding: utf-8 -*-
@Time    : 2024/07/05 22:00
@Author  : Alexander Tomelo
"""
from datetime import datetime
import time

# import pytest
# import allure
# from selenium.common.exceptions import ElementClickInterceptedException
from pages.base_page import BasePage
from pages.TradingView.trading_view import TradingView
from pages.GoogleSheets.googlesheets import GoogleSheet

page_tr_v = None
broker = "CAPITALCOM"
new_row = "4"
cur_column = "B"


class TestTradingView:

    def test_analisys(self, d, gs, cur_trading_instrument, file):
        """
        Полный алгоритм действий с полученным TI
        """
        global page_tr_v
        global new_row
        global cur_column

        # Arrange
        href = "https://www.tradingview.com/"

        if d.current_url != href:
            page_tr_v = BasePage(d, href)
            page_tr_v.open_page()
            page_tr_v = TradingView(d, href)
            page_tr_v.go_to_search_markets_here()

        # Action
        page_tr_v.search_markets(cur_trading_instrument)
        time.sleep(1)

        place, qty = page_tr_v.get_place_for_broker(broker)
        gs_out = [str(place)]
        cell = cur_column + new_row
        gs.update_range_values(cell, [gs_out])

        file.write(f"{datetime.now()}\t"
                   f"Столбец: '{cur_column}'\t"
                   f"{cur_trading_instrument}:\t\t"
                   f"{broker} занимает {place} место из {qty}\n")

        print(f"{broker} занимает {place} место из {qty}")
        cur_column = chr(ord(cur_column) + 1)
