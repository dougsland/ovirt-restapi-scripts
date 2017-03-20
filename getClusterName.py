#!/usr/bin/python
#
# Copyright (C) 2011-2017
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
import ssl
from xml.etree import ElementTree

# Example
ADDR = "192.168.122.116"
API_PORT = "443"
USER = "admin@internal"  # Must provide @DOMAIN
PASSWD = "redhat"

# Setting URL
URL = "https://" + ADDR + ":" + API_PORT + "/api/clusters"

request = urllib2.Request(URL)
print("Connecting to: %s" % URL)

base64string = base64.encodestring('%s:%s' % (USER, PASSWD)).strip()
request.add_header("Authorization", "Basic %s" % base64string)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    xmldata = urllib2.urlopen(request, context=ctx).read()
except urllib2.URLError, e:
    print("Error: cannot connect to REST API: %s" % (e))
    print("Try to login using the same user/pass by "
          "the Admin Portal and check the error!")
    sys.exit(2)

tree = ElementTree.XML(xmldata)
list = tree.findall("cluster/name")

print("\nClusters found:")
for item in list:
    print("* %s" % item.text)
