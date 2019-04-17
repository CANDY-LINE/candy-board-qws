#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019 CANDY LINE INC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class SerialPortEmurator:
    def __init__(self):
        self.org_res = {
            'AT+COPS?': [
                "AT+COPS?",
                "",
                "",
                "+COPS: 0,0,\"NTT DOCOMO\",4",
                "",
                "",
                "OK",
                ""
            ],
            'AT+CCLK?': [
                "AT+CCLK?",
                "",
                "",
                "+CCLK: \"17/06/01,11:47:29+36\"",
                "",
                "",
                "OK",
                ""
            ],
            'AT+IPR=': [
                "AT+IPR=",
                "",
                "",
                "OK",
                ""
            ],
            'AT+COPS=': [
                "AT+COPS=",
                "",
                "",
                "OK",
                ""
            ],
            'AT+CTZU=': [
                "AT+CTZU=",
                "",
                "",
                "OK",
                ""
            ],
            'AT+CTZU?': [
                "AT+CTZU?",
                "",
                "",
                "+CTZU: 0",
                "",
                "",
                "OK",
                ""
            ],
            'AT+QPOWD': [
                "AT+QPOWD",
                "",
                "",
                "OK",
                ""
                "",
                "",
                "",
                "",
                "POWERED DOWN",
                "",
                "",
            ],
            'AT+GSN': [
                "AT+GSN",
                "",
                "",
                "999999999999999",
                "",
                "",
                "OK",
                ""
            ],
            'AT+QGDCNT=': [
                "AT+QGDCNT=",
                "",
                "",
                "OK",
                ""
            ],
            'AT+QGDCNT?': [
                "AT+QGDCNT?",
                "",
                "",
                "+QGDCNT: 7555,39379",
                "",
                "",
                "OK",
                ""
            ],
            'AT+CGDCONT?': [
                "AT+CGDCONT?",
                "",
                "",
                "+CGDCONT: 1,\"IPV4V6\",\"access_point_name\",\"0.0.0.0\",0,0",
                "",
                "",
                "",
                "OK",
                ""
            ],
            'AT$QCPDPP?': [
                "AT$QCPDPP?",
                "",
                "",
                "$QCPDPP: 1,3,\"user_id\"",
                "",
                "$QCPDPP: 2,0",
                "",
                "$QCPDPP: 3,0",
                "",
                "$QCPDPP: 4,0",
                "",
                "$QCPDPP: 5,0",
                "",
                "$QCPDPP: 6,0",
                "",
                "$QCPDPP: 7,0",
                "",
                "$QCPDPP: 8,0",
                "",
                "$QCPDPP: 9,0",
                "",
                "$QCPDPP: 10,0",
                "",
                "$QCPDPP: 11,0",
                "",
                "$QCPDPP: 12,0",
                "",
                "$QCPDPP: 13,0",
                "",
                "$QCPDPP: 14,0",
                "",
                "$QCPDPP: 15,0",
                "",
                "$QCPDPP: 16,0",
                "",
                "",
                "",
                "OK",
                ""
            ],
            'AT+CGDCONT=': [
                "AT+CGDCONT=",
                "",
                "",
                "OK",
                ""
            ],
            'AT$QCPDPP=': [
                "AT$QCPDPP=",
                "",
                "",
                "OK",
                ""
            ],
            'AT+CSQ': [
                "AT+CSQ",
                "",
                "",
                "+CSQ: 4,99",  # "+CSQ: 99,99"
                "",
                "",
                "",
                "OK",
                ""
            ],
            'AT+CREG?': [
                "AT+CREG?",
                "",
                "",
                "+CREG: 0,1",
                "",
                "",
                "",
                "OK",
                ""
            ],
            'AT+CGREG?': [
                "AT+CGREG?",
                "",
                "",
                "+CGREG: 0,1",
                "",
                "",
                "",
                "OK",
                ""
            ],
            'AT+CEREG?': [
                "AT+CEREG?",
                "",
                "",
                "+CEREG: 0,1",
                "",
                "",
                "",
                "OK",
                ""
            ],
            'AT+CNUM': [
                "AT+CNUM",
                "",
                "",
                "+CNUM: ,\"09099999999\",129",  # "+CNUM: ,\"\",129"
                "",
                "",
                "",
                "",
                "",
                "OK",
                ""
            ],
            'AT+CIMI': [
                "AT+CIMI",
                "",
                "",
                "440111111111111",  # "+CME ERROR: operation not allowed"
                "",
                "OK",
                ""
            ],
            'AT+CPAS': [
                "AT+CPAS",
                "",
                "",
                "+CPAS: 4",  # "+CPAS: 0"
                "",
                "",
                "",
                "OK",
                ""
            ],
            'AT+QNVW=': [
                "AT+QNVW=",
                "",
                "",
                "OK",
                ""
            ],
            'AT+CFUN?': [
                "AT+CFUN?",
                "",
                "",
                "+CFUN: 1",
                "",
                "",
                "",
                "OK",
                ""
            ],
            'ATI': [
                "ATI",
                "",
                "",
                "MAN",
                "",
                "MOD",
                "",
                "Revision: REV",
                "",
                "",
                "",
                "OK",
                ""
            ],
            'AT+QGPSCFG=': [
                "AT+QGPSCFG=",
                "",
                "",
                "OK",
                ""
            ],
            'AT+QGPS=': [
                "AT+QGPS=",
                "",
                "",
                "OK",
                ""
            ],
            'AT+QGPS?': [
                "AT+QGPS?",
                "",
                "",
                "+QGPS: 1",
                "",
                "",
                "",
                "OK",
                ""
            ],
            'AT+QGPSLOC=': [
                "AT+QGPSLOC=",
                "",
                "",
                "+QGPSLOC: 071217.0,35.68116,139.76486,"
                "0.7,50.4,2,0.00,0.0,0.0,210518,09",
                "",
                "",
                "",
                "OK",
                ""
            ],
            'AT+QGPSEND': [
                "AT+QGPSEND",
                "",
                "",
                "OK",
                ""
            ],
            'AT+QNWINFO': [
                "AT+QNWINFO",
                "",
                "",
                "+QNWINFO: \"FDD LTE\",\"44010\",\"LTE BAND 1\",1849",
                "",
                "",
                "",
                "OK",
                ""
            ],
        }
        self.reset_res()

    def reset_res(self):
        self.res = dict(self.org_res)

    def available(self):
        return True

    def read_line(self):
        if self.line < 0:
            return None
        try:
            text = self.res[self.cmd][self.line]
            self.line += 1
            return text
        except Exception:
            self.line = -1
            return None

    def write(self, str):
        print("W:[%s]" % str)
        self.cmd = str.strip()
        if self.cmd.find('=') >= 0:
            self.cmd = self.cmd[:self.cmd.find('=') + 1]
        self.line = 0
        self.res[self.cmd][0] = str.strip()
