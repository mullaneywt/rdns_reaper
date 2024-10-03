# pylint: disable=W,C,R

import os

from netaddr import AddrFormatError, IPAddress, IPNetwork, IPSet

from rdns_reaper import RdnsReaper


def test_simpletest_1():
    dns = RdnsReaper()
    assert isinstance(dns, RdnsReaper)


def test_simple_iadd():
    dns = RdnsReaper()
    dns += "10.0.0.1"
    assert dns["10.0.0.1"] is None


def test__add__():
    dns1 = RdnsReaper()
    """Add a single IP as a string with the add function"""
    dns1.add("10.0.0.1")
    """Add a single IP as a string with the operand"""
    dns2 = dns1 + "10.0.0.2"
    assert dns2.keys() == ["10.0.0.1", "10.0.0.2"]
    dns3 = RdnsReaper()
    dns3.add("10.0.0.3")
    """Add two classes together"""
    dns4 = dns2 + dns3
    """Add a set to the class"""
    dns5 = dns4 + {"10.0.0.4", "10.0.0.5"}
    for address in ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4", "10.0.0.5"]:
        assert address in dns5.keys()
    """Add a list to the class"""
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


def test__iadd1__():
    dns1 = RdnsReaper()
    """Add a single IP as a string with the add function"""
    dns1.add("10.0.0.1")
    """Add a single IP as a string with the operand"""
    dns1 += "10.0.0.2"
    assert dns1.keys() == ["10.0.0.1", "10.0.0.2"]
    dns2 = RdnsReaper()
    dns2.add("10.0.0.3")
    """Add two classes together"""
    dns1 += dns2
    """Add a set to the class"""
    dns1 += {"10.0.0.4", "10.0.0.5"}
    for address in ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4", "10.0.0.5"]:
        assert address in dns1.keys()
    """Add a list to the class"""
    dns1 += ["10.0.0.6", "10.0.0.7"]
    for address in [
        "10.0.0.1",
        "10.0.0.2",
        "10.0.0.3",
        "10.0.0.4",
        "10.0.0.5",
        "10.0.0.6",
        "10.0.0.7",
    ]:
        assert address in dns1.keys()

    try:
        dns1 += False
    except TypeError:
        assert True
    else:
        assert False


def test__iadd2__():
    dns1 = RdnsReaper()
    dns2 = RdnsReaper()
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
    dns1 = RdnsReaper()
    dns1 += "10.0.0.1"
    assert "10.0.0.1" in dns1


def test__del__():
    dns1 = RdnsReaper()
    dns1 += "10.0.0.1"
    del dns1["10.0.0.1"]
    assert "10.0.0.1" not in dns1


def test__set__item():
    dns1 = RdnsReaper()
    dns1.add("10.0.0.1")
    dns1["10.0.0.1"] = "private.address"
    assert dns1["10.0.0.1"] == "private.address"


def test_add_w_ip():
    dns1 = RdnsReaper()
    dns1.add("10.0.0.1")
    assert "10.0.0.1" in dns1


def test_add_w_list():
    dns1 = RdnsReaper()
    dns1.add(["10.0.0.1", "10.0.0.2"])
    assert "10.0.0.1" in dns1
    assert "10.0.0.2" in dns1


# def test_add_w_ipset():
#     dns1 = RdnsReaper()
#     ips = IPSet(["10.0.0.1", "10.0.0.2"])
#     dns1.add(ips)
#     assert "10.0.0.1" in dns1
#     assert "10.0.0.2" in dns1


def test_add_ip():
    dns1 = RdnsReaper()
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
    dns1 = RdnsReaper()
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
    dns1 = RdnsReaper()
    assert dns1.get_options()["allow_reserved_networks"] is False
    dns1.allow_reserved_networks(True)
    assert dns1.get_options()["allow_reserved_networks"] is True
    dns1.allow_reserved_networks(False)
    assert dns1.get_options()["allow_reserved_networks"] is False

    dns2 = RdnsReaper(allow_reserved_networks=False)
    assert dns2.get_options()["allow_reserved_networks"] is False
    dns2 = RdnsReaper(allow_reserved_networks=True)
    assert dns2.get_options()["allow_reserved_networks"] is True

    try:
        dns2.allow_reserved_networks("taco")
    except TypeError:
        assert True
    else:
        assert False


