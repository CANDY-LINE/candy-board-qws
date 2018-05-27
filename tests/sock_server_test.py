#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2018 CANDY LINE INC.
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
    assert ret == '{"status": "OK", "result": {"apns": [{"apn": ' \
        '"access_point_name", "user": "user_id", "apn_id": "1"}]}}'


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


def test_network_show(setup_sock_server):
    ret = setup_sock_server.perform({'category': 'network', 'action': 'show'})
    assert ret == '{"status": "OK", ' \
        '"result": {' \
        '"operator": "NTT DOCOMO", ' \
        '"rssi": "-105", ' \
        '"network": "N/A", "rssiDesc": "", ' \
        '"registration": {"cs": "Registered", "ps": "Registered"}}}'


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
    assert ret == '{"status": "OK", ' \
        '"result": {' \
        '"operator": "N/A", ' \
        '"rssi": "-89", ' \
        '"network": "N/A", ' \
        '"rssiDesc": "", ' \
        '"registration": ' \
        '{"cs": "Searching", "ps": "Searching"}}}'


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
    assert ret == '{"status": "OK", ' \
        '"result": {' \
        '"operator": "N/A", ' \
        '"rssi": "-89", ' \
        '"network": "N/A", "rssiDesc": "", ' \
        '"registration": ' \
        '{"cs": "Denied", "ps": "Searching"}}}'


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
    ret = setup_sock_server.perform({'category': 'sim', 'action': 'show'})
    assert ret == '{"status": "OK", "result": ' \
        '{"msisdn": "09099999999", ' \
        '"state": "SIM_STATE_READY", "imsi": "440111111111111"}}'


def test_modem_show(setup_sock_server):
    ret = setup_sock_server.perform({'category': 'modem', 'action': 'show'})
    assert ret == '{"status": "OK", "result": ' \
        '{' \
        '"counter": {"rx": "39379", "tx": "7555"}, ' \
        '"datetime": "17/06/01,11:47:29", ' \
        '"functionality": "Full", ' \
        '"imei": "999999999999999", ' \
        '"timezone": 9.0, ' \
        '"model": "MOD", ' \
        '"manufacturer": "MAN", ' \
        '"revision": "REV"' \
        '}}'


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
    assert ret == '{"status": "OK", "result": ' \
        '{' \
        '"counter": {"rx": "39379", "tx": "7555"}, ' \
        '"datetime": "17/06/01,11:47:29", ' \
        '"functionality": "Anomaly", ' \
        '"imei": "999999999999999", ' \
        '"timezone": 9.0, ' \
        '"model": "MOD", ' \
        '"manufacturer": "MAN", ' \
        '"revision": "REV"' \
        '}}'


def test_modem_reset(setup_sock_server):
    ret = setup_sock_server.perform({'category': 'modem', 'action': 'reset'})
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
    ret = setup_sock_server.perform(
        {'category': 'modem',
         'action': 'init',
         'baudrate': '115200',
         'counter_reset': True
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
    assert ret == '{"status": "ERROR", "cmd": "AT+QNVW", "result": ""}'


def test_gnss_start(setup_sock_server):
    ret = setup_sock_server.perform(
        {'category': 'gnss', 'action': 'start'})
    assert ret == '{"status": "OK", "result": ""}'


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
                  '{"session": "started", "autogps": "disabled"}}'


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
                  '{"session": "stopped", "autogps": "enabled"}}'


def test_gnss_stop(setup_sock_server):
    ret = setup_sock_server.perform(
        {'category': 'gnss', 'action': 'stop'})
    assert ret == '{"status": "OK", "result": ""}'


def test_gnss_locate_ok(setup_sock_server):
    ret = setup_sock_server.perform(
        {'category': 'gnss', 'action': 'locate'})
    assert ret == '{"status": "OK", "result": ' \
                  '{' \
                  '"spkn": 0.0, "nsat": 9, "hdop": 0.7, "cog": 0.0, ' \
                  '"spkm": 0.0, "latitude": 35.68116, ' \
                  '"timestamp": "2018-05-21T07:12:17", ' \
                  '"altitude": 50.4, "fix": "2D", "longitude": 139.76486}' \
                  '}'


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
