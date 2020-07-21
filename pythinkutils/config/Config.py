# -*- coding: UTF-8 -*-

import sys
import os

import configparser
import argparse
# from thinkutils.common_utils.singleton import Singleton

class ThinkConfig:

    m_myConfig = None

    def __init__(self):
        self.config = configparser.ConfigParser()

    def read(self, szPath):
        self.config.read(szPath)

    def get(self, szSection, szOption, szDefault = None):
        try:
            return self.config.get(szSection, szOption)
        except Exception as e:
            return szDefault

    def get_boolean(self, szSection, szOption, default = False):
        try:
            return self.config.getboolean(szSection, szOption)
        except Exception as e:
            return default

    def get_int(self, szSection, szOption, default = -1):
        try:
            return self.config.getint(szSection, szOption)
        except Exception as e:
            return default

    def get_float(self, szSection, szOption, default = 0.0):
        try:
            return self.config.getfloat(szSection, szOption)
        except Exception as e:
            return default

    @classmethod
    def get_default_config(cls):
        if cls.m_myConfig is None:
            config = ThinkConfig()
            config.read(os.path.dirname(os.path.abspath(__file__)) + "/app.properties")

            cls.m_myConfig = config

        return cls.m_myConfig

g_config = ThinkConfig.get_default_config()

# if __name__ == '__main__':
#     config = ThinkConfig.get_default_config()
#
#     print(config.get("mysql", "host"))
#
#     config1 = ThinkConfig.get_default_config()
#
#     print(config == config1)