def test_allow_reserved_networks_2():
    """Test to make sure the reserved network filter works."""
    dns1 = RdnsReaper()
    dns1.add("224.0.0.0")
    rl = dns1._build_resolve_list()
    assert "224.0.0.0" not in rl
    dns1.allow_reserved_networks(True)
    rl = dns1._build_resolve_list()
    assert "224.0.0.0" in rl


def test_auto_save_1():
    """Test to make sure autosave enables correctly"""
    dns1 = RdnsReaper(autosave=True, filename="savetest.yaml", filemode="w")
    assert dns1._options_dict["autosave"] == True


def test_auto_save_2():
    """Test to make sure autosave throws an error if filename/mode aren't present or are incorrect"""
    try:
        dns1 = RdnsReaper(autosave=True, filename="savetest.yaml", filemode="r")
    except ValueError:
        assert True
    else:
        assert False

    try:
        dns1 = RdnsReaper(autosave=True, filename="savetest.yaml")
    except ValueError:
        assert True
    else:
        assert False

    try:
        dns1 = RdnsReaper(autosave=True, filemode="w")
    except ValueError:
        assert True
    else:
        assert False

    try:
        dns1 = RdnsReaper(autosave=True)
    except ValueError:
        assert True
    else:
        assert False


def test_auto_save_3():
    try:
        os.remove("rdns_reaper/test/savetest.yaml")
    except FileNotFoundError:
        pass

    dns1 = RdnsReaper(autosave=True, filename="savetest.yaml", filemode="w")
    dns1.add(["1.1.1.1"])
    dns1.resolve_all()

    dns2 = RdnsReaper(filename="savetest.yaml", filemode="r")

    assert dns2["1.1.1.1"] == "one.one.one.one"


def test_auto_save_4():
    try:
        os.remove("rdns_reaper/test/savetest.yaml")
    except FileNotFoundError:
        pass

    dns1 = RdnsReaper(filename="savetest.yaml", filemode="w")
    assert dns1._options_dict["autosave"] == False
    dns1.autosave(True)
    assert dns1._options_dict["autosave"] == True
    dns1.autosave(False)

    try:
        dns1.autosave("DNS")
    except TypeError:
        assert True
    else:
        assert False

    dns2 = RdnsReaper()
    try:
        dns2.autosave(True)
    except ValueError:
        assert True
    else:
        assert False


def test_clear_all_hostnames():
    test_hosts = ["1.1.1.1", "8.8.8.8"]
    dns1 = RdnsReaper()
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
    dns1 = RdnsReaper()
    dns1.add(test_hosts)
    assert dns1.keys() == test_hosts
    assert dns1.values() == [None, None]
    dns1.set_name("1.1.1.1", "one.one.one.one")
    dns1.set_name("8.8.8.8", "google.com")
    assert dns1["1.1.1.1"] == "one.one.one.one"
    assert dns1["8.8.8.8"] == "google.com"
    dns1.clearname("1.1.1.1")
    assert dns1["1.1.1.1"] is None
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
    dns1 = RdnsReaper()
    dns1.set_filter(filter_data, mode=filter_mode)
    response = dns1.get_filter()
    assert response == (IPSet(filter_data), "allow")

    dns2 = RdnsReaper(filter=filter_data, filtermode=filter_mode)
    response2 = dns2.get_filter()
    assert response2 == (IPSet(filter_data), "allow")


def test__getitem__():
    dns1 = RdnsReaper()
    dns1.add_ip("10.0.0.1")
    response = dns1["10.0.0.1"]
    assert response is None

    try:
        dns1["chocotaco"]
    except AddrFormatError:
        assert True
    else:
        assert False

    assert dns1["10.0.0.2"] is False


def test_limit_to_rfc1918_true():
    dns1 = RdnsReaper()
    assert dns1._options_dict["limit_to_rfc1918"] is False
    dns1.limit_to_rfc1918(True)
    assert dns1._options_dict["limit_to_rfc1918"]

    dns2 = RdnsReaper(limit_to_rfc1918=True)
    assert dns2._options_dict["limit_to_rfc1918"]
    dns2 = RdnsReaper(limit_to_rfc1918=False)
    assert dns2._options_dict["limit_to_rfc1918"] is False

    try:
        dns1.limit_to_rfc1918("chocotaco")
    except TypeError:
        assert True
    else:
        assert False

    try:
        dns1 = RdnsReaper(limit_to_rfc1918="chocotaco")
    except TypeError:
        assert True
    else:
        assert False


