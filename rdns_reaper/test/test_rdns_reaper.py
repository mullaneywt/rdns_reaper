import pytest
from rdns_reaper import rdns_reaper


def test_simpletest_1():
    dns = rdns_reaper()
    assert isinstance(dns, rdns_reaper)


def test_simple_iadd():
    dns = rdns_reaper()
    dns += "10.0.0.1"
    assert dns["10.0.0.1"] == None
