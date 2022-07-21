===========
Basic Usage
===========


Create an rdns_reaper instance
------------------------------

>>> from rdns_reaper import rdns_reaper
>>> rdr = rdns_reaper(limit_to_rfc1918=False, concurrent=20, unresolvable=r"N\A")

The `rnds_reaper` module can be imported and assigned in your program to a name of your chosing.  No arguments are required, although several keyword arguments are available.


Simple lookup example
---------------------

Create an instance of the class

>>> dns = rdns_reaper()

Prepare your addresses to be resolved.  This can be a single string with a single address, a list of strings each containing a single address, or an IPSet containing multiple addresses.  If using an IPSet, make sure you pass a /32 or /128 address, not a network.

>>> ips_to_resolve = ["1.1.1.1", "8.8.8.8"]

The `add()` function should be able to detect and handle any format.  You can also use the + or += operators to add items, or to add two rdns_reaper instances together.  The `resolve_all()` function will start a parallel resolver and attempt to get the names for all addresses, with 5 threads by default.

>>> dns.add(ips_to_resolve)
>>> dns.resolve_all()

You can get an individual item by address from the resolver.

>>> print(dns["1.1.1.1"])

Or you can iterate over the resolver to get a tuple for each item.

>>> for address, name in dns:
>>>     print(f"{address} is called {name}")

Output:

>>> 1.1.1.1 is called one.one.one.one
>>> 8.8.8.8 is called dns.google


Limit to RFC1918
----------------

If you are using IPv4 exclusively and want to check only internal RFC1918 addresses, you can add a `limit_to_rfc1918` keyword argument to limit your lookup queries.  Any address passed to the module that is IPv6 or IPv4 outside of RFC1918 is silently discarded.

>>> dns = rdns_reaper(limit_to_rfc1918=True)
>>> ips_to_resolve = ["1.1.1.1", "8.8.8.8", "10.0.0.1"]
>>> dns.add(ips_to_resolve)
>>> dns.resolve_all()
>>> print(dns.items())
>>> for address, name in dns:
>>>     print(f"{address} is called {name}")

Output

>>> 1.1.1.1 is called None
>>> 8.8.8.8 is called None
>>> 10.0.0.0 is called host1.myhost.example.com

Override automatic filtering
----------------------------

Reserved networks in the IPv4 and IPv6 address space are automatically skipped by default.  This includes things like loopback space, documentation addresses, multicast addresses, etc.

If you want to search in this area, pass the `allow_reserved_networks` keyword argument

>>> dns = rdns_reaper(allow_reserved_networks=True)
>>> dns.add("225.0.0.1")
>>> dns.resolve_all()
>>> dns["225.0.0.1"]

Output

>>> multicastgroup1.example.com


Custom filtering
----------------

You can define a custom filter as an allowlist or a blocklist.  The filter can mix both IPv4 and IPv6 addressing together.  This filter will not work correctly if the `limit_rfc_1918` option is set to True, unless you are only using filtering inside the RFC1918 space.  If you want to allow reserved networks while also using a custom filter, you'll need to enable the `allow_reserved_networks` feature while also using the filter

Example allowing searching of only the 10/8 and 172.16/12 RFC1918 spaces.

>>> filter_data = ["10.0.0.0/8", "172.16.0.0/12"]
>>> dns = rdns_reaper(filter=filterdata, filtermode="allow")

Example preventing searching the RFC1918 space

>>> filter_data = ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]
>>> dns = rdns_reaper(filter=filterdata, filtermode="block")

If `filtermode` is not specified then the default is a blocklist.

Disk based cache
----------------

A disk based cache in YAML format is available to store data between executions of the resolver engine.  The keyword argument `filename` containing an optional path and filename for the cache is presented when the instance is created, along with a `w` or `r` argument as a `filemode` keyword argument to setup the resolver as read-write or read only.

The cache, if it exists, is automatically read in when an instance is created, including both the IP address and hostname (is previously resolved).  The cache can be saved to disk by calling the `savefile()` method or will automatically be saved if used inside of a `with open() as handle` style block. 

If a cache file doesn't exit, the resolver starts with an empty dictionary and will create the file upon execution of the `savefile()` method.

Build an initial cache, resolve entries, and store

>>> dns1 = rdns_reaper(filename="cache.yaml", filemode="w")
>>> ips_to_resolve = ["1.1.1.1", "8.8.8.8"]
>>> dns1.add(ips_to_resolve)
>>> dns1.resolve_all()
>>> dns1.savefile()

Create a new instance and read in the cache

>>> dns2 = rdns_reaper(filename="cache.yaml", filemode="r")
>>> print(dns2.items())

Output

>>> {'1.1.1.1': 'one.one.one.one', '8.8.8.8': 'dns.google'}