[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rdns-reaper)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/rdns-reaper)
![PyPI](https://img.shields.io/pypi/v/rdns-reaper)
![piwheels](https://img.shields.io/piwheels/v/rdns-reaper)
![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/mullaneywt/rdns_reaper)

Build Status

![Read the Docs](https://img.shields.io/readthedocs/rdns_reaper)
![](https://github.com/mullaneywt/rdns_reaper/actions/workflows/releases_build.yaml/badge.svg)
![](https://github.com/mullaneywt/rdns_reaper/actions/workflows/main_build.yaml/badge.svg)
![](https://github.com/mullaneywt/rdns_reaper/actions/workflows/dev_build.yaml/badge.svg)

rdns-reaper: Reverse DNS Lookup Engine
======================================

rdns-reaper is a multi-threaded lookup engine for Python v3 to resolve DNS names from IP addresses.  IP addresses can be added to the custom class by a calling program individually or in batches, after which point the client triggers the resolver to execute on all IP addresses.  Once the lookup completes, the calling program can retrieve the data in a variety of ways.

The library currently runs on IPv4 addresses and IPv6 address.  Entries can be cached to disk to prevent excessive querying.  Limited filtering exists to restrict lookups to RFC1918 IPv4 space as an option.

rdns-reaper is currently tested with Python 3.6-3.11

Documentation
-------------

Read our documentation at https://rdns-reaper.readthedocs.io/en/latest/

Object Name Change
------------------

**Note that starting with version 0.1.0, the reaper object has been renamed from rdns_reaper to RdnsReaper**

For backwards compatability you can use the following import statement until your codebase is updated with the new name:

```python
>>> from rdns_reaper import RdnsReaper as rdns_reaper
```

The correct import statement for all new applications is:

```python
>>> from rdns_reaper import RdnsReaper
```


Installation and Usage
----------------------


### PyPI
```shell
$ pip install rdns-reaper

#For a specific version (e.g. 0.0.10)
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
>>> from rdns_reaper import RdnsReaper
>>> rdr = RdnsReaper(limit_to_rfc1918=False, concurrent=20, unresolvable=r"N\A")

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

### Supported parameters
The following parameters are supported when an instance of rdns_reaper is created:
|parameter|type|description|default|
|-|-|-|-|
| allow_reserved_networks | boolean | Disables automatic filtering of IPv4/IPv6 reserved networks | False |
| autosave | boolean | Automatically saves disk based cache when resolve_all() is called | False |
| limit_to_rfc1918 | boolean | Limits checking to only IPv4 RFC1918 address space (IPv6 entirely disabled) | False |
| concurrent | integer | Number of concurrent resolver threads to use | 5 |
| unresolvable | string | Value to populate if resolving fails | None |
| filemode | ["r"\|"w"] | read only or read-write disk cache | None |
| filename | string | Path and filename for YAML formatted disk cache | None |
| filter | IPSet, string, list of strings | Sets a custom IP filter | None |
| filtermode | ["allow"\|"block"] | set the filter mode to an allow list or a block list | None |

Note that entries with None as a value will be reprocessed in subsequent resolver runs, while entries with any other value from the `unresolveable` parameter will not be processed again without manual intervention

### Supported operators
* \+, which can add two rdns_reaper objects, a string with a single IP address, or a set/list with one or more IP addresses
* \+=, which can add two rdns_reaper objects, a string with a single IP address, or a set/list with one or more IP addresses

### Supported magic methods
* contains() - checks if a given string containing an IP address exists in the resolver instance
* del() - takes a string containing an IP address and removes it from the resolver instance
* getitem() - returns the resolved name for given string containing an IP address
* iter() - will provider an iterator that returns address/name tuples
* len() - number of unique IP addresses in a resolver instance

### Supported custom methods
* add_ip(IP) - adds an IP address (provided as a string)
* add_ip_list(IP_LIST) - adds IP addresses (provided as a list of strings)
* allow_reserved_networks() - disable/enable automatic filter of reserved networks
* autosave() - disable/enable automatic saving of disk based cache
* clear_all_hostnames() - resets all names to None across entire instance
* clearname(IP) - resets a name to None
* get_dict() - returns a dictionary with addresses as keys and names as values
* get_filter() - returns a tuple with custom filter information or None if not set
* get_options() - returns a dictionary listing options that have been set
* keys() - returns a list of all IP addresses in the instance
* loadfile() - forces a load of the YAML based disk cache
* limit_to_rfc1918 - disable/enable automatic filtering to only IPv4 RFC1918 networks
* remove_ip(IP) - removes an IP address (provided as a string)
* resolve_all() - launches a threaded resolver process
* resolve_all_serial() - launches a singular serial resolver process
* savefile() - forces a save of the YAML based disk cache
* set_file(FILENAME, MODE) - sets the filename and mode ("r"|"w") for disk based cache
* set_filter(IPSet, [mode=]) - sets a custom filter based on an IPSet, IP network in a string, or a list of strings containing IP networks.  Optional mode argument can be `block` or `allow` to set filtering to a block list or allow list
* set_name(IP, NAME) - forces the name for a value (provided as strings)
* values() - returns a list of all DNS names

Issues and contributing
-----------------------

If you find any issues, feel free to create a new issue at our github repository at: https://github.com/mullaneywt/rdns_reaper/issues

Make sure you include information about the version you're running, the environment you're running in, what data you've presented to the lookup engine, and what your responses/error information was.

Feature requests can also be created as an issue on github at the repository above.

For Python developers, if you have a new feature or a bug-fix that you've implemented, please open a pull request with some detailed information about what you intend to add or fix.

If you still having questions, feel free to email the maintainer.

License
-------

Licensed under GNU GPL V3.0.  See the LICENSE file for more information.
