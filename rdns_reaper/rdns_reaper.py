import copy
import socket
import yaml
import concurrent.futures
from netaddr import IPAddress, IPNetwork, AddrFormatError


class rdns_reaper:
    def __init__(self, *args, **kwargs):
        """Initialize class and take in user options."""
        self._dns_dict = dict()
        self._resolver_ip = None

        if "limit_to_rfc1918" in kwargs.keys():
            match kwargs["limit_to_rfc1918"]:
                case bool():
                    self._limit_to_rfc1918 = kwargs["limit_to_rfc1918"]
                case _:
                    #User passed an invalid response
                    self._limit_to_rfc1918 = False
        else:
            self._limit_to_rfc1918 = False





        """Process parallel lookup concurrency"""
        try:
            if type(kwargs["concurrent"]) is int:
                self._concurrent = kwargs["concurrent"]
            else:
                raise TypeError
        except KeyError:
            self._concurrent = 1

        




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
        if type(new) is rdns_reaper:
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
        """Return self for use in with blocks."""
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
        if type(new) is rdns_reaper:
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

    def __setitem__(self, ip, value):
        """Allow set/reset of hostname for an IP via index."""
        self.setname(ip, value)

    def _resolve_function(self, ip):
        try:
            name = socket.gethostbyaddr(ip)[0]
            self._dns_dict[ip] = name
        except socket.herror:
            self._dns_dict[ip] = self._unresolvable

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
        for ip in ip_list:
            self.add_ip(ip)

    def clear_all_hostnames(self):
        """Clear all the hostnames from existing entries."""
        new_ip_dict = {ip: None for ip in self._dns_dict}
        self._dns_dict = new_ip_dict

    def clearname(self, ip):
        """Clear a specific IP's hostname."""
        try:
            ip = IPAddress(ip)
            self._dns_dict[ip] = None
        except AddrFormatError:
            raise TypeError
        except KeyError:
            return False

    def dict(self):
        """Return the internal dictionary to the calling function."""
        return self.dict()

    def get_dict(self):
        """Return the internal dictionary to the calling function."""
        return self._dns_dict

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

    def loadfile(self, filename):
        """Load saved data in YAML format."""
        with open(filename) as f_handle:
            f_data = f_handle.read()
            self._dns_dict = yaml.safe_load(f_data)

    def remove_ip(self, ip):
        """Remove an IP from the list, return false if not found."""
        try:
            IPAddress(ip)
            self._dns_dict.pop(ip)
        except AddrFormatError:
            raise TypeError
        except KeyError:
            return False
        return True

    def resolve_all(self):
        """Resolve all unknown IPs in parallel."""
        pending_ips = [
            ip for ip, hostname in self._dns_dict.items() if hostname is None
        ]
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self._concurrent
        ) as executor:
            executor.map(self._resolve_function, set(pending_ips))

    def resolve_all_serial(self):
        """Resolve all unknown IPs serially."""
        pending_ips = [key for key, value in self._dns_dict.items() if value is None]
        for key in pending_ips:
            if self._limit_to_rfc1918:
                if self._isrfc1918(key) is False:
                    self._resolve_function(key)
            else:
                self._resolve_function(key)

    def savefile(self, filename=None):
        """Save internal dictionary to YAML file."""
        if filename is None and self._filename is not None and self._filemode == "w":
            filename = self._filename

        with open(filename, "w") as f_handle:
            f_handle.write("---\n")
            f_handle.write(yaml.dump(self._dns_dict))

    def setname(self, ip, hostname):
        """Force the hostname of an IP."""
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

    def values(self):
        """Return the hostnames as values in list format."""
        return [hostname for hostname in self._dns_dict.values()]

    @staticmethod
    def _isrfc1918(address_txt):
        """Determine if an address is RFC1918 private or not."""
        address = IPAddress(address_txt)
        n1 = IPNetwork("10.0.0.0/8")
        if address in n1:
            return True
        n2 = IPNetwork("172.16.0.0/12")
        if address in n2:
            return True
        n3 = IPNetwork("192.168.0.0/16")
        if address in n3:
            return True
        return False

    class _reaper_iterator:
        def __init__(self, parentclass):
            self.__parentclass = parentclass
            self.__counter = 0
            self.__parent_len = len(parentclass)
            self.__parent_keys = list(parentclass._dns_dict.keys())

        def __iter__(self):
            return self

        def __next__(self):
            if self.__counter < self.__parent_len:
                key = self.__parent_keys[self.__counter]
                value = self.__parentclass._dns_dict[key]
                self.__counter += 1
                return (key, value)
            else:
                raise StopIteration
            pass


def main():
    """Test functionality."""
    dr = rdns_reaper(limit_to_rfc1918=True, concurrent=20, unresolvable=r"N\A")
    dr2 = rdns_reaper(limit_to_rfc1918=True, concurrent=20, unresolvable=r"N\A")
    # dr.set_resolver("10.100.1.88")
    try:
        dr.loadfile("dns_test.yaml")
    except FileNotFoundError:
        pass

    # # dr.add_ip_list(["8.8.8.8", "1.1.1.1", "8.8.4.4", "10.100.1.88"])
    # dr.add_ip_list(["1.1.1.1", "10.100.1.88", "10.100.1.99"])
    # dr2.add_ip_list(["8.8.8.8", "8.8.4.4"])

    # dr += dr2
    # dr += "1.1.1.2"
    # dr += ["1.1.1.3", "1.1.1.4"]
    # # print(dr.__dict__)
    # dr.resolve_all()
    # # print("1.1.1.1" in dr)
    # # print(dr["1.1.1.1"])
    # # print("1.1.1.2" in dr)
    # # print(dr["1.1.1.2"])
    # dr.savefile("dns_test.yaml")


    d1 = rdns_reaper(
        limit_to_rfc1918=None,
        concurrent=20,
        unresolvable=r"N\A",
        filename="d1.yaml",
        filemode="w",
    )


    d1 += "1.1.1.1"
    d1 += "1.1.1.2"

    d1.resolve_all()
    d1.savefile()

    # close(d1)

    print(d1.__dict__)
    # for k, v in d1:
    #    print(f"{k} - {v}")


if __name__ == "__main__":
    # main()
    pass
