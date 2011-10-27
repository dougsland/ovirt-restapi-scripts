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
USER     = "rhevm@ad.rhev3.com"
PASSWD   = "T0pSecreT!"

def getDataCenterId(dc_name):
 
	URL      = "https://" + ADDR + ":" + API_PORT + "/api/datacenters"

	request = urllib2.Request(URL)

	print "Preparing to remove: %s" %(dc_name)

	base64string = base64.encodestring('%s:%s' % (USER, PASSWD)).strip()
	request.add_header("Authorization", "Basic %s" % base64string)

	try:
		xmldata = urllib2.urlopen(request).read()
	except urllib2.URLError, e:
		print "Error: cannot connect to REST API: %s" % (e)
		print "\tTry to login using the same user/pass by the Admin Portal and check the error!"
		sys.exit(2)

	tree = ElementTree.XML(xmldata)
	list = tree.findall("data_center")

	dc_id = None
	for item in list:
		if dc_name == item.find("name").text:
			dc_id = item.attrib["id"]
			print "datacenter id %s" % (dc_id)
			break

	return dc_id


def removeDataCenter(dc_id):

	# Setting URL
	URL      = "https://" + ADDR + ":" + API_PORT + "/api/datacenters/" + str(dc_id)

	request = urllib2.Request(URL)
	print "connecting to: " + URL

	base64string = base64.encodestring('%s:%s' % (USER, PASSWD)).strip()
	request.add_header("Authorization", "Basic %s" % base64string)

	request.get_method = lambda: 'DELETE'

	try:
        	xmldata = urllib2.urlopen(request).read()
	except urllib2.URLError, e:
        	print "Error: cannot connect to REST API: %s" % (e)
		print "Possible errors: "
	        print "\t- Are you trying to remove an non existing item?"
	        print "\t- Try to login using the same user/pass by the Admin Portal and check the error!"
        	sys.exit(2)

	return 0

if __name__ == "__main__":

	if len(sys.argv) != 3:
		print "Usage: %s my_datacenter number_of_datacenter" %(sys.argv[0])
		sys.exit(1)

	nr_DC = sys.argv[2]

	for nrm in range(1,  int(nr_DC)):

        	name = sys.argv[1] + "_" + str(nrm)

		id_ret = getDataCenterId(name)

		if id_ret == None:
			print "Cannot find DataCenter"
			sys.exit(1)

		ret = removeDataCenter(id_ret)
		if ret == 0:
			print "DataCenter removed"

