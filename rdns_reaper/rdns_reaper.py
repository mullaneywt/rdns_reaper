import copy
import socket
import concurrent.futures
import yaml
from netaddr import IPAddress, IPSet, AddrFormatError

IPV4_RESERVED_NETWORK_LIST = [
    "0.0.0.0/8",
    "100.64.0.0/10",
    "127.0.0.0/8",
    "169.254.0.0/16",
    "192.0.0.0/24",
    "192.0.2.0/24",
    "192.88.99.0/24",
    "198.51.100.0/24",
    "203.0.113.0/24",
    "224.0.0.0/4",
    "233.252.0.0/24",
    "240.0.0.0/4",
    "255.255.255.255/32",
]

IPV4_RFC1918_NETWORK_LIST = [
    "10.0.0.0/8",
    "172.16.0.0/12",
    "192.168.0.0/16",
]

IPV6_RESERVED_NETWORK_LIST = [
    "::ffff:0:0/96",
    "::ffff:0:0:0/96",
    "64:ff9b::/96",
    "64:ff9b:1::/48",
    "100::/64",
    "2001:0000::/32",
    "2001:20::/28",
    "2001:db8::/32",
    "2002::/16",
    "fc00::/7",
    "fe80::/10",
    "ff00::/8",
]


class rdns_reaper:
<<<<<<< HEAD
    """Reverse DNS Lookup Engine."""

    _concurrent = 5
    _filter = None
    _filter_mode = None
=======
>>>>>>> eedcba2 (Refactoring)

    """Reverse DNS Lookup Engine."""

    _concurrent = 5
    _filter = None
    _filter_mode = None

    def __init__(self, **kwargs):
        """Initialize class and take in user options.

        Keyword Arguments:
            allow_reserved_networks (bool, optional): if True disable automatic filtering of
                reserved networks, must be set to True if checking of any reserved networks
                is desired.  Can then be supplemented with a custom filter
            concurrent (int, default = 5): number of concurrent resolver threads
            limit_to_rfc1918 (bool, optional): limit resolve to IPv4 RFC1918 only
            filter (str, list of strs, IPSet, optional): filter data
                can be a string containing an IP Address, list of strings, or an IPSet object
            filtermode ("block" | "allow", optional): sets filter mode to block list or allow list
                defaults to block list if not specified
            filename (str, optional): path and filename for disk based cache in YAML format
            filemode ("r" | "w"), required if filename set): read only or read-write mode for
                disk cache, if set to write, resolver may try to update the cache periodically
                the savefile() function can be called without arguments to force an update
            unresolvable (str, optional): string to set for each entry if resolving fails
                None is the default, all other options prevent subsequent lookups if disk based
                cache is in use


        """
        self._dns_dict = {}
        self._resolver_ip = None

        """Check for RFC1918 filtering"""
        if "limit_to_rfc1918" in kwargs:
            self.limit_to_rfc1918(kwargs["limit_to_rfc1918"])
        else:
            self._limit_to_rfc1918 = False

        """Check for custom filtering"""
        if kwargs.get("filter") is not None:
            if kwargs.get("filtermode") is not None:
                self.set_filter(kwargs["filter"], mode=kwargs["filtermode"])
            else:
                self.set_filter(kwargs["filter"])
<<<<<<< HEAD


        """Allow reserved network check"""
=======
        # else:
        #     self._filter = None
        #     self._filter_mode = None

        """Allow reserved network check"""

