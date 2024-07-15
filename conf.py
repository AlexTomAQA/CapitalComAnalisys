""""
-*- coding: utf-8 -*-
@Time    : 2024/07/05 22:00
@Author  : Alexander Tomelo
"""
DEBUG = False
QTY_LINKS = 1

# HEADLESS = True  # режим браузера без отображения (безголовый)
HEADLESS = False  # режим с отображением браузера

# CHROME_WINDOW_SIZES = "--window-size=1280,720"
CHROME_WINDOW_SIZES = "--window-size=1920,1080"
# CHROME_WINDOW_SIZES_4k = "--window-size=3440,1440"
# HEADLESS = "--headless"  # not visible

# EDGE_WINDOW_SIZES = "--window-size=1280,720"
# EDGE_WINDOW_SIZES = "--window-size=1920,1080"
# EDGE_WINDOW_SIZES = (1280, 720)
EDGE_WINDOW_SIZES = (1920, 1080)

FIREFOX_WINDOW_WIDTH = "--width=1280"
FIREFOX_WINDOW_HEIGHT = "--height=720"
# FIREFOX_WINDOW_WIDTH = "--width=1920"
# FIREFOX_WINDOW_HEIGHT = "--height=1080"

SAFARI_WINDOW_SIZES = (1280, 720)
# SAFARI_WINDOW_SIZES = (1920, 1080)

BROWSER_HEADLESS = True  # not visible
# BROWSER_HEADLESS = False  # visible

# options parameters
CHROMIUM_HEADLESS = "--headless=new"  # not visible
WINDOW_SIZES = "--window-size=1920,1080"
CHROMIUM_WINDOW_WIDTH = "--width=1280"
CHROMIUM_WINDOW_HEIGHT = "--height=720"