def test_limit_to_rfc1918_false():
    dns1 = RdnsReaper()
    dns1.limit_to_rfc1918(False)
    assert dns1._options_dict["limit_to_rfc1918"] is False


def test_dict():
    dns1 = RdnsReaper()
    dns1.add_ip("1.1.1.1", "one.one.one.one")
    response = dns1.dict()
    assert response == {"1.1.1.1": "one.one.one.one"}


def test_get_dict():
    dns1 = RdnsReaper()
    dns1.add_ip("1.1.1.1", "one.one.one.one")
    response = dns1.get_dict()
    assert response == {"1.1.1.1": "one.one.one.one"}


def test_items():
    dns1 = RdnsReaper()
    dns1.add_ip("1.1.1.1", "one.one.one.one")
    dns1.add_ip("8.8.8.8", "dns.google")
    assert isinstance(dns1.items(), type({}.items()))
    l1 = list(dns1.items())
    assert l1 == [("1.1.1.1", "one.one.one.one"), ("8.8.8.8", "dns.google")]


def test_iterator():
    dns = RdnsReaper()
    dns.add_ip_list(["1.1.1.1", "8.8.8.8"])
    dns.resolve_all_serial()
    l1 = [("1.1.1.1", "one.one.one.one"), ("8.8.8.8", "dns.google")]

    for address in dns:
        if address not in l1:
            assert False

    assert True


def test_kwargs_concurrent():
    dns = RdnsReaper(concurrent=10)
    try:
        dns = RdnsReaper(concurrent="taco")
    except TypeError:
        assert True
    else:
        assert False


def test_kwargs_filename():
    dns = RdnsReaper(filename="test.yaml")
    try:
        dns = RdnsReaper(filename=False)
    except TypeError:
        assert True
    else:
        assert False


def test_kwargs_unresolvable():
    dns = RdnsReaper(unresolvable=r"N\A")
    try:
        dns = RdnsReaper(unresolvable=False)
    except TypeError:
        assert True
    else:
        assert False


def test_file_load_1():
    dns = RdnsReaper(filename="rdns_reaper/test/loadtest.yaml", filemode="r")
    assert dns["1.1.1.1"] == "one.one.one.one"


def test_file_load_2():
    with RdnsReaper(filename="rdns_reaper/test/loadtest.yaml", filemode="r") as dns:
        assert dns["1.1.1.1"] == "one.one.one.one"


def test_file_load_3():
    try:
        dns = RdnsReaper(filename="rdns_reaper/test/loadtest.yaml", filemode="q")
    except ValueError:
        assert True
    else:
        assert False

    try:
        dns = RdnsReaper(filename="rdns_reaper/test/loadtest.yaml", filemode=False)
    except TypeError:
        assert True
    else:
        assert False


def test_file_load_4():
    try:
        dns = RdnsReaper(filename="rdns_reaper/test/taco.yaml", filemode="r")
    except:
        assert False
    else:
        assert True


def test_file_save_1():
    try:
        os.remove("rdns_reaper/test/savetest.yaml")
    except FileNotFoundError:
        pass
    dns1 = RdnsReaper(filename="rdns_reaper/test/savetest.yaml", filemode="w")
    dns1.add_ip("1.1.1.1", "one.one.one.one")
    dns1.savefile()

    dns2 = RdnsReaper(filename="rdns_reaper/test/savetest.yaml", filemode="r")
    assert dns2["1.1.1.1"] == "one.one.one.one"


def test_file_save_2():
    try:
        os.remove("rdns_reaper/test/savetest.yaml")
    except FileNotFoundError:
        pass

    with RdnsReaper(filename="rdns_reaper/test/savetest.yaml", filemode="w") as dns1:
        dns1.add_ip("1.1.1.1", "one.one.one.one")

    with RdnsReaper(filename="rdns_reaper/test/savetest.yaml", filemode="r") as dns2:
        assert dns2["1.1.1.1"] == "one.one.one.one"


