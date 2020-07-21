# -*- coding: UTF-8 -*-

import sys
import os

from multiprocessing import Process
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebElement
import redis
import time
import json
from tempfile import TemporaryDirectory

from pythinkutils.common.log import g_logger
from pythinkutils.common.datetime_utils import *
from pythinkutils.common.StringUtils import *

class BaseCPASeleniumProcess(Process, AbstractEventListener):
    def __init__(self):
        super(Process, self).__init__()
        super(AbstractEventListener, self).__init__()

        self.m_eventDriver = None

    def run(self):
        while True:
            time.sleep(3)
            try:
                self.on_start()
            except Exception as e:
                g_logger.error(e)
                pass

    def before_navigate_to(self, url, browser):
        pass

    def after_navigate_to(self, url, browser):
        pass

    def after_click(self, element, browser):
        pass

    def on_start(self):
        pass

    def on_get_ua(self):
        return ""

    def on_get_proxy(self):
        # return "SOCKS5://{}:{}".format(dictProxy["ip"], dictProxy["port"])
        return ""

    def on_get_data_dir(self):
        return TemporaryDirectory()

    def mk_chrome(self, bHeadless = True):
        option = webdriver.ChromeOptions()

        if bHeadless:
            option.add_argument('headless')

        option.add_argument('--no-sandbox')

        szUA = self.on_get_ua()
        if False == is_empty_string(szUA):
            option.add_argument("user-agent={0}".format(szUA))

        szProxy = self.on_get_proxy()
        if False == is_empty_string(szProxy):
            g_logger.info("--proxy-server={}".format(szProxy))
            option.add_argument("--proxy-server={}".format(szProxy))
        else:
            pass

        option.add_argument('--user-data-dir={}'.format(self.on_get_data_dir()))

        driver = webdriver.Chrome(options=option)
        driver.delete_all_cookies()
        driver.set_window_size(1080, 1920)
        driver.set_page_load_timeout(60)

        self.m_eventDriver = EventFiringWebDriver(driver, self)