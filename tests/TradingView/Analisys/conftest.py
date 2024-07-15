"""
-*- coding: utf-8 -*-
@Time    : 2024/07/05 20:30
@Author  : AlexTomQA
"""

from datetime import datetime
# import random

import pytest

from pages.GoogleSheets.googlesheets import GoogleSheet


@pytest.fixture(
    scope="session",
    params=[
        "loc",  # locally runing
    ],
)
def cur_env(request):
    """Fixture"""
    # проверка аргументов командной строки
    if request.config.getoption("env"):
        if request.config.getoption("env") == "github":
            env = "github"
    else:
        env = request.param
    print(f"Current test environment - {env}")
    return env


@pytest.fixture(
    scope="function",
    params=[
        "GOLD",
        "GBPUSD",
        "EURUSD",
        "NZDUSD",
        "USDJPY",
        "AUDUSD",
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
        "SILVER",
        "COPPER",
        "CORN",
        "WHEAT",
    ],  # 23
)
def cur_trading_instrument(request):
    print(f"Current trading instrument - {request.param}\n")
    return request.param


@pytest.fixture(
    scope="session",
    # autouse=True
)
def gs(cur_env):
    print(f"\n{datetime.now()}   *** start fixture gs => setup ***\n")
    """Start execution program"""

    g_sheet = GoogleSheet(cur_env)

    # старт парсинга
    gs_out = ['Parsing now']
    g_sheet.update_range_values('A1', [gs_out])

    end_analisys_date_time = ['']
    g_sheet.update_range_values('C1', [end_analisys_date_time])

    # надо вставить строку
    g_sheet.add_new_row_before_(4)

    # надо вписать временной штамп
    start_analisys_date_time = [datetime.now().strftime("%d/%m/%Y %H:%M:%S")]
    g_sheet.update_range_values('A4', [start_analisys_date_time])

    yield g_sheet

    # окончание парсинг
    gs_out = ['Last parsing']
    g_sheet.update_range_values('A1', [gs_out])
    end_analisys_date_time = [datetime.now().strftime("%d/%m/%Y %H:%M:%S")]
    g_sheet.update_range_values('C1', [end_analisys_date_time])

    del g_sheet
    print(f"\n{datetime.now()}   *** end fixture gs => teardown ***\n")


@pytest.fixture(
    scope="module",
    params=[
        "File",
    ],
)
def file(request):
    """File Initialization"""
    file_name = "/home/atom/Projects/CapitalComAnalisys/tests/TradingView/result.txt"
    # file_name = "tests/TradingView/result.txt"
    file = open(file_name, "w")

    yield file

    file.close()
    print("*** The end file fixture => teardown ***\n")