def test_file_save_3():
    try:
        os.remove("rdns_reaper/test/savetest.yaml")
    except FileNotFoundError:
        pass

    with RdnsReaper(autosave=True, filename="rdns_reaper/test/savetest.yaml", filemode="w") as dns1:
        dns1.add_ip("1.1.1.1", "one.one.one.one")
        dns1.resolve_all()

    with RdnsReaper(filename="rdns_reaper/test/savetest.yaml", filemode="r") as dns2:
        assert dns2["1.1.1.1"] == "one.one.one.one"


def test_filter_1():
    dns = RdnsReaper()
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
    assert RdnsReaper._isrfc1918("10.0.0.1")
    assert RdnsReaper._isrfc1918("1.0.0.1") is False


def test_isreservedaddress():
    assert RdnsReaper._isreservedaddress("224.0.0.1")
    assert RdnsReaper._isreservedaddress("10.0.0.1") is False
    assert RdnsReaper._isreservedaddress("fe80::1")
    assert RdnsReaper._isreservedaddress("2600::") is False


def test_isreservedipv4():
    assert RdnsReaper._isreservedipv4("224.0.0.1")
    assert RdnsReaper._isreservedipv4("10.0.0.1") is False
    try:
        RdnsReaper._isreservedipv4("taco")
    except ValueError:
        assert True
    except AddrFormatError:
        assert True
    else:
        assert False

    try:
        RdnsReaper._isreservedipv4("::")
    except ValueError:
        assert True
    else:
        assert False


def test_isreservedipv6():
    assert RdnsReaper._isreservedipv6("fe80::1")
    assert RdnsReaper._isreservedipv6("2600::") is False
    try:
        RdnsReaper._isreservedipv6("taco")
    except ValueError:
        assert True
    except AddrFormatError:
        assert True
    else:
        assert False

    try:
        RdnsReaper._isreservedipv6("10.0.0.1")
    except ValueError:
        assert True
    else:
        assert False


def test_remove_ip():
    dns = RdnsReaper()
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
    dns1 = RdnsReaper(allow_reserved_networks=True)
    dns1 += ["1.1.1.1", "8.8.8.8", "2600::", "10.255.254.253"]
    dns1.resolve_all()

    assert dns1["1.1.1.1"] == "one.one.one.one"
    assert dns1["2600::"] == "www.sprint.net"

    dns2 = RdnsReaper(limit_to_rfc1918=True)
    dns2.add(["1.1.1.1", "10.0.0.1"])
    assert "1.1.1.1" not in dns2._build_resolve_list()
    assert "10.0.0.1" in dns2._build_resolve_list()


def test_set_name():
    dns1 = RdnsReaper()
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


def test_set_file_1():
    try:
        os.remove("rdns_reaper/test/savetest.yaml")
    except FileNotFoundError:
        pass

    dns1 = RdnsReaper(filename="savetest.yaml", filemode="r")
    dns1.set_file(None)
    assert dns1._options_dict["filename"] is None
    assert dns1._options_dict["filemode"] is None

    dns1 = RdnsReaper(filename="savetest.yaml", filemode="r")
    dns1.set_file("savetest.yaml")
    assert dns1._options_dict["filename"] is None
    assert dns1._options_dict["filemode"] is None

    try:
        dns1.set_file(123)
    except TypeError:
        assert True
    else:
        assert False

    try:
        dns1.set_file("savetest.yaml", 53)
    except ValueError:
        assert True
    else:
        assert False

    dns2 = RdnsReaper()
    dns2.set_file("savetest.yaml", filemode="r")
    assert dns2._options_dict["filename"] == "savetest.yaml"
    assert dns2._options_dict["filemode"] == "r"
    dns2.set_file("savetest.yaml", filemode="w")
    assert dns2._options_dict["filename"] == "savetest.yaml"
    assert dns2._options_dict["filemode"] == "w"


def test_cleanup():
    try:
        os.remove("rdns_reaper/test/savetest.yaml")
    except FileNotFoundError:
        pass
    try:
        os.remove("savetest.yaml")
    except FileNotFoundError:
        pass
