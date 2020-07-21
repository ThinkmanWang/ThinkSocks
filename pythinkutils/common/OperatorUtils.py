# -*- coding: UTF-8 -*-

import sys
import os

class OperatorUtils(object):
    g_lstVCT = ["1700", "1701", "1702"]
    g_lstVCM = ["1703", "1705", "1706"]
    g_lstVCU = ["1704", "1707", "1708", "1709", "171"]
    g_lstSatellite = ["1349"]
    g_lstCM = ["1340", "1341", "1342", "1343", "1344", "1345", "1346", "1347", "1348", "135", "136", "137", "138",
               "139", "147", "150", "151", "152", "157", "158", "159", "172", "178", "182", "183", "184", "187", "188",
               "198"]
    g_lstCU = ["130", "131", "132", "145", "155", "156", "166", "171", "175", "176", "185", "186", "166"]
    g_lstCT = ["133", "149", "153", "173", "177", "180", "181", "189", "199"]

    @classmethod
    def get_phone_operator(cls, szPhone):
        def phone_startswith(szPhone, lstStart):
            for szStart in lstStart:
                if str(szPhone).startswith(szStart):
                    return True

            return False

        if phone_startswith(szPhone, OperatorUtils.g_lstVCT):
            return "CT"
        elif phone_startswith(szPhone, OperatorUtils.g_lstVCM):
            return "CM"
        elif phone_startswith(szPhone, OperatorUtils.g_lstVCU):
            return "CU"
        elif phone_startswith(szPhone, OperatorUtils.g_lstSatellite):
            return "SATELLITE"
        elif phone_startswith(szPhone, OperatorUtils.g_lstCM):
            return "CM"
        elif phone_startswith(szPhone, OperatorUtils.g_lstCU):
            return "CU"
        elif phone_startswith(szPhone, OperatorUtils.g_lstCT):
            return "CT"
        else:
            return ""

# print(OperatorUtils.get_phone_operator("18621675203"))