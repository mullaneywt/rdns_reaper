===========
Basic Usage
===========


Create an rdns_reaper instance
------------------------------

>>> from rdns_reaper import rdns_reaper
>>> rdr = rdns_reaper(limit_to_rfc1918=False, concurrent=20, unresolvable=r"N\A")

The `rnds_reaper` module can be imported and assigned in your program to a name of your chosing.  No arguments are required, although several keyword arguments are available.


Simple lookup 

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