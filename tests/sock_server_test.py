# Copyright (c) 2017 CANDY LINE INC.
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
        '"rssi": "-105",' \
        ' "network": "ONLINE", "rssiDesc": ""}}'


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
    assert ret == '{"status": "OK", "result": ""}'


def test_service_version(setup_sock_server):
    ret = setup_sock_server.perform(
        {'category': 'service', 'action': 'version'})
    assert ret == '{"status": "OK", "result": {"version": "devel"}}'


def test_resolve_modem_port(setup_sock_server):
    candy_board_qws.SerialPort.resolve_modem_port()
