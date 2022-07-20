.. rdns_reaper documentation master file, created by
   sphinx-quickstart on Wed Jul 20 11:19:24 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

rdns-reaper: Reverse DNS Lookup Engine
======================================

rdns-reaper is a multi-threaded lookup engine for Python v3 to resolve DNS names from IP addresses.  IP addresses can be added to the custom class by a calling program individually or in batches, after which point the client triggers the resolver to execute on all IP addresses.  Once the lookup completes, the calling program can retrieve the data in a variety of ways.

The library currently runs on IPv4 addresses and IPv6 address.  Entries can be cached to disk to prevent excessive querying.  Limited filtering exists to restrict lookups to RFC1918 IPv4 space as an option.

rdns-reaper is currently tested with Python 3.6-3.11


.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   install
   rdns_reaper

Usage
-----

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


Supported operators
-------------------

* \+, which can add two rdns_reaper objects, a string with a single IP address, or a set/list with one or more IP addresses 
* \+=, which can add two rdns_reaper objects, a string with a single IP address, or a set/list with one or more IP addresses

Supported magic methods
-----------------------

* contains() - checks if a given string containing an IP address exists in the resolver instance
* del() - takes a string containing an IP address and removes it from the resolver instance
* getitem() - returns the resolved name for given string containing an IP address
* iter() - will provider an iterator that returns address/name tuples
* len() - number of unique IP addresses in a resolver instance

Supported custom methods
------------------------

* add_ip(IP) - adds an IP address (provided as a string)
* add_ip_list(IP_LIST) - adds IP addresses (provided as a list of strings)
* allow_reserved_networks() - disable/enable automatic filter of reserved networks
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
* setname(IP, NAME) - forces the name for a value (provided as strings)
* set_filter(IPSet, [mode=]) - sets a custom filter based on an IPSet, IP network in a string, or a list of strings containing IP networks.  Optional mode argument can be `block` or `allow` to set filtering to a block list or allow list
* values() - returns a list of all DNS names

License
-------

Licensed under the GNU GPL v3.0


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`