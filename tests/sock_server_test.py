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

import path_hack
import candy_board_qws
from emulator_serialport import SerialPortEmurator
import pytest
import json


@pytest.fixture(scope='function')
def setup_sock_server(request):
    serialport = SerialPortEmurator()
    server = candy_board_qws.SockServer(
        'devel',
        '/var/run/candy-board-service.sock',
        serialport)
    server.debug = True
    server.seralport = serialport
    return server


def test_perform_nok(setup_sock_server):
    ret = setup_sock_server.perform(
        {'category': 'no-such-category', 'action': 'no-such-action'})
    assert ret == '{"status": "ERROR", "result": "Unknown Command"}'


def test_perform_nok(setup_sock_server):
    ret = setup_sock_server.perform({'category': '_apn', 'action': 'ls'})
    assert ret == '{"status": "ERROR", "result": "Unknown Command"}'


def test_perform_nok2(setup_sock_server):
    ret = setup_sock_server.perform({})
    assert ret == '{"status": "ERROR", "result": "Invalid Args"}'


def test_apn_ls(setup_sock_server):
    ret = setup_sock_server.perform({'category': 'apn', 'action': 'ls'})
    act = json.loads(ret)
    assert act['status'] == 'OK'
    assert act['result']['apns'][0]['apn'] == 'access_point_name'
    assert act['result']['apns'][0]['user'] == 'user_id'
    assert act['result']['apns'][0]['apn_id'] == '1'


def test_apn_set(setup_sock_server):
    ret = setup_sock_server.perform(
        {
            'category': 'apn', 'action': 'set', 'name': 'apn',
            'user_id': 'user', 'password': 'password'
        })
    assert ret == '{"status": "OK", "result": ""}'


def test_apn_del(setup_sock_server):
    ret = setup_sock_server.perform(
        {'category': 'apn', 'action': 'del', 'apn_id': '1'})
    assert ret == '{"status": "OK", "result": ""}'


def test_apn_set_nok(setup_sock_server):
    ret = setup_sock_server.perform({'category': 'apn', 'action': 'set'})
    assert ret == '{"status": "ERROR", "result": "Invalid Args"}'


def test_network_show_ec2x_lte(setup_sock_server):
    ret = setup_sock_server.perform({'category': 'network', 'action': 'show'})
    act = json.loads(ret)
    assert act['status'] == 'OK'
    assert act['result']['network'] == 'N/A'
    assert act['result']['access'] == 'FDD LTE'
    assert act['result']['band'] == 'LTE BAND 1'
    assert act['result']['registration']['cs'] == 'Registered'
    assert act['result']['registration']['ps'] == 'Registered'
    assert act['result']['registration']['eps'] == 'Registered'
    assert act['result']['operator'] == 'NTT DOCOMO'
    assert act['result']['rssi'] == '-105'
    assert act['result']['rssiDesc'] == ''


