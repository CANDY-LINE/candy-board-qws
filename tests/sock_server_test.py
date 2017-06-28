import path_hack
import candy_board_qws
from emulator_serialport import SerialPortEmurator
import pytest


@pytest.fixture(scope='function')
def setup_sock_server(request):
    serialport = SerialPortEmurator()
    server = candy_board_qws.SockServer(
        'devel',
        {'apn': 'apn', 'user': 'apn_user', 'password': 'apn_password'},
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
    assert ret == '{"status": "OK", "result": {"rssi": "-105",' \
        ' "network": "ONLINE", "rssiDesc": ""}}'


def test_sim_show(setup_sock_server):
    ret = setup_sock_server.perform({'category': 'sim', 'action': 'show'})
    assert ret == '{"status": "OK", "result": ' \
        '{"msisdn": "09099999999", ' \
        '"state": "SIM_STATE_READY", "imsi": "440111111111111"}}'


def test_modem_show(setup_sock_server):
    ret = setup_sock_server.perform({'category': 'modem', 'action': 'show'})
    assert ret == '{"status": "OK", "result": ' \
        '{"imei": "999999999999999", ' \
        '"counter": {"rx": "39379", "tx": "7555"}, "model": "MOD", ' \
        '"revision": "REV", "manufacturer": "MAN"}}'


def test_modem_reset(setup_sock_server):
    ret = setup_sock_server.perform({'category': 'modem', 'action': 'reset'})
    assert ret == '{"status": "OK", "result": ""}'


def test_modem_off(setup_sock_server):
    ret = setup_sock_server.perform({'category': 'modem', 'action': 'off'})
    assert ret == '{"status": "OK", "result": ""}'


def test_service_version(setup_sock_server):
    ret = setup_sock_server.perform(
        {'category': 'service', 'action': 'version'})
    assert ret == '{"status": "OK", "result": {"version": "devel"}}'


def test_resolve_modem_port(setup_sock_server):
    candy_board_qws.SerialPort.resolve_modem_port()
