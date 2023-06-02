==================
Supported Features
==================

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
