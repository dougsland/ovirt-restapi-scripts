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
from xml.etree import ElementTree

"""
EXAMPLE XML output
========================
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<networks>
    <network id="00000000-0000-0000-0000-000000000009" href="/api/networks/00000000-0000-0000-0000-000000000009">
        <name>rhevm</name>
        <description>Management Network</description>
        <data_center id="c6a1fb7a-ca1f-11e0-9c91-5254006cd06b" href="/api/datacenters/c6a1fb7a-ca1f-11e0-9c91-5254006cd06b"/>
        <stp>false</stp>
        <status>
            <state>operational</state>
        </status>
    </network>
    <network id="96883b27-3c09-44ee-a317-b8e0a40d87f8" href="/api/networks/96883b27-3c09-44ee-a317-b8e0a40d87f8">
        <name>rhevm</name>
        <description>Management Network</description>
        <data_center id="d2d438e3-24e2-4d65-bd69-a725634a3c0f" href="/api/datacenters/d2d438e3-24e2-4d65-bd69-a725634a3c0f"/>
        <stp>false</stp>
        <status>
            <state>non_operational</state>
        </status>
    </network>
</networks>
"""

# Example
ADDR     = "192.168.123.176"
API_PORT = "8443"
USER     = "rhevm@ad.rhev3.com"
PASSWD   = "T0pSecreT!"

# Setting URL
URL      = "https://" + ADDR + ":" + API_PORT + "/api/networks"

request = urllib2.Request(URL)
print "Connecting to: %s\n" % (URL)

base64string = base64.encodestring('%s:%s' % (USER, PASSWD)).strip()
request.add_header("Authorization", "Basic %s" % base64string)

try:
        xmldata = urllib2.urlopen(request).read()
except urllib2.URLError, e:
        print "Error: cannot connect to REST API: %s" % (e)
        print "Try to login using the same user/pass by the Admin Portal and check the error!"
        sys.exit(2)

#print xmldata 

tree = ElementTree.XML(xmldata)
list = tree.findall("network")

#print len(list)

for item in list:
	print "id:  %s"           % (item.attrib["id"])
	print "href:  %s"         % (item.attrib["href"])
	print "name: %s"          % (item.find("name").text)
	print "description: %s"   % (item.find("description").text)

	if item.find("data_center") != None:
		print "data_center id: %s"            % (item.find("data_center").attrib["id"])
		print "data_center href: %s"          % (item.find("data_center").attrib["href"])

	print "stp: %s"  		      % (item.find("stp").text)
	print "status -> state: %s"	      % (item.find("status/state").text)
	print "\n"
