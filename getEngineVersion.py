#!/usr/bin/python
#
# Copyright (C) 2013
#
# Douglas Schilling Landgraf <dougsland@gmail.com>
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

# Example
ADDR     = "192.168.1.16"
API_PORT = "443"
USER     = "admin@internal"
PASSWD   = "mySuperPassword"

# Setting URL
URL      = "https://" + ADDR + ":" + API_PORT + "/api"

request = urllib2.Request(URL)
print "Connecting to: " + URL

base64string = base64.encodestring('%s:%s' % (USER, PASSWD)).strip()
request.add_header("Authorization", "Basic %s" % base64string)

try:
        xmldata = urllib2.urlopen(request).read()
except urllib2.URLError, e:
        print "Error: cannot connect to REST API: %s" % (e)
        print "Try to login using the same user/pass by the Admin Portal and check the error!"
        sys.exit(2)

tree = ElementTree.XML(xmldata)
list = tree.findall("product_info")

for item in list:
        print item.find("name").text
        print item.find("version").attrib
