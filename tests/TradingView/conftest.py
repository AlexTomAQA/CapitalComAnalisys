"""
-*- coding: utf-8 -*-
@Time    : 2024/07/05 20:30
@Author  : AlexTomQA
"""

import pytest
import random


@pytest.fixture(
    scope="function",
    # params=random.sample([
    params=[
        "GOLD",
        "GBPUSD",
        "EURUSD",
        "NZDUSD",
        "EURUSD",
        "USDJPY",
        "AUDUSD",
        "GBPUSD",
        "USDCHF",
        "USDMXN",
        "EURGBP",
        "USDZAR",
        "GBPAUD",
        "BTCUSD",
        "XRPUSD",
        "DOGEUSD",
        "ADABTC",
        "MATICUSD",
        "US30",
        "UK100",
        "VIX",
        "GOLD",
        "SILVER",
        "COPPER",
        "CORN",
        "WHEAT",
        # ], 26),  # 26
    ],  # 26
)
def cur_rnd_trading_instrument(request):
    print(f"Current trading instrument - {request.param}\n")
    return request.param


@pytest.fixture(
    scope="module",
    params=[
        "Chrome",
        # "Edge",
        # "Firefox",
        # "Safari",
    ],
    autouse=True,
)
def file(request):
    """File Initialization"""
    file_name = "/Users/alekstom/Projects/TestCapitalComPySe/tests/TradingView/result.txt"
    file = open(file_name, "w")

    yield file

    file.close()
    print("*** The end file fixture => teardown ***\n")


@pytest.fixture(
    scope="function",
    params=random.sample([
        "Shares",
        "Forex",
        "Indices",
        "Commodities",
        "Cryptocurrencies"
    ], 2)
)
def cur_market_2_rnd_from_5(request):
    """Markets sorting parameters"""
    print(f"\n\n\nCurrent market - {request.param}")
    return request.param
