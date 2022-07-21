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
    """Reverse DNS Lookup Engine."""

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
        self._resolver_ip = None
        self._dns_dict = {}
        self._concurrent = 5
        self._options_dict = {
            "allow_reserved_networks": False,
            "concurrent": 5,
            "filemode": None,
            "filename": None,
            "filter": None,
            "filter_mode": None,
            "limit_to_rfc1918": False,
        }
        """Check for RFC1918 filtering"""
        if "limit_to_rfc1918" in kwargs:
            self.limit_to_rfc1918(kwargs["limit_to_rfc1918"])
        else:
            self._options_dict["limit_to_rfc1918"] = False

        """Check for custom filtering"""
        if kwargs.get("filter") is not None:
            self.set_filter(kwargs.get("filter"), mode=kwargs.get("filtermode"))
         
        """Allow reserved network check"""
        if kwargs.get("allow_reserved_networks"):
            self._options_dict["allow_reserved_networks"] = True
        else:
            self._options_dict["allow_reserved_networks"] = False

        """Process parallel lookup concurrency"""
        if kwargs.get("concurrent"):
            if isinstance(kwargs["concurrent"], int):
                self._options_dict["concurrent"] = kwargs["concurrent"]
            else:
                raise TypeError

        """Determine how to mark unresolvable entries"""
        try:
            if isinstance(kwargs["unresolvable"], str):
                self._unresolvable = kwargs["unresolvable"]
            else:
                raise TypeError
        except KeyError:
            self._unresolvable = None

        try:
            if isinstance(kwargs["filemode"], str):
                self._options_dict["filemode"] = kwargs["filemode"]
            else:
                raise TypeError
        except KeyError:
            pass

        try:
            if isinstance(kwargs["filename"], str):
                self._options_dict["filename"] = kwargs["filename"]
            else:
                raise TypeError
        except KeyError:
            pass

        if (self._options_dict["filename"] is not None) and (
            self._options_dict["filemode"] in ("r", "w")
        ):
            try:
                self.loadfile(self._options_dict["filename"])
            except FileNotFoundError:
                pass

    def __add__(self, new):
        """Add two instances together and return a deepcopy."""
        self_copy = copy.deepcopy(self)
        if isinstance(new, rdns_reaper):
            self_copy._dns_dict.update(new._dns_dict)
        elif isinstance(new, str):
            self_copy.add_ip(new)
        elif isinstance(new, set):
            self_copy.add_ip_list(new)
        elif isinstance(new, list):
            self_copy.add_ip_list(new)
        else:
            raise TypeError
        return self_copy

    def __contains__(self, ip_address):
        """Allow for checking of IP in the instance."""
        if ip_address in self._dns_dict.keys():
            return True
        return False

    def __delitem__(self, ip_address):
        """Remove an item if del() is called."""
        self.remove_ip(ip_address)

    def __enter__(self):
        """Return self for use in 'with open()' style blocks."""
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Save file when class is being destroyed as appropriate."""
        if (self._options_dict["filename"] is not None) and (
            self._options_dict["filemode"] == "w"
        ):
            self.savefile(self._options_dict["filename"])

    def __getitem__(self, ip_address):
        """Return IP address from internal dictionary, false if not found."""
        try:
            IPAddress(ip_address)
            return self._dns_dict[ip_address]
        except AddrFormatError:
            raise TypeError
        except KeyError:
            return False

    def __iadd__(self, new):
        """Add two instances together and return."""
        if isinstance(new, rdns_reaper):
            self._dns_dict.update(new._dns_dict)
        elif isinstance(new, str):
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

    def add(self, *args, **kwargs):
        """Generalized function for adding."""
        self.__iadd__(*args, **kwargs)

    def add_ip(self, ip_address, hostname=None):
        """Add an IP to the list with option hostname, skip if exists."""
        if ip_address in self._dns_dict.keys():
            return True

        try:
            IPAddress(ip_address)
            if hostname is None:
                self._dns_dict.update({ip_address: None})
            else:
                self._dns_dict.update({ip_address: hostname})
            return ip_address
        except AddrFormatError as error_case:
            raise TypeError from error_case

    def add_ip_list(self, ip_list):
        """Add all new IP's from a list."""
        if isinstance(ip_list, set):
            ip_list = list(ip_list)
        if not isinstance(ip_list, list):
            raise TypeError
        for ip_address in ip_list:
            self.add_ip(ip_address)

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

        self._options_dict["allow_reserved_networks"] = option

    def clear_all_hostnames(self):
        """Clear all the hostnames from existing entries."""
        new_ip_dict = {ip: None for ip in self._dns_dict}
        self._dns_dict = new_ip_dict

    def clearname(self, ip_address):
        """Clear a specific IP's hostname.

        Args:
            ip (str): A string containing an IP address
        """
        try:
            IPAddress(ip_address)
        except AddrFormatError as error_case:
            raise TypeError from error_case
        
        if ip_address not in self._dns_dict.keys():
            raise KeyError("Address not found")

        self._dns_dict[ip_address] = None

    def dict(self):
        """Return the internal dictionary to the calling function."""
        return self.dict()

    def get_dict(self):
        """Return the internal dictionary to the calling function."""
        return self._dns_dict

    def get_filter(self):
        """Return current filter status."""
        return (self._options_dict["filter"], self._options_dict["filter_mode"])
        # try:
        # except AttributeError:
            # return None

    def get_options(self):
        """Return info about the various options set by the user"""
        # options_dict = {
        #     "allow_reserved_networks": self._allow_reserved_networks,
        #     "concurrent": self._concurrent,
        #     "limit_to_rfc1918": self._limit_to_rfc1918,
        #     "filter": self._filter,
        #     "filtermode": self._filter_mode,
        #     "filename": self._filename,
        #     "filemode": self._filemode,
        # }
        return self._options_dict

    def items(self):
        """Return the IP address and hostnames as k, v pairs in list format."""
        return dict(self._dns_dict.items())

    def keys(self):
        """Return the IP address as keys in list format."""
        return list(self._dns_dict.keys())

    def limit_to_rfc1918(self, value):
        """Set the RFC1918 filter."""
        if not isinstance(value, bool):
            raise TypeError
        self._options_dict["limit_to_rfc1918"] = value

    def loadfile(self, filename):
        """Load saved data in YAML format.

        Args
            filename (str): path and filename for the disk based YAML cache file
        """
        with open(filename) as f_handle:
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
        if self._options_dict["limit_to_rfc1918"]:
            IPv4_skipped_networks = IPSet(IPV4_RESERVED_NETWORK_LIST)
        elif self._options_dict["allow_reserved_networks"] is False:
            IPv4_skipped_networks = IPSet(IPV4_RESERVED_NETWORK_LIST)
        else:
            IPv4_skipped_networks = IPSet()

        if self._options_dict["allow_reserved_networks"] is False:
            IPv6_skipped_networks = IPSet(IPV6_RESERVED_NETWORK_LIST)
        else:
            IPv6_skipped_networks = IPSet()

        initial_ip_list = [
            key for key, value in self._dns_dict.items() if value is None
        ]

        pending_ipset = IPSet(initial_ip_list)

        if self._options_dict["filter_mode"] == "block":
            result_ipset = pending_ipset - self._options_dict["filter"]
            initial_pending_ips = [str(x) for x in result_ipset]
        elif self._options_dict["filter_mode"] == "allow":
            result_ipset = pending_ipset & self._options_dict["filter"]
            initial_pending_ips = [str(x) for x in result_ipset]
        else:
            initial_pending_ips = [str(x) for x in pending_ipset]

        pending_ips = []

        for key in initial_pending_ips:
            address = IPAddress(key)

            if self._options_dict["limit_to_rfc1918"] is False:
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
            max_workers=self._options_dict["concurrent"]
        ) as executor:
            executor.map(self._resolve_function, set(pending_ips))

    def resolve_all_serial(self):
        """Resolve all unknown IPs serially."""
        pending_ips = self._build_resolve_list()

        for address in pending_ips:
            self._resolve_function(address)

    def savefile(self, filename=None):
        """Save internal dictionary to YAML file."""
        if (
            filename is None
            and self._options_dict["filename"] is not None
            and self._options_dict["filemode"] == "w"
        ):
            filename = self._options_dict["filename"]

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
            IPAddress(ip_address)
        except AddrFormatError as error_case:
            raise TypeError(f"IP Error: {error_case}") from error_case

        if ip_address not in self._dns_dict.keys():
            raise KeyError("Address does not exist")
        self._dns_dict[ip_address] = hostname
        # except KeyError as error_case:
        # raise KeyError("Address does not exist")

    def set_resolver(self, resolver_ip):
        """Set the desired resolve IP - NOT WORKING."""
        try:
            IPAddress(resolver_ip)
            self._resolver_ip = resolver_ip
        except AddrFormatError:
            raise TypeError

    def set_filter(self, filter_data, **kwargs):
        print(filter_data)
        print(kwargs)
        if kwargs.get("mode") is None:
            self._options_dict["filter_mode"] = "block"
        elif kwargs.get("mode").lower() in ("allow", "block"):
            self._options_dict["filter_mode"] = kwargs.get("mode").lower()
        else:
            raise ValueError

        if isinstance(filter_data, str):
            filter_data = IPSet([filter_data])
        elif isinstance(filter_data, list):
            filter_data = IPSet(filter_data)

        if not isinstance(filter_data, IPSet):
            raise TypeError

        self._options_dict["filter"] = filter_data

    def values(self):
        """Return the hostnames as values in list format."""
        return list(self._dns_dict.values())

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
    def _isreservedaddress(address_txt):
        """Determine if an address is reserved (loopbacks, documentation, etc) or not."""
        address = IPAddress(address_txt)

        if address.version == 4:
            return rdns_reaper._isreservedIPv4(address_txt)
        elif address.version == 6:
            return rdns_reaper._isreservedIPv6(address_txt)
        else:
            raise ValueError

    @staticmethod
    def _isreservedIPv4(address_txt):
        """Determine if an address is reserved (loopbacks, documentation, etc) or not."""
        address = IPAddress(address_txt)

        if address.version == 4:
            reserved_network_IPSet = IPSet(IPV4_RESERVED_NETWORK_LIST)
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
