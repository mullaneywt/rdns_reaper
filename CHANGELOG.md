# Changelog

## 0.0.5

**Bugfixes**
Fixed RFC1918 checking, added IPv4 version checking, check against the known reserved addresses (loopbacks, multicast, Class E, etc) and prevent resolver attempts against reserved addresses

**Known Caveats** 
should probably change around the checking of addresses to make it less resource intensive if you are processing a large list