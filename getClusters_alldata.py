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
<clusters>
    <cluster id="99408929-82cf-4dc7-a532-9d998063fa95" href="/api/clusters/99408929-82cf-4dc7-a532-9d998063fa95">
        <name>Default</name>
        <description>The default server cluster</description>
        <link rel="networks" href="/api/clusters/99408929-82cf-4dc7-a532-9d998063fa95/networks"/>
        <link rel="permissions" href="/api/clusters/99408929-82cf-4dc7-a532-9d998063fa95/permissions"/>
        <data_center id="c6a1fb7a-ca1f-11e0-9c91-5254006cd06b" href="/api/datacenters/c6a1fb7a-ca1f-11e0-9c91-5254006cd06b"/>
        <memory_policy>
            <overcommit percent="100"/>
            <transparent_hugepages>
                <enabled>false</enabled>
            </transparent_hugepages>
        </memory_policy>
        <scheduling_policy/>
        <version minor="0" major="3"/>
        <error_handling>
            <on_error>migrate</on_error>
        </error_handling>
    </cluster>
</clusters>
"""

# Example
ADDR     = "192.168.123.176"
API_PORT = "8443"
USER     = "rhevm@ad.rhev3.com"
PASSWD   = "T0pSecreT!"

# Setting URL
URL      = "https://" + ADDR + ":" + API_PORT + "/api/clusters"

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
list = tree.findall("cluster")

#print len(list)

for item in list:
	print "id:  %s"           % (item.attrib["id"])
	print "href:  %s"         % (item.attrib["href"])
	print "name: %s"          % (item.find("name").text)
	print "description: %s"   % (item.find("description").text)

	for subitem in item.findall("link"):
		print "link rel: %s"   % (subitem).attrib["rel"]
		print "link href: %s"  % (subitem).attrib["href"]

	print "data_center id: %s"                	    	       % (item.find("data_center").attrib["id"])
	print "data_center href: %s"              	    	       % (item.find("data_center").attrib["href"])
	print "memory_policy -> overcommit -> percent: %s"  	       % (item.find("memory_policy/overcommit").attrib["percent"])
	print "memory_policy -> transparent_hugepages -> enabled: %s"  % (item.find("memory_policy/transparent_hugepages/enabled").text)
	print "version minor: %s"                	    	       % (item.find("version").attrib["minor"])
	print "version major: %s"                	    	       % (item.find("version").attrib["major"])
	print "error_handling -> on_error: %s"  % (item.find("error_handling/on_error").text)
	print "\n"
