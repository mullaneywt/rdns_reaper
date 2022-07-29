from rdns_reaper import RdnsReaper as rdns_reaper


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
        limit_to_rfc1918=False,
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
    main()
    pass
