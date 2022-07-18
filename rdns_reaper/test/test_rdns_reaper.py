import pytest
from rdns_reaper import rdns_reaper


def test_simpletest_1():
    dns = rdns_reaper()
    assert isinstance(dns, rdns_reaper)


def test_simple_iadd():
    dns = rdns_reaper()
    dns += "10.0.0.1"
    assert dns["10.0.0.1"] == None


def test__add__():
    dns1 = rdns_reaper()
    dns2 = rdns_reaper()
    dns1 += "10.0.0.1"
    dns2 += "10.0.0.2"
    dns3 = dns1 + dns2
    assert dns3.keys() == ["10.0.0.1", "10.0.0.2"]


def test__contains():
    dns1 = rdns_reaper()
    dns1 += "10.0.0.1"
    assert "10.0.0.1" in dns1


def test__del__():
    dns1 = rdns_reaper()
    dns1 += "10.0.0.1"
    del dns1["10.0.0.1"]
    assert "10.0.0.1" not in dns1


def test_add_ip():
    dns1 = rdns_reaper()
    dns1.add_ip("10.0.0.1")
    assert "10.0.0.1" in dns1


def test_add_ip_list():
    dns1 = rdns_reaper()
    dns1.add_ip_list(["10.0.0.1"])
    assert "10.0.0.1" in dns1


def test_limit_to_rfc1918_true():
    dns1 = rdns_reaper()
    dns1.limit_to_rfc1918(True)
    assert dns1._limit_to_rfc1918


def test_limit_to_rfc1918_false():
    dns1 = rdns_reaper()
    dns1.limit_to_rfc1918(False)
    assert dns1._limit_to_rfc1918 is False


def test_iterator():
    dns = rdns_reaper()
    dns.add_ip_list(["1.1.1.1", "8.8.8.8"])
    dns.resolve_all_serial()
    l1 = [("1.1.1.1", "one.one.one.one"), ("8.8.8.8", "dns.google")]

    for address in dns:
        if address not in l1:
            assert False

    assert True


def test_filter_1():
    dns = rdns_reaper()
    dns += ["10.0.0.1", "10.0.1.2"]

    dns.set_filter("10.0.0.0/24", mode="block")
    assert dns._build_resolve_list() == ["10.0.1.2"]
    dns.set_filter("10.0.0.0/24", mode="allow")
    assert dns._build_resolve_list() == ["10.0.0.1"]
