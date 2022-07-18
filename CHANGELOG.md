# Changelog

## 0.0.12

Added option for allow/block list filtering with the .set_filter() method.  The .set_filter() method takes a single required parameter of an IP network formatted as a string, a list of IP networks formatted as strings, or a netaddr IPSet object.  The filter also takes an optional `mode` keyword argument with values of `allow` or `block` to change the filter between an allow filter or a block filter.

Users should not use the built-in simple RFC1918 filter if they are using this feature.
This feature will not disable the reserved IP address checking for things like loopback, multicast, documentation, and link-local addresses.

Added docstrings to allow for use of help() and .\_\_doc\_\_ for easier use of the library by third parties.

Changed to the GNU GPL v3.0 license.

## 0.0.11

Minor bug fixes and code documentation changes.  Significant changes to README file to update documentation on github and PyPI.

**Known Caveats** 

From 0.0.5: should probably change around the checking of addresses to make it less resource intensive if you are processing a large list - further work should be done here to improve this

## 0.0.10

**New Features**

Basic IPv6 support is now available.  Reserved IPv6 addresses (multicast, link local, etc), will automatically be ignored by default

**Known Caveats** 

From 0.0.5: should probably change around the checking of addresses to make it less resource intensive if you are processing a large list - further work should be done here to improve this

## 0.0.8

**Bugfixes**

Fixed a problem with the limit_to_rfc1918 function not actually doing anything

**Known Caveats** 

From 0.0.5: should probably change around the checking of addresses to make it less resource intensive if you are processing a large list

## 0.0.6

**Bugfixes**

Fixed a problem with version strings in __init__

**Known Caveats** 

From 0.0.5: should probably change around the checking of addresses to make it less resource intensive if you are processing a large list


## 0.0.5

**Bugfixes**

Fixed RFC1918 checking, added IPv4 version checking, check against the known reserved addresses (loopbacks, multicast, Class E, etc) and prevent resolver attempts against reserved addresses

**Known Caveats** 

should probably change around the checking of addresses to make it less resource intensive if you are processing a large list