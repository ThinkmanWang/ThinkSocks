# -*- coding: UTF-8 -*-

import sys
import os

import time

from pythinkutils.selenium.BaseCPASeleniumProcess import BaseCPASeleniumProcess
from pythinkutils.common.log import g_logger

class BaiduProcess(BaseCPASeleniumProcess):
    def __init__(self):
        super(BaiduProcess, self).__init__()

    def before_navigate_to(self, url, browser):
        g_logger.info("Before navigate to %s" % (url, ))

    def after_navigate_to(self, url, browser):
        g_logger.info("After navigate to %s" % (url, ))

    def after_click(self, element, browser):
        pass

    def on_start(self):
        try:
            self.mk_chrome(bHeadless=False)

            if self.m_eventDriver is None:
                return

            self.m_eventDriver.get("http://baidu.com")

            time.sleep(30)
        except Exception as e:
            time.sleep(10)
        finally:
            self.m_eventDriver.quit()

    def on_get_ua(self):
        return ""

    def on_get_proxy(self):
        return ""


if __name__ == '__main__':
    p = BaiduProcess()
    p.start()

    p.join()