>>>>>>> eedcba2 (Refactoring)
        if kwargs.get("allow_reserved_networks"):
            self._allow_reserved_networks = True
        else:
            self._allow_reserved_networks = False

        """Process parallel lookup concurrency"""
        if kwargs.get("concurrent"):
            if isinstance(kwargs["concurrent"], int):
                self._concurrent = kwargs["concurrent"]
            else:
                raise TypeError

        """Determine how to mark unresolvable entries"""
        try:
            if type(kwargs["unresolvable"]) is str:
                self._unresolvable = kwargs["unresolvable"]
            else:
                raise TypeError
        except KeyError:
            self._unresolvable = None

        try:
            if type(kwargs["filemode"]) is str:
                self._filemode = kwargs["filemode"]
            else:
                raise TypeError
        except KeyError:
            self._filemode = None

        try:
            if type(kwargs["filename"]) is str:
                self._filename = kwargs["filename"]
            else:
                raise TypeError
        except KeyError:
            self._filename = None

        if (self._filename is not None) and (
            (self._filemode == "r") or (self._filemode == "w")
        ):
            try:
                self.loadfile(self._filename)
            except FileNotFoundError:
                pass

    def __add__(self, new):
        """Add two instances together and return a deepcopy."""
        self_copy = copy.deepcopy(self)
        if isinstance(new, rdns_reaper):
            self_copy._dns_dict.update(new._dns_dict)
        elif type(new) is str:
            self_copy.add_ip(new)
        elif type(new) is set:
            self_copy.add_ip_list(new)
        elif type(new) is list:
            self_copy.add_ip_list(new)
        else:
            raise TypeError
        return self_copy

    def __contains__(self, ip):
        """Allow for checking of IP in the instance."""
        if ip in self._dns_dict.keys():
            return True
        return False

    def __delitem__(self, ip):
        """Remove an item if del() is called."""
        self.remove_ip(ip)

    def __enter__(self):
        """Return self for use in 'with open()' style blocks."""
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Save file when class is being destroyed as appropriate."""
        if (self._filename is not None) and (self._filemode == "w"):
            self.savefile(self._filename)

    def __getitem__(self, ip):
        """Return IP address from internal dictionary, false if not found."""
        try:
            IPAddress(ip)
            return self._dns_dict[ip]
        except AddrFormatError:
            raise TypeError
        except KeyError:
            return False

    def __iadd__(self, new):
        """Add two instances together and return."""
        if isinstance(new, rdns_reaper):
            self._dns_dict.update(new._dns_dict)
        elif type(new) is str:
            self.add_ip(new)
        elif type(new) is set:
            self.add_ip_list(new)
        elif type(new) is list:
            self.add_ip_list(new)
        else:
            raise TypeError
        return self

    def __iter__(self):
        """Return an iterator as needed for k, v walking."""
        return self._reaper_iterator(self)

    def __len__(self):
        """Determine number of addresses in module."""
        return len(self._dns_dict)

    def __setitem__(self, ip_address, value):
        """Allow set/reset of hostname for an IP via index."""
        self.set_name(ip_address, value)

    def _resolve_function(self, ip_address):
        try:
            name = socket.gethostbyaddr(ip_address)[0]
            self._dns_dict[ip_address] = name
        except socket.herror:
            self._dns_dict[ip_address] = self._unresolvable
<<<<<<< HEAD

    def add(self, *args, **kwargs):
        self.__iadd__(*args, **kwargs)
=======
>>>>>>> eedcba2 (Refactoring)

    def add(self, *args, **kwargs):
        self.__iadd__(*args, **kwargs)

    def add_ip(self, ip, hostname=None):
        """Add an IP to the list with option hostname, skip if exists."""
        if ip in self._dns_dict.keys():
            return True

        try:
            IPAddress(ip)
            if hostname is None:
                self._dns_dict.update({ip: None})
            else:
                self._dns_dict.update({ip: hostname})
        except AddrFormatError:
            raise TypeError

    def add_ip_list(self, ip_list):
        """Add all new IP's from a list."""
        if type(ip_list) is set:
            ip_list = list(ip_list)
        if type(ip_list) is not list:
            raise TypeError
        for ip_address in ip_list:
            self.add_ip(ip_address)
<<<<<<< HEAD

    def allow_reserved_networks(self, option):
        """Allow users to enable/disable automatic filtering of reserved networks.

        If a user wants to check reserved network IPs (loopbacks, link local, multicast, etc.)
        they must set this option to True.  Users may manually filter some of the reserved
        networks with the filter() option.  This option *must* be set to True to resolve any
        reserved networks.  Using an allow filter with this option set to False will not resolve
        any reserved networks.

        Args:
            option (bool): Set to True to disable automatic filtering of reserved networks

        """
        if not isinstance(option, bool):
            raise TypeError

        self._allow_reserved_networks = option
