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
<data_centers>
    <data_center id="c6a1fb7a-ca1f-11e0-9c91-5254006cd06b" href="/api/datacenters/c6a1fb7a-ca1f-11e0-9c91-5254006cd06b">
        <name>Default</name>
        <description>The default Data Center</description>
        <link rel="storagedomains" href="/api/datacenters/c6a1fb7a-ca1f-11e0-9c91-5254006cd06b/storagedomains"/>
        <link rel="permissions" href="/api/datacenters/c6a1fb7a-ca1f-11e0-9c91-5254006cd06b/permissions"/>
        <storage_type>nfs</storage_type>
        <version minor="0" major="3"/>
        <supported_versions>
            <version minor="0" major="3"/>
        </supported_versions>
        <status>
            <state>uninitialized</state>
        </status>
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
list = tree.findall("data_center")

#print len(list)

for item in list:
	print "id:  %s"           % (item.attrib["id"])
	print "href: %s "         % (item.attrib["href"])
	print "name: %s"          % (item.find("name").text)
	print "description: %s"   % (item.find("description").text)
	for subitem in item.findall("link"):
		print "link ref: %s"      % (subitem.attrib["rel"])
		print "link href: %s"      % (subitem.attrib["href"])
	print "storage_type: %s"  % (item.find("storage_type").text)
	print "version minor: %s"  % (item.find("version").attrib["minor"])
	print "version major: %s"  % (item.find("version").attrib["major"])
	print "supported_versions minor: %s"  % (item.find("supported_versions/version").attrib["minor"])
	print "supported_versions major: %s"  % (item.find("supported_versions/version").attrib["major"])
	print "status: %s"  % (item.find("status/state").text)
	print "\n"
