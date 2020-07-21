# -*- coding: utf-8 -*-

import os

class FileUtils(object):
    @classmethod
    def create_folder_if_not_exists(cls, szPath):
        if False == os.path.exists(szPath):
            os.makedirs(szPath)