=======
>>>>>>> eedcba2 (Refactoring)

    def allow_reserved_networks(self, option):
        if not isinstance(option, bool):
            raise TypeError

        self._allow_reserved_networks = option

    def clear_all_hostnames(self):
        """Clear all the hostnames from existing entries."""
        new_ip_dict = {ip: None for ip in self._dns_dict}
        self._dns_dict = new_ip_dict

<<<<<<< HEAD
=======

>>>>>>> eedcba2 (Refactoring)
    def clearname(self, ip_address):
        """Clear a specific IP's hostname.

        Args:
            ip (str): A string containing an IP address
        """
        try:
            ip_address = IPAddress(ip_address)
            self._dns_dict[ip_address] = None
            return True
        except AddrFormatError as error_case:
            raise TypeError from error_case
        except KeyError:
            return False

    def dict(self):
        """Return the internal dictionary to the calling function."""
        return self.dict()

    def get_dict(self):
        """Return the internal dictionary to the calling function."""
        return self._dns_dict

    def get_filter(self):
        """Return current filter status."""
        try:
            return (self._filter, self._filter_mode)
        except AttributeError:
            return None

    def get_options(self):
        """Return info about the various options set by the user"""
        options_dict = {
            "allow_reserved_networks": self._allow_reserved_networks,
            "concurrent": self._concurrent,
            "limit_to_rfc1918": self._limit_to_rfc1918,
            "filter": self._filter,
            "filtermode": self._filter_mode,
            "filename": self._filename,
            "filemode": self._filemode,
        }
        return options_dict

    def items(self):
        """Return the IP address and hostnames as k, v pairs in list format."""
        return {ip: hostname for ip, hostname in self._dns_dict.items()}.items()

    def keys(self):
        """Return the IP address as keys in list format."""
        return [ip for ip in self._dns_dict.keys()]

    def limit_to_rfc1918(self, value):
        """Set the RFC1918 filter."""
        if type(value) is not bool:
            raise TypeError
        self._limit_to_rfc1918 = value

    def loadfile(self, filename):
        """Load saved data in YAML format.

        Args
            filename (str): path and filename for the disk based YAML cache file
        """
<<<<<<< HEAD

