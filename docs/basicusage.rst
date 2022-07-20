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

Prepare your addresses to be resolved.  This can be a single string with a single address, a list of strings each containing a single address, or an IPSet containing multiple addresses.  If using an IPSet, make sure you pass a /32 or /128 address, not a network

>>> ips_to_resolve = ["1.1.1.1", "8.8.8.8"]

The `add()` function should be able to detect and handle any format.  You can also use the + or += operators to add items, or to add two rdns_reaper instances together.  The `resolve_all()` function will start a parallel resolver and attempt to get the names for all addresses, with 5 threads by default.

>>> dns.add(ips_to_resolve)
>>> dns.resolve_all()

You can get an individual item by address from the resolver

>>> print(dns["1.1.1.1"])

Or you can iterate over the resolver to get a tuple for each item

>>> for address, name in dns:
>>>     print(f"{address} is called {name}")

Output:

1.1.1.1 is called one.one.one.one
8.8.8.8 is called dns.google
