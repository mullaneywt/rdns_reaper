.. rdns_reaper documentation master file, created by
   sphinx-quickstart on Wed Jul 20 11:19:24 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

rdns-reaper: Reverse DNS Lookup Engine
======================================

rdns-reaper is a multi-threaded lookup engine for Python v3 to resolve DNS names from IP addresses.  IP addresses can be added to the custom class by a calling program individually or in batches, after which point the client triggers the resolver to execute on all IP addresses.  Once the lookup completes, the calling program can retrieve the data in a variety of ways.

The library currently runs on IPv4 addresses and IPv6 address.  Entries can be cached to disk to prevent excessive querying.  Limited filtering exists to restrict lookups to RFC1918 IPv4 space as an option.

rdns-reaper is currently tested with Python 3.6-3.12

Object Name Change
------------------

**Note that starting with version 0.1.0, the reaper object has been renamed from rdns_reaper to RdnsReaper**

For backwards compatability you can use the following import statement until your codebase is updated with the new name:

`from rdns_reaper import RdnsReaper as rdns_reaper`

The correct import statement for all new applications is:

`from rdns_reaper import RdnsReaper`

Important URLs:
---------------

* Bug Tracker: `https://github.com/mullaneywt/rdns_reaper/issues <https://github.com/mullaneywt/rdns_reaper/issues>`_
* Current Release Documentation: `https://rdns-reaper.readthedocs.io/en/latest/ <https://rdns-reaper.readthedocs.io/en/latest/>`_
* Release Candidate Documentation: `https://rdns-reaper.readthedocs.io/en/main/ <https://rdns-reaper.readthedocs.io/en/main/>`_
* Source Code: `http://github.com/mullaneywt/rdns_reaper <http://github.com/mullaneywt/rdns_reaper>`_
* PyPI: `https://pypi.org/project/rdns-reaper/ <https://pypi.org/project/rdns-reaper/>`_


Navigation
----------


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   install
   basicusage
   supported


Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`


License
-------

Licensed under the GNU GPL v3.0