def test_network_show_uc20_gsm_1800(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['AT+QNWINFO'] = [
        "AT+QNWINFO",
        "",
        "",
        "ERROR",
        ""
    ]
    server.seralport.res['AT+QGBAND'] = [
        "AT+QGBAND",
        "",
        "",
        "+QGBAND: 2",
        "",
        "",
        "OK",
        ""
    ]
    ret = setup_sock_server.perform({'category': 'network', 'action': 'show'})
    act = json.loads(ret)
    assert act['status'] == 'OK'
    assert act['result']['network'] == 'N/A'
    assert act['result']['access'] == 'GSM'
    assert act['result']['band'] == 'GSM 1800'
    assert act['result']['registration']['cs'] == 'Registered'
    assert act['result']['registration']['ps'] == 'Registered'
    assert act['result']['registration']['eps'] == 'Registered'
    assert act['result']['operator'] == 'NTT DOCOMO'
    assert act['result']['rssi'] == '-105'
    assert act['result']['rssiDesc'] == ''


def test_network_show_no_signal(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['AT+COPS?'] = [
        "AT+COPS?",
        "",
        "",
        "+COPS: 0",
        "",
        "",
        "OK",
        ""
    ]
    server.seralport.res['AT+CSQ'] = [
        "AT+CSQ",
        "",
        "",
        "+CSQ: 12,99",
        "",
        "",
        "",
        "OK",
        ""
    ]
    server.seralport.res['AT+CREG?'] = [
        "AT+CREG?",
        "",
        "",
        "+CREG: 0,2",
        "",
        "",
        "",
        "OK",
        ""
    ]
    server.seralport.res['AT+CGREG?'] = [
        "AT+CGREG?",
        "",
        "",
        "+CGREG: 0,2",
        "",
        "",
        "",
        "OK",
        ""
    ]
    ret = setup_sock_server.perform({'category': 'network', 'action': 'show'})
    act = json.loads(ret)
    assert act['status'] == 'OK'
    assert act['result']['network'] == 'N/A'
    assert act['result']['access'] == 'FDD LTE'
    assert act['result']['band'] == 'LTE BAND 1'
    assert act['result']['registration']['cs'] == 'Searching'
    assert act['result']['registration']['ps'] == 'Searching'
    assert act['result']['registration']['eps'] == 'Registered'
    assert act['result']['operator'] == 'N/A'
    assert act['result']['rssi'] == '-89'
    assert act['result']['rssiDesc'] == ''


def test_network_show_denied_in_cs_networks(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['AT+COPS?'] = [
        "AT+COPS?",
        "",
        "",
        "+COPS: 0",
        "",
        "",
        "OK",
        ""
    ]
    server.seralport.res['AT+CSQ'] = [
        "AT+CSQ",
        "",
        "",
        "+CSQ: 12,99",
        "",
        "",
        "",
        "OK",
        ""
    ]
    server.seralport.res['AT+CREG?'] = [
        "AT+CREG?",
        "",
        "",
        "+CREG: 0,3",
        "",
        "",
        "",
        "OK",
        ""
    ]
    server.seralport.res['AT+CGREG?'] = [
        "AT+CGREG?",
        "",
        "",
        "+CGREG: 0,2",
        "",
        "",
        "",
        "OK",
        ""
    ]
    ret = setup_sock_server.perform({'category': 'network', 'action': 'show'})
    act = json.loads(ret)
    assert act['status'] == 'OK'
    assert act['result']['network'] == 'N/A'
    assert act['result']['access'] == 'FDD LTE'
    assert act['result']['band'] == 'LTE BAND 1'
    assert act['result']['registration']['cs'] == 'Denied'
    assert act['result']['registration']['ps'] == 'Searching'
    assert act['result']['registration']['eps'] == 'Registered'
    assert act['result']['operator'] == 'N/A'
    assert act['result']['rssi'] == '-89'
    assert act['result']['rssiDesc'] == ''


def test_network_deregister(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['AT+COPS='] = [
        "AT+COPS=",
        "",
        "",
        "OK",
        ""
    ]
    ret = setup_sock_server.perform(
        {'category': 'network', 'action': 'deregister'})
    assert ret == '{"status": "OK", "result": ""}'


def test_network_register(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['AT+COPS='] = [
        "AT+COPS=",
        "",
        "",
        "OK",
        ""
    ]
    ret = setup_sock_server.perform(
        {'category': 'network', 'action': 'register'})
    assert ret == '{"status": "OK", "result": {"mode": "0"}}'


def test_network_register_44099(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['AT+COPS='] = [
        "AT+COPS=",
        "",
        "",
        "OK",
        ""
    ]
    ret = setup_sock_server.perform(
        {'category': 'network', 'action': 'register', 'operator': '44099'})
    assert ret == '{"status": "OK", "result": {"mode": "1"}}'


def test_network_register_44099_auto(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['AT+COPS='] = [
        "AT+COPS=",
        "",
        "",
        "OK",
        ""
    ]
    ret = setup_sock_server.perform(
        {'category': 'network', 'action': 'register',
            'operator': '44099', 'auto': True})
    assert ret == '{"status": "OK", "result": {"mode": "4"}}'


def test_sim_show(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['AT+QCCID'] = [
        "AT+QCCID",
        "",
        "",
        "+QCCID: 00000000000000000000",
        "",
        "",
        "",
        "OK",
        ""
    ]
    ret = setup_sock_server.perform({'category': 'sim', 'action': 'show'})
    act = json.loads(ret)
    assert act['status'] == 'OK'
    assert act['result']['msisdn'] == '09099999999'
    assert act['result']['state'] == 'SIM_STATE_READY'
    assert act['result']['imsi'] == '440111111111111'
    assert act['result']['iccid'] == '00000000000000000000'


def test_modem_show(setup_sock_server):
    ret = setup_sock_server.perform({'category': 'modem', 'action': 'show'})
    act = json.loads(ret)
    assert act['status'] == 'OK'
    assert act['result']['counter']['rx'] == '39379'
    assert act['result']['counter']['tx'] == '7555'
    assert act['result']['datetime'] == '17/06/01,11:47:29'
    assert act['result']['functionality'] == 'Full'
    assert act['result']['imei'] == '999999999999999'
    assert act['result']['timezone'] == 9.0
    assert act['result']['model'] == 'MOD'
    assert act['result']['manufacturer'] == 'MAN'
    assert act['result']['revision'] == 'REV'


def test_modem_show_anomaly(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['AT+CFUN?'] = [
        "AT+CFUN?",
        "",
        "",
        "+CFUN: 7",
        "",
        "",
        "",
        "OK",
        ""
    ]
    ret = setup_sock_server.perform({'category': 'modem', 'action': 'show'})
    act = json.loads(ret)
    assert act['status'] == 'OK'
    assert act['result']['counter']['rx'] == '39379'
    assert act['result']['counter']['tx'] == '7555'
    assert act['result']['datetime'] == '17/06/01,11:47:29'
    assert act['result']['functionality'] == 'Anomaly'
    assert act['result']['imei'] == '999999999999999'
    assert act['result']['timezone'] == 9.0
    assert act['result']['model'] == 'MOD'
    assert act['result']['manufacturer'] == 'MAN'
    assert act['result']['revision'] == 'REV'


def test_modem_show_no_timezone(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['AT+CCLK?'] = [
        "AT+CCLK?",
        "",
        "",
        "+CCLK: \"80/01/06,00:02:45\"",
        "",
        "",
        "OK",
        ""
    ]
    ret = setup_sock_server.perform({'category': 'modem', 'action': 'show'})
    act = json.loads(ret)
    assert act['status'] == 'OK'
    assert act['result']['counter']['rx'] == '39379'
    assert act['result']['counter']['tx'] == '7555'
    assert act['result']['datetime'] == '80/01/06,00:02:45'
    assert act['result']['functionality'] == 'Full'
    assert act['result']['imei'] == '999999999999999'
    assert act['result']['timezone'] == 0.0
    assert act['result']['model'] == 'MOD'
    assert act['result']['manufacturer'] == 'MAN'
    assert act['result']['revision'] == 'REV'

def test_modem_reset(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['AT+CLCK='] = [
        "AT+CLCK=",
        "",
        "",
        "OK",
        ""
    ]
    ret = setup_sock_server.perform({'category': 'modem', 'action': 'reset'})
    assert ret == '{"status": "OK", "result": ""}'


def test_modem_reset_pu_ok(setup_sock_server):
    ret = setup_sock_server.perform({
        'category': 'modem', 'action': 'reset', 'pu': True})
    assert ret == '{"status": "OK", "result": ""}'


def test_modem_reset_pu_no_dialtone(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['AT+CLCK='] = [
        "AT+CLCK=",
        "",
        "",
        "NO DIALTONE",
        ""
    ]
    ret = setup_sock_server.perform({
        'category': 'modem', 'action': 'reset', 'pu': False})
    assert ret == '{"status": "OK", "result": ""}'


def test_modem_reset_pu_error(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['AT+CLCK='] = [
        "AT+CLCK=",
        "",
        "",
        "ERROR",
        ""
    ]
    ret = setup_sock_server.perform({
        'category': 'modem', 'action': 'reset', 'pu': False})
    assert ret == '{"status": "OK", "result": ""}'


def test_modem_reset_pu_error_0(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['AT+CLCK='] = [
        "AT+CLCK=",
        "",
        "",
        "+CME ERROR: 0",
        "",
        "",
        "",
        "OK",
        ""
    ]
    ret = setup_sock_server.perform({
        'category': 'modem', 'action': 'reset', 'pu': False})
    assert ret == '{"status": "OK", "result": ""}'


def test_modem_reset_pu_error_0_nok(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['AT+CLCK='] = [
        "AT+CLCK=",
        "",
        "",
        "+CME ERROR: 0",
        ""
    ]
    ret = setup_sock_server.perform({
        'category': 'modem', 'action': 'reset', 'pu': False})
    assert ret == '{"status": "OK", "result": ""}'


def test_modem_reset_with_counter_opts_CSV(setup_sock_server):
    ret = setup_sock_server.perform(
        {'category': 'modem', 'action': 'reset', 'opts': 'counter=yes '}
    )
    assert ret == '{"status": "OK", "result": "counter"}'


def test_modem_reset_with_counter_opts_JSON(setup_sock_server):
    ret = setup_sock_server.perform(
        {'category': 'modem', 'action': 'reset', 'opts': '{"counter":"yes"}'}
    )
    assert ret == '{"status": "OK", "result": "counter"}'


def test_modem_off(setup_sock_server):
    ret = setup_sock_server.perform({'category': 'modem', 'action': 'off'})
    assert ret == '{"status": "OK", "result": ""}'


def test_modem_init(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['AT+CLCK='] = [
        "AT+CLCK=",
        "",
        "",
        "OK",
        ""
    ]
    ret = setup_sock_server.perform(
        {'category': 'modem',
         'action': 'init',
         'baudrate': '115200',
         'counter_reset': True
         })
    assert ret == '{"status": "OK", ' \
                  '"result": {"counter_reset": "OK", "baudrate": "OK"}}'


def test_modem_init_pu_true(setup_sock_server):
    ret = setup_sock_server.perform(
        {'category': 'modem',
         'action': 'init',
         'baudrate': '115200',
         'counter_reset': True,
         'pu': True
         })
    assert ret == '{"status": "OK", ' \
                  '"result": {"counter_reset": "OK", "baudrate": "OK"}}'


def test_modem_init_qnvw_failure(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['AT+QNVW='] = [
        "AT+QNVW=",
        "",
        "",
        "ERROR",
        ""
    ]
    ret = setup_sock_server.perform(
        {'category': 'modem',
         'action': 'init',
         'baudrate': '115200',
         'counter_reset': True
         })
    act = json.loads(ret)
    assert act['status'] == 'ERROR'
    assert act['cmd'] == 'AT+QNVW'
    assert act['result'] == ''


def test_gnss_start_ec2x(setup_sock_server):
    ret = setup_sock_server.perform(
        {'category': 'gnss', 'action': 'start'})
    assert ret == '{"status": "OK", "result": ""}'


def test_gnss_start_ec2x_nok(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['AT+QGPSCFG="gnssconfig",0'] = [
        "AT+QGPSCFG=\"gnssconfig\",0",
        "",
        "",
        "+CME ERROR: 999",
        "",
        "",
        "ERROR",
        ""
    ]
    ret = setup_sock_server.perform(
        {'category': 'gnss', 'action': 'start'})
    act = json.loads(ret)
    assert act['status'] == 'ERROR'
    assert act['cmd'] == 'gnssconfig'
    assert act['result'] == 'ERROR'


def test_gnss_start_uc2x(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['ATI'] = [
        "ATI",
        "",
        "",
        "MAN",
        "",
        "UC20",
        "",
        "Revision: REV",
        "",
        "",
        "",
        "OK",
        ""
    ]
    ret = setup_sock_server.perform(
        {'category': 'gnss', 'action': 'start'})
    assert ret == '{"status": "OK", "result": ""}'


def test_gnss_start_uc2x_nok(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['ATI'] = [
        "ATI",
        "",
        "",
        "MAN",
        "",
        "UC20",
        "",
        "Revision: REV",
        "",
        "",
        "",
        "OK",
        ""
    ]
    server.seralport.res['AT+QGPSCFG="glonassenable",0'] = [
        "AT+QGPSCFG=\"glonassenable\",0",
        "",
        "",
        "+CME ERROR: 501",
        "",
        "",
        "ERROR",
        ""
    ]
    ret = setup_sock_server.perform(
        {'category': 'gnss', 'action': 'start'})
    act = json.loads(ret)
    assert act['status'] == 'ERROR'
    assert act['cmd'] == 'glonassenable'
    assert act['result'] == 'ERROR'


def test_gnss_status_on(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['AT+QGPSCFG='] = [
        'AT+QGPSCFG="autogps"',
        "",
        "",
        '+QGPSCFG: "autogps",0',
        "",
        "",
        "",
        "OK",
        ""
    ]
    ret = setup_sock_server.perform(
        {'category': 'gnss', 'action': 'status'})
    assert ret == '{"status": "OK", "result": ' + \
                  '{"session": "started", "qzss": "disabled"}}'


def test_gnss_status_on_uc20(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['ATI'] = [
        "ATI",
        "",
        "",
        "MAN",
        "",
        "UC20",
        "",
        "Revision: REV",
        "",
        "",
        "",
        "OK",
        ""
    ]
    ret = setup_sock_server.perform(
        {'category': 'gnss', 'action': 'status'})
    assert ret == '{"status": "OK", "result": ' + \
                  '{"session": "started", "qzss": "N/A"}}'


def test_gnss_status_off(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['AT+QGPSCFG='] = [
        'AT+QGPSCFG="autogps"',
        "",
        "",
        '+QGPSCFG: "autogps",1',
        "",
        "",
        "",
        "OK",
        ""
    ]
    server.seralport.res['AT+QGPS?'] = [
        "AT+QGPS?",
        "",
        "",
        "+QGPS: 0",
        "",
        "",
        "",
        "OK",
        ""
    ]
    ret = setup_sock_server.perform(
        {'category': 'gnss', 'action': 'status'})
    assert ret == '{"status": "OK", "result": ' + \
                  '{"session": "stopped", "qzss": "enabled"}}'


def test_gnss_stop(setup_sock_server):
    ret = setup_sock_server.perform(
        {'category': 'gnss', 'action': 'stop'})
    assert ret == '{"status": "OK", "result": ""}'


def test_gnss_locate_ok(setup_sock_server):
    ret = setup_sock_server.perform(
        {'category': 'gnss', 'action': 'locate'})
    act = json.loads(ret)
    assert act['status'] == 'OK'
    assert act['result']['spkn'] == 0.0
    assert act['result']['nsat'] == 9
    assert act['result']['hdop'] == 0.7
    assert act['result']['cog'] == 0.0
    assert act['result']['spkm'] == 0.0
    assert act['result']['latitude'] == 35.68116
    assert act['result']['altitude'] == 50.4
    assert act['result']['longitude'] == 139.76486
    assert act['result']['fix'] == '2D'
    assert act['result']['timestamp'] == '2018-05-21T07:12:17.000Z'


def test_gnss_locate_error_not_yet_fixed(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['AT+QGPSLOC='] = [
        "AT+QGPSLOC=",
        "",
        "",
        "+CME ERROR: 516",
        ""
    ]
    ret = setup_sock_server.perform(
        {'category': 'gnss', 'action': 'locate'})
    assert ret == '{"status": "ERROR", "result": "Not fixed yet"}'


def test_gnss_locate_error_other(setup_sock_server):
    server = setup_sock_server
    server.seralport.res['AT+QGPSLOC='] = [
        "AT+QGPSLOC=",
        "",
        "",
        "+CME ERROR: 500",
        ""
    ]
    ret = setup_sock_server.perform(
        {'category': 'gnss', 'action': 'locate'})
    assert ret == '{"status": "ERROR", "result": "500"}'


def test_service_version(setup_sock_server):
    ret = setup_sock_server.perform(
        {'category': 'service', 'action': 'version'})
    assert ret == '{"status": "OK", "result": {"version": "devel"}}'


def test_resolve_modem_port(setup_sock_server):
    candy_board_qws.SerialPort.resolve_modem_port()
