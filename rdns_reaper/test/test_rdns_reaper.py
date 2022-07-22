# import pytest
from rdns_reaper import rdns_reaper
from netaddr import IPAddress, IPNetwork, IPSet, AddrFormatError


def test_simpletest_1():
    dns = rdns_reaper()
    assert isinstance(dns, rdns_reaper)


def test_simple_iadd():
    dns = rdns_reaper()
    dns += "10.0.0.1"
    assert dns["10.0.0.1"] == None


def test__add__():
    dns1 = rdns_reaper()
    dns1.add("10.0.0.1")
    dns2 = dns1 + "10.0.0.2"
    assert dns2.keys() == ["10.0.0.1", "10.0.0.2"]
    dns3 = rdns_reaper()
    dns3.add("10.0.0.3")
    dns4 = dns2 + dns3
    dns5 = dns4 + {"10.0.0.4", "10.0.0.5"}
    for address in ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4", "10.0.0.5"]:
        assert address in dns5.keys()
    dns6 = dns5 + ["10.0.0.6", "10.0.0.7"]
    for address in [
        "10.0.0.1",
        "10.0.0.2",
        "10.0.0.3",
        "10.0.0.4",
        "10.0.0.5",
        "10.0.0.6",
        "10.0.0.7",
    ]:
        assert address in dns6.keys()

    try:
        dns1 + False
    except TypeError:
        assert True
    else:
        assert False


def test__iadd__():
    dns1 = rdns_reaper()
    dns2 = rdns_reaper()
    dns1 += "10.0.0.1"
    dns2 += ["10.0.0.2", "10.0.0.3"]
    dns2 += {"10.0.0.4", "10.0.0.5"}
    dns1 += dns2
    for address in ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4", "10.0.0.5"]:
        assert address in dns1.keys()

    try:
        dns1 += False
    except TypeError:
        assert True
    else:
        assert False


def test__contains__():
    dns1 = rdns_reaper()
    dns1 += "10.0.0.1"
    assert "10.0.0.1" in dns1


def test__del__():
    dns1 = rdns_reaper()
    dns1 += "10.0.0.1"
    del dns1["10.0.0.1"]
    assert "10.0.0.1" not in dns1


def test__set__item():
    dns1 = rdns_reaper()
    dns1.add("10.0.0.1")
    dns1["10.0.0.1"] = "private.address"
    assert dns1["10.0.0.1"] == "private.address"


def test_add_w_ip():
    dns1 = rdns_reaper()
    dns1.add("10.0.0.1")
    assert "10.0.0.1" in dns1


def test_add_w_list():
    dns1 = rdns_reaper()
    dns1.add(["10.0.0.1", "10.0.0.2"])
    assert "10.0.0.1" in dns1
    assert "10.0.0.2" in dns1


# def test_add_w_ipset():
#     dns1 = rdns_reaper()
#     ips = IPSet(["10.0.0.1", "10.0.0.2"])
#     dns1.add(ips)
#     assert "10.0.0.1" in dns1
#     assert "10.0.0.2" in dns1


def test_add_ip():
    dns1 = rdns_reaper()
    dns1.add_ip("10.0.0.1")
    dns1.add_ip("10.0.0.2", "private.address")
    assert "10.0.0.1" in dns1
    assert dns1.add_ip("10.0.0.1")
    assert dns1["10.0.0.2"] == "private.address"

    try:
        dns1.add_ip("taco")
    except TypeError:
        assert True
    else:
        assert False


def test_add_ip_list():
    dns1 = rdns_reaper()
    dns1.add_ip_list(["10.0.0.1", "10.0.0.2"])
    assert "10.0.0.1" in dns1
    assert "10.0.0.2" in dns1

    try:
        dns1.add_ip_list("taco")
    except TypeError:
        assert True
    else:
        assert False


def test_allow_reserved_networks_1():
    """Test to make sure reserved network switching works."""
    dns1 = rdns_reaper()
    assert dns1.get_options()["allow_reserved_networks"] is False
    dns1.allow_reserved_networks(True)
    assert dns1.get_options()["allow_reserved_networks"] is True
    dns1.allow_reserved_networks(False)
    assert dns1.get_options()["allow_reserved_networks"] is False

    dns2 = rdns_reaper(allow_reserved_networks=False)
    assert dns2.get_options()["allow_reserved_networks"] is False
    dns2 = rdns_reaper(allow_reserved_networks=True)
    assert dns2.get_options()["allow_reserved_networks"] is True

    try:
        dns2.allow_reserved_networks("taco")
    except TypeError:
        assert True
    else:
        assert False


def test_allow_reserved_networks_2():
    """Test to make sure the reserved network filter works."""
    dns1 = rdns_reaper()
    dns1.add("224.0.0.0")
    rl = dns1._build_resolve_list()
    assert "224.0.0.0" not in rl
    dns1.allow_reserved_networks(True)
    rl = dns1._build_resolve_list()
    assert "224.0.0.0" in rl


