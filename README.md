[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rdns-reaper)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/rdns-reaper)
![PyPI](https://img.shields.io/pypi/v/rdns-reaper)
![piwheels](https://img.shields.io/piwheels/v/rdns-reaper)

rdns-reaper: Reverse DNS lookup Engine
======================================

rdns-reaper is a multi-threaded lookup engine for Python v3 to resolve DNS names from IP addresses.  IP addresses can be added to the custom class by a calling program individually or in batches, after which point the client triggers the resolver to execute on all IP addresses.  Once the lookup completes, the calling program can retrieve the data in a variety of ways.

The library currently runs on IPv4 addresses and IPv6 address.  Entries can be cached to disk to prevent excessive querying.  Limited filtering exists to restrict lookups to RFC1918 IPv4 space as an option.

rdns-reaper is currently tested with Python 3.6-3.11


Installation and Usage
----------------------


### PyPI
```shell
$ pip install rdns-reaper
#or for a specific version (e.g. 0.0.10)
$ pip install rdns-reaper==0.0.10
```

### Github with PIP
```shell
#Latest Full Release
$ pip install git+https://github.com/mullaneywt/rdns_reaper/@releases
#Latest Release Candidate
$ pip install git+https://github.com/mullaneywt/rdns_reaper/
#Specific Release Version (e.g. 0.0.10)
$ pip install git+https://github.com/mullaneywt/rdns_reaper/@0.0.10
```

### Usage
```python
>>> from rdns_reaper import rdns_reaper
>>> rdr = rdns_reaper(limit_to_rfc1918=False, concurrent=20, unresolvable=r"N\A")

>>> iplist = ["8.8.8.8", "1.1.1.1", "8.8.4.4"]
>>> rdr.add_ip_list(iplist)
>>> rdr.resolve_all()

>>> rdr["1.1.1.1"]
one.one.one.one

>>> for address in rdr:
>>>   print(address)
{
	('8.8.8.8', 'dns.google')
	('1.1.1.1', 'one.one.one.one')
	('8.8.4.4', 'dns.google')
}
```

License
-------

This project currently is not licensed for use by third parties and all rights are retained by the creator.  Plans for adoption of a common open source license are in the works.