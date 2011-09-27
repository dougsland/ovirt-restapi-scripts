#!/usr/bin/python
#
# Copyright (C) 2011
#
# Douglas Schilling Landgraf <dougsland@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import urllib2
import base64
import sys

xml_request ="""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<data_center>
	<name>SuperDataCenter</name>
	<storage_type>nfs</storage_type>
	<version minor=\"0\" major=\"3\"/>
</data_center>
"""

# Example
ADDR     = "192.168.123.176"
API_PORT = "8443"
USER     = "rhevm@ad.rhev3.com"
PASSWD   = "T0pSecreT!"

# Setting URL
URL      = "https://" + ADDR + ":" + API_PORT + "/api/datacenters"


request = urllib2.Request(URL)
print "Connecting to: " + URL

base64string = base64.encodestring('%s:%s' % (USER, PASSWD)).strip()
request.add_header("Authorization", "Basic %s" % base64string)
request.add_header('Content-Type', 'application/xml')

try:
	ret = urllib2.urlopen(request, xml_request)
except urllib2.URLError, e:
	print "%s" %(e)
	print "Are you trying to add an existing item?"
	sys.exit(-1)

print "Done!"

# To see the response from the server 
#response = ret.read()
#print response
