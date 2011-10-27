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


if __name__ == "__main__":

	if len(sys.argv) != 3:
		print "Usage: %s datacenter cluster_name" %(sys.argv[0])
		print "Example: %s my_datacenter nfs" %(sys.argv[0])
		sys.exit(1)

	print "Creating cluster %s" %(sys.argv[1])

	id_ret = getDataCenterId(sys.argv[1])

	if id_ret == None:
                print "Cannot find DataCenter"
                sys.exit(1)

	print id_ret

	xml_request ="""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<cluster>
	    <name>""" + sys.argv[2] + """</name>
    	    <cpu id=\"Intel Conroe Family\"/>
            <data_center id="""+"\""+ """"""+id_ret+""""""+ "\""+"""/>
        </cluster>
	"""

	# Setting URL
	URL      = "https://" + ADDR + ":" + API_PORT + "/api/clusters"


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
