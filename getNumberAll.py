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

# Example
ADDR     = "192.168.123.176"
API_PORT = "8443"
USER     = "rhevm@ad.rhev3.com"  # Must provide @DOMAIN
PASSWD   = "T0pSecreT!"

def getNumber(apiName):

	if apiName == "datacenters":
		searchStr = "data_center" + "/name"
	elif apiName == "storagedomains":
		searchStr = "storage_domains" + "/name"
	else:
		# [:-1] - remove the last caracter in the string - in this case 's'
		# We use this approach to re-use the string of URL into the XML search (see below)
		searchStr = apiName[:-1] + "/name"

	# Setting URL
	URL      = "https://" + ADDR + ":" + API_PORT + "/api/" + apiName

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

	#print searchStr

	list = tree.findall(searchStr)

	#print len(list)

	counter = 0
	for item in list:
		counter += 1

	return counter

if __name__ == "__main__":
	print "Number of datacenters %s\n"    % (getNumber("datacenters"))
	print "Number of hosts %s\n"          % (getNumber("hosts"))
	print "Number of clusters %s\n"       % (getNumber("clusters"))
	print "Number of storagedomains %s\n" % (getNumber("storagedomains"))
	print "Number of templates %s\n"      % (getNumber("templates"))
	print "Number of roles %s\n"          % (getNumber("roles"))
	print "Number of networks %s\n"       % (getNumber("networks"))
	print "Number of tags %s\n"           % (getNumber("tags"))
	print "Number of groups %s\n"         % (getNumber("groups"))
	#print "Number of users %s\n"         % (getNumber("users"))
	#print "Number of vmpools %s\n"       % (getNumber("vmpools"))
	print "Number of vms %s\n"            % (getNumber("vms"))
