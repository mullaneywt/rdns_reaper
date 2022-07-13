# Changelog

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