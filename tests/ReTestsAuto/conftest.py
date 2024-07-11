"""
-*- coding: utf-8 -*-
@Time    : 2023/12/24 10:00
@Author  : Alexander Tomelo
"""
import os
from datetime import datetime, timedelta

import pytest

from pages.GoogleSheets.googlesheets import GoogleSheet
# from tests.ReTestsAuto.ReTestsAuto import unique_test, retest_skipped_tests, no_new_column

# ===========================================================
# выбор необходимых языков для ретеста
lang_list = [
        # "ar",
        # "cn",
        # "de",
        # "el",
        # "en",
        # "es",
        # "fr",
        # "hu",
        # "it",
        # "nl",
        "pl",
        "ro",
        "ru",
        "zh",
    ]

# ===========================================================
# выбор необходимых лицензий для ретеста
country_list = [
        "gb",  # United Kingdom - "FCA"
        "de",  # Germany - "CYSEC"
        "au",  # Australia - "ASIC"
        "ae",  # United Arab Emirates - "SCB"
]

# ===========================================================
# выбор необходимых ролей для ретеста
role_list = [
        "Auth",
        "NoAuth",
        "NoReg",
    ]

# ===========================================================
# ретест без добавления нового столбца
# ===========================================================
new_column = False  # без добавления нового столбца
# new_column = True  # с добавлением нового столбца

# ============================================================
# для проверки одного или нескольких тестов ввести номера строк
# так же необходимо поменять флаг unique_test = True
# ============================================================
# unique_test = True
unique_test = False
# ============================================================
list_rows = [114]

# ============================================================
# повторный проход только Skipped-tests
# retest_skipped_tests = True
retest_skipped_tests = False

# ============================================================
status_list = ['failed', 'passed']

# ============================================================
# получение корня проекта
host = "\\".join(os.getcwd().split('\\')[:-2]) + '\\'  # for macOS & Linux debugging
# host = "\\".join(os.getcwd().split('\\')) + '\\'  # for Windows debugging
# ============================================================

# ========= variables for this module ========
one_time_copy_paste = False
first_runer = False
last_runer = False


def time_concat(time1, time2):

    # Преобразование строк в объекты времени
    time1_obj = datetime.strptime(time1, "%H:%M:%S")
    time2_obj = datetime.strptime(time2, "%H:%M:%S")

    # Сложение временных объектов
    result_time_obj = time1_obj + timedelta(hours=time2_obj.hour, minutes=time2_obj.minute, seconds=time2_obj.second)

    # Преобразование результата обратно в строку
    result_time_str = result_time_obj.strftime("%H:%M:%S")
    return result_time_str


@pytest.fixture(
    scope="session"
    # , autouse=True
)
def gs():
    print(f"\n{datetime.now()}   *** start fixture gs = ... ***\n")
    """Start execution program"""

    global one_time_copy_paste
    global first_runer
    global last_runer

    g_sheet = GoogleSheet()
    g_sheet.wait_while_bugs_report_busy()
    gs_out = ["Busy"]
    g_sheet.update_range_values('B1', [gs_out])

    cell_o1 = g_sheet.get_cell_values("O1")
    print(f"cell_o1 имеет тип {type(cell_o1)}   и  значение {cell_o1}")
    var = cell_o1[0]
    print(f"var имеет тип {type(var)}   и  значение {var}")
    var2 = var[0]
    print(f"var2 имеет тип {type(var2)}   и  значение {var2}")
    qty_job = int(var2)  # Q-ty Job
    print(f"qty_job имеет тип {type(qty_job)}   и  значение {qty_job}")

    qty_job += 1
    if qty_job == 1:
        first_runer = True
    else:
        first_runer = False

    # first_runer = if qty_job == 1: False

    gs_out = [str(qty_job)]
    g_sheet.update_range_values('O1', [gs_out])

    # получение длины таблицы
    values = g_sheet.get_all_row_values()
    rows_qty = len(values)
    del values
    print(f"\n{datetime.now()}   QTY of rows = {rows_qty}")
    # execution_time_1 = g_sheet.get_row_values(4)[0][21]

    # старт ретеста
    start_retest_date = [datetime.now().strftime("%d/%m/%Y %H:%M:%S")]

    if unique_test or retest_skipped_tests or not new_column:
        # установка времени старта ретеста
        if first_runer:
            g_sheet.update_range_values('V1', [start_retest_date])
            # установка таймера выполнения ретестов
            # для запуска на Github
            g_sheet.update_range_values('V4', [["=NOW()-V1-TIME(3;0;0)"]])
            # для запуска на локальном компе
            # g_sheet.update_range_values('V4', [["=NOW()-V1-TIME(1;0;0)"]])

    else:
        # пройти надо 1 раз
        if not one_time_copy_paste:
            # # добавление нового столбца для результатов ретеста
            g_sheet.add_new_column_after_()
            #
            # # копирование данных столбца
            g_sheet.new_data_copy_past(
                0, rows_qty, 0, rows_qty,
                21, 22, 22, 23)
            #
            # # очистка полей
            g_sheet.clear_values(4, rows_qty, 21, 22)
            #
            # # замена значения Status на дату ретеста
            g_sheet.update_range_values('W3', [["=W2"]])
            g_sheet.date_format_cell()

            # установка времени старта ретеста
            g_sheet.update_range_values('V1', [start_retest_date])

            # установка таймера выполнения ретестов
            # # для запуска на Github
            g_sheet.update_range_values('V4', [["=NOW()-V1-TIME(3;0;0)"]])
            # для запуска на локальном компе
            # g_sheet.update_range_values('V4', [["=NOW()-V1"]])

            one_time_copy_paste = True

    # # установка счетчика выполненных в фильтре таблицы ретестов
    # g_sheet.new_data_copy_past(
    #     1, 2, 1, 2,
    #     5, 6, 21, 22)

    gs_out = ['Bugs Report']
    g_sheet.update_range_values('B1', [gs_out])

    yield g_sheet

    # окончание ретеста
    cell_o1 = g_sheet.get_cell_values("O1")
    print(f"cell_o1 имеет тип {type(cell_o1)}   и  значение {cell_o1}")
    var = cell_o1[0]
    print(f"var имеет тип {type(var)}   и  значение {var}")
    var2 = var[0]
    print(f"var2 имеет тип {type(var2)}   и  значение {var2}")
    qty_job = int(var2)  # Q-ty Job
    print(f"qty_job имеет тип {type(qty_job)}   и  значение {qty_job}")

    qty_job -= 1
    if qty_job == 0:
        last_runer = True
    else:
        last_runer = False

    gs_out = [str(qty_job)]
    g_sheet.update_range_values('O1', [gs_out])

    if last_runer:
        end_retest_date = [datetime.now().strftime("%d/%m/%Y %H:%M:%S")]
        g_sheet.update_range_values('V2', [end_retest_date])
        g_sheet.update_range_values('V4', [["=V2 - V1"]])

    gs_out = ['Bugs Report']
    g_sheet.update_range_values('B1', [gs_out])

    # if unique_test or retest_skipped_tests or not new_column:
    # execution_time_2 = g_sheet.get_row_values(4)[0][21]
    # # установка полного времени тестирования
    # execution_time = time_concat(execution_time_1, execution_time_2)
    # g_sheet.update_range_values('V4', [[execution_time]])

    # del g_sheet
    print(f"\n{datetime.now()}   *** end fixture gs = teardown ***\n")
