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
<event id="3218" href="/api/events/3218">
        <description>User rhevm logged in.</description>
        <code>30</code>
        <severity>normal</severity>
        <time>2011-09-14T07:31:08.095-04:00</time>
        <user id="ce2375f6-4fe0-4fc9-8692-6f4b7b50a9d6" href="/api/users/ce2375f6-4fe0-4fc9-8692-6f4b7b50a9d6"/>
 </event>
"""

# Example
ADDR     = "192.168.123.176"
API_PORT = "8443"
USER     = "rhevm@ad.rhev3.com"
PASSWD   = "T0pSecreT!"

# Setting URL
URL      = "https://" + ADDR + ":" + API_PORT + "/api/events"

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
list = tree.findall("event")

#print len(list)

for item in list:
	print "id:  %s"           % (item.attrib["id"])
	print "href: %s"          % (item.attrib["href"])
	print "code: %s"          % (item.find("code").text)
	print "severity: %s"      % (item.find("severity").text)
	print "time: %s"          % (item.find("time").text)

	if item.find("user") <> None:
		print "user id: %s"       % (item.find("user").attrib["id"])
		print "user href: %s"     % (item.find("user").attrib["href"])

	if item.find("host") <> None:
		print "host id: %s"       % (item.find("host").attrib["id"])
		print "host href: %s"     % (item.find("host").attrib["href"])

	if item.find("cluster") <> None:
		print "cluster id: %s"       % (item.find("cluster").attrib["id"])
		print "cluster href: %s"     % (item.find("cluster").attrib["href"])

	print "\n"