def test_clear_all_hostnames():
    test_hosts = ["1.1.1.1", "8.8.8.8"]
    dns1 = rdns_reaper()
    dns1.add(test_hosts)
    assert dns1.keys() == test_hosts
    assert dns1.values() == [None, None]
    dns1.set_name("1.1.1.1", "one.one.one.one")
    assert dns1["1.1.1.1"] == "one.one.one.one"
    dns1.clear_all_hostnames()
    assert dns1.keys() == test_hosts
    assert dns1.values() == [None, None]


def test_clearname():
    test_hosts = ["1.1.1.1", "8.8.8.8"]
    dns1 = rdns_reaper()
    dns1.add(test_hosts)
    assert dns1.keys() == test_hosts
    assert dns1.values() == [None, None]
    dns1.set_name("1.1.1.1", "one.one.one.one")
    dns1.set_name("8.8.8.8", "google.com")
    assert dns1["1.1.1.1"] == "one.one.one.one"
    assert dns1["8.8.8.8"] == "google.com"
    dns1.clearname("1.1.1.1")
    assert dns1["1.1.1.1"] == None
    assert dns1["8.8.8.8"] == "google.com"

    try:
        dns1.clearname("1.1.1.1.1")
    except TypeError:
        assert True
    else:
        assert False

    try:
        dns1.clearname(False)
    except KeyError:
        assert True
    else:
        assert False


def test_get_filter():
    filter_data = ["10.0.0.0/8", "172.16.0.0/12"]
    filter_mode = "allow"
    dns1 = rdns_reaper()
    dns1.set_filter(filter_data, mode=filter_mode)
    response = dns1.get_filter()
    assert response == (IPSet(filter_data), "allow")

    dns2 = rdns_reaper(filter=filter_data, filtermode=filter_mode)
    response2 = dns2.get_filter()
    assert response2 == (IPSet(filter_data), "allow")


def test__getitem__():
    dns1 = rdns_reaper()
    dns1.add_ip("10.0.0.1")
    response = dns1["10.0.0.1"]
    assert response == None

    try:
        dns1["chocotaco"]
    except AddrFormatError:
        assert True
    else:
        assert False

    assert dns1["10.0.0.2"] is False


def test_limit_to_rfc1918_true():
    dns1 = rdns_reaper()
    assert dns1._options_dict["limit_to_rfc1918"] is False
    dns1.limit_to_rfc1918(True)
    assert dns1._options_dict["limit_to_rfc1918"]

    dns2 = rdns_reaper(limit_to_rfc1918=True)
    assert dns2._options_dict["limit_to_rfc1918"]
    dns2 = rdns_reaper(limit_to_rfc1918=False)
    assert dns2._options_dict["limit_to_rfc1918"] is False

    try:
        dns1.limit_to_rfc1918("chocotaco")
    except TypeError:
        assert True
    else:
        assert False

    try:
        dns1 = rdns_reaper(limit_to_rfc1918="chocotaco")
    except TypeError:
        assert True
    else:
        assert False


def test_limit_to_rfc1918_false():
    dns1 = rdns_reaper()
    dns1.limit_to_rfc1918(False)
    assert dns1._options_dict["limit_to_rfc1918"] is False


def test_dict():
    dns1 = rdns_reaper()
    dns1.add_ip("1.1.1.1", "one.one.one.one")
    response = dns1.dict()
    assert response == {"1.1.1.1": "one.one.one.one"}


def test_get_dict():
    dns1 = rdns_reaper()
    dns1.add_ip("1.1.1.1", "one.one.one.one")
    response = dns1.get_dict()
    assert response == {"1.1.1.1": "one.one.one.one"}


def test_items():
    dns1 = rdns_reaper()
    dns1.add_ip("1.1.1.1", "one.one.one.one")
    assert dns1.items() == {"1.1.1.1": "one.one.one.one"}


def test_iterator():
    dns = rdns_reaper()
    dns.add_ip_list(["1.1.1.1", "8.8.8.8"])
    dns.resolve_all_serial()
    l1 = [("1.1.1.1", "one.one.one.one"), ("8.8.8.8", "dns.google")]

    for address in dns:
        if address not in l1:
            assert False

    assert True


def test_kwargs_concurrent():
    dns = rdns_reaper(concurrent=10)
    try:
        dns = rdns_reaper(concurrent="taco")
    except TypeError:
        assert True
    else:
        assert False


def test_kwargs_filename():
    dns = rdns_reaper(filename="test.yaml")
    try:
        dns = rdns_reaper(filename=False)
    except TypeError:
        assert True
    else:
        assert False


def test_kwargs_unresolvable():
    dns = rdns_reaper(unresolvable=r"N\A")
    try:
        dns = rdns_reaper(unresolvable=False)
    except TypeError:
        assert True
    else:
        assert False


