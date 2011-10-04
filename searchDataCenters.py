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

import unittest
import base64
import urllib2
import sys
from xml.etree import ElementTree

ADDR     = "192.168.123.176"
API_PORT = "8443"
USER     = "rhevm@ad.rhev3.com"
PASSWD   = "T0pSecreT!"

if len(sys.argv) != 2:
        print "Usage: %s datacenter_name" %(sys.argv[0])
        print "Example: %s MyDataCenter"  %(sys.argv[0])
        sys.exit(1)

# Setting URL
URL      = "https://" + ADDR + ":" + API_PORT + "/api/datacenters?search=" + sys.argv[1]

request = urllib2.Request(URL)
print "Connecting to: " + URL

base64string = base64.encodestring('%s:%s' % (USER, PASSWD)).strip()
request.add_header("Authorization", "Basic %s" % base64string)
request.add_header('Content-Type', 'application/xml')

try:
	xmldata = urllib2.urlopen(request).read()
except urllib2.URLError, e:
	print "%s" %(e)
	sys.exit(-1)

tree = ElementTree.XML(xmldata)
lst = tree.findall("data_center")

if len(lst) == 0:
	print "Cannot find [%s] DataCenter!" % (sys.argv[1])
	sys.exit(-1)

for item in lst:
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
