[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

rdns-reaper: Reverse DNS lookup Engine
======================================

rdns-reaper is a multi-threaded lookup engine for Python v3 to resolve DNS names from IP addresses.  IP addresses can be added to the custom class by a calling program individually or in batches, after which point the client triggers the resolver to execute on all IP addresses.  Once the lookup completes, the calling program can retrieve the data in a variety of ways.

The library currently only runs on IPv4 addresses, with IPv6 address functionality planned in the future.  Entries can be cached to disk to prevent excessive querying.  Limited filtering exists to restrict lookups to RFC1918 IP space as an option.


Installation and Usage
----------------------


### PyPI
```shell
$ pip install rdns-reaper
$
```