=======
>>>>>>> eedcba2 (Refactoring)
        with open(filename, encoding="UTF-8") as f_handle:
            f_data = f_handle.read()
            self._dns_dict = yaml.safe_load(f_data)

    def remove_ip(self, ip_address):
        """Remove an IP from the list, return false if not found.

        Args:
            ip (str): A string containing an IP Address to remove
        """
        try:
            IPAddress(ip_address)
            self._dns_dict.pop(ip_address)
        except AddrFormatError as error_case:
            raise TypeError from error_case
        except KeyError:
            return False
        return True

    def _build_resolve_list(self):
        """Build list of IP's to perform resolver on, shared by serial and parallel methods."""
        if self._limit_to_rfc1918:
            IPv4_skipped_networks = IPSet(IPV4_RESERVED_NETWORK_LIST)
        elif self._allow_reserved_networks is False:
            IPv4_skipped_networks = IPSet(IPV4_RESERVED_NETWORK_LIST)
        else:
            IPv4_skipped_networks = IPSet()

        if self._allow_reserved_networks is False:
            IPv6_skipped_networks = IPSet(IPV6_RESERVED_NETWORK_LIST)
        else:
            IPv6_skipped_networks = IPSet()

        initial_ip_list = [
            key for key, value in self._dns_dict.items() if value is None
        ]

        pending_ipset = IPSet(initial_ip_list)

        if self._filter_mode == "block":
            result_ipset = pending_ipset - self._filter
            initial_pending_ips = [str(x) for x in result_ipset]
        elif self._filter_mode == "allow":
            result_ipset = pending_ipset & self._filter
            initial_pending_ips = [str(x) for x in result_ipset]
        else:
            initial_pending_ips = [str(x) for x in pending_ipset]

        pending_ips = list()

        for key in initial_pending_ips:
            address = IPAddress(key)

            if self._limit_to_rfc1918 is False:
                if (address.version == 4) and (address not in IPv4_skipped_networks):
                    pending_ips.append(key)
                elif (address.version == 6) and (address not in IPv6_skipped_networks):
                    pending_ips.append(key)
            else:
                if address in IPSet(IPV4_RFC1918_NETWORK_LIST):
                    pending_ips.append(key)

        return pending_ips

    def resolve_all(self):
        """Resolve all unknown IPs in parallel."""
        pending_ips = self._build_resolve_list()
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self._concurrent
        ) as executor:
            executor.map(self._resolve_function, set(pending_ips))

    def resolve_all_serial(self):
        """Resolve all unknown IPs serially."""
        pending_ips = self._build_resolve_list()

        for address in pending_ips:
            self._resolve_function(address)

    def savefile(self, filename=None):
        """Save internal dictionary to YAML file."""
        if filename is None and self._filename is not None and self._filemode == "w":
            filename = self._filename

        with open(filename, "w", encoding="UTF-8") as f_handle:
            f_handle.write("---\n")
            f_handle.write(yaml.dump(self._dns_dict))


    def set_name(self, ip_address, hostname):
        """Force the hostname of an IP.

        Args:
            ip_address (str): String containing an IP address to be modified
            hostname (str): Desired FQDN hostname to be set for this entry
                Can be None to reset record to allow for subsequent lookup
        """
        try:
            ip = IPAddress(ip)
            self._dns_dict[ip] = hostname
        except AddrFormatError:
            raise TypeError
        except KeyError:
            return False

    def set_resolver(self, resolver_ip):
        """Set the desired resolve IP - NOT WORKING."""
        try:
            IPAddress(resolver_ip)
            self._resolver_ip = resolver_ip
        except AddrFormatError:
            raise TypeError

    def set_filter(self, input, **kwargs):
        if kwargs.get("mode") is None:
            self._filter_mode = "block"
        elif kwargs.get("mode").lower() in ("allow", "block"):
            self._filter_mode = kwargs.get("mode").lower()
        else:
            raise ValueError

        if isinstance(input, str):
            input = IPSet([input])
        elif isinstance(input, list):
            input = IPSet(input)

        if not isinstance(input, IPSet):
            raise TypeError

        self._filter = input

    def values(self):
        """Return the hostnames as values in list format."""
        return [hostname for hostname in self._dns_dict.values()]

    @staticmethod
    def _isrfc1918(address_txt):
        """Determine if an address is RFC1918 private or not."""
        address = IPAddress(address_txt)
        rfc1918_networks = ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]
        rfc1918_IPSet = IPSet(rfc1918_networks)

        if address in rfc1918_IPSet:
            return True
        return False

    @staticmethod
    def _isreservedIPv4(address_txt):
        """Determine if an address is reserved (loopbacks, documentation, etc) or not."""
        address = IPAddress(address_txt)

        if address.version == 4:
            reserved_network_IPSet = IPSet(IPV4_RESERVED_NETWORK_LIST)
            if address_txt in reserved_network_IPSet:
                return True
            return False
        elif address.version == 6:
            reserved_network_IPSet = IPSet(IPV6_RESERVED_NETWORK_LIST)
            if address_txt in reserved_network_IPSet:
                return True
            return False
        else:
            raise ValueError

    @staticmethod
    def _isreservedIPv6(address_txt):
        """Determine if an address is reserved (loopbacks, documentation, etc) or not."""
        address = IPAddress(address_txt)

        if address.version == 6:
            reserved_network_IPSet = IPSet(IPV6_RESERVED_NETWORK_LIST)
            if address_txt in reserved_network_IPSet:
                return True
            return False
        else:
            raise ValueError

    class _reaper_iterator:
        def __init__(self, parentclass):
            self.__parentclass = parentclass
            self.__counter = 0
            self.__parent_len = len(parentclass)
            self.__parent_keys = list(parentclass.keys())

        def __iter__(self):
            return self

        def __next__(self):
            if self.__counter < self.__parent_len:
                key = self.__parent_keys[self.__counter]
                value = self.__parentclass[key]
                self.__counter += 1
                return (key, value)
            else:
                raise StopIteration
            pass