def test_file_load_1():
    dns = rdns_reaper(filename="rdns_reaper/test/loadtest.yaml", filemode="r")
    assert dns["1.1.1.1"] == "one.one.one.one"


def test_file_load_2():
    with rdns_reaper(filename="rdns_reaper/test/loadtest.yaml", filemode="r") as dns:
        assert dns["1.1.1.1"] == "one.one.one.one"


def test_file_load3():
    try:
        dns = rdns_reaper(filename="rdns_reaper/test/loadtest.yaml", filemode="q")
    except ValueError:
        assert True
    else:
        assert False

    try:
        dns = rdns_reaper(filename="rdns_reaper/test/loadtest.yaml", filemode=False)
    except TypeError:
        assert True
    else:
        assert False
def test_file_save_1():
    dns1 = rdns_reaper(filename="rdns_reaper/test/savetest.yaml", filemode="w")
    dns1.add_ip("1.1.1.1", "one.one.one.one")
    dns1.savefile()

    dns2 = rdns_reaper(filename="rdns_reaper/test/savetest.yaml", filemode="r")
    assert dns2["1.1.1.1"] == "one.one.one.one"


def test_file_save_2():
    with rdns_reaper(filename="rdns_reaper/test/savetest.yaml", filemode="w") as dns1:
        dns1.add_ip("1.1.1.1", "one.one.one.one")

    with rdns_reaper(filename="rdns_reaper/test/savetest.yaml", filemode="r") as dns2:
        assert dns2["1.1.1.1"] == "one.one.one.one"


def test_filter_1():
    dns = rdns_reaper()
    dns += ["10.0.0.1", "10.0.1.2"]
    dns.set_filter("10.0.0.0/24")
    assert dns._build_resolve_list() == ["10.0.1.2"]
    dns.set_filter("10.0.0.0/24", mode="block")
    assert dns._build_resolve_list() == ["10.0.1.2"]
    dns.set_filter("10.0.0.0/24", mode="allow")
    assert dns._build_resolve_list() == ["10.0.0.1"]

    try:
        dns.set_filter("10.0.0.0/24", mode="taco")
    except ValueError:
        assert True
    else:
        assert False

    try:
        dns.set_filter(False)
    except TypeError:
        assert True
    else:
        assert False


def test_isrfc1918():
    assert rdns_reaper._isrfc1918("10.0.0.1")
    assert rdns_reaper._isrfc1918("1.0.0.1") is False


def test_isreservedaddress():
    assert rdns_reaper._isreservedaddress("224.0.0.1")
    assert rdns_reaper._isreservedaddress("10.0.0.1") is False
    assert rdns_reaper._isreservedaddress("fe80::1")
    assert rdns_reaper._isreservedaddress("2600::") is False


def test_isreservedIPv4():
    assert rdns_reaper._isreservedIPv4("224.0.0.1")
    assert rdns_reaper._isreservedIPv4("10.0.0.1") is False
    try:
        rdns_reaper._isreservedIPv4("taco")
    except ValueError:
        assert True
    except AddrFormatError:
        assert True
    else:
        assert False


def test_isreservedIPv6():
    assert rdns_reaper._isreservedIPv6("fe80::1")
    assert rdns_reaper._isreservedIPv6("2600::") is False
    try:
        rdns_reaper._isreservedIPv6("taco")
    except ValueError:
        assert True
    except AddrFormatError:
        assert True
    else:
        assert False


def test_remove_ip():
    dns = rdns_reaper()
    dns.add_ip("1.1.1.1")
    assert "1.1.1.1" in dns
    dns.remove_ip("1.1.1.1")
    assert "1.1.1.1" not in dns

    assert dns.remove_ip("2.2.2.2") is False

    try:
        dns.remove_ip("1.1.1.1.1")
    except TypeError:
        assert True
    else:
        assert False


def test_resolver_all_1():
    dns1 = rdns_reaper(allow_reserved_networks=True)
    dns1 += ["1.1.1.1", "8.8.8.8", "2600::", "10.255.254.253"]
    dns1.resolve_all()

    assert dns1["1.1.1.1"] == "one.one.one.one"
    assert dns1["2600::"] == "www.sprint.net"

    dns2 = rdns_reaper(limit_to_rfc1918=True)
    dns2.add(["1.1.1.1", "10.0.0.1"])
    assert "1.1.1.1" not in dns2._build_resolve_list()
    assert "10.0.0.1" in dns2._build_resolve_list()


def test_setname():
    dns1 = rdns_reaper()
    dns1 += ["1.1.1.1", "8.8.8.8"]
    dns1.set_name("1.1.1.1", "one.one.one.one")
    assert dns1["1.1.1.1"] == "one.one.one.one"
    try:
        dns1.set_name("taco", "taco")
    except TypeError:
        assert True
    else:
        assert False

    try:
        dns1.set_name("2.2.2.2", "two.two.two.two")
    except KeyError:
        assert True
    else:
        assert False
