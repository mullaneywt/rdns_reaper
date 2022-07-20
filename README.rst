rdns-reaper: Reverse DNS Lookup Engine
======================================

rdns-reaper is a multi-threaded lookup engine for Python v3 to resolve DNS names from IP addresses.  IP addresses can be added to the custom class by a calling program individually or in batches, after which point the client triggers the resolver to execute on all IP addresses.  Once the lookup completes, the calling program can retrieve the data in a variety of ways.

The library currently runs on IPv4 addresses and IPv6 address.  Entries can be cached to disk to prevent excessive querying.  Limited filtering exists to restrict lookups to RFC1918 IPv4 space as an option.

rdns-reaper is currently tested with Python 3.6-3.11

https://github.com/mullaneywt/rdns_reaper