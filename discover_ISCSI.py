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

def getHostId(host_name):

        URL      = "https://" + ADDR + ":" + API_PORT + "/api/hosts"

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
        list = tree.findall("host")

        host_id = None
        for item in list:
                if host_name == item.find("name").text:
                        host_id = item.attrib["id"]
                        print "host id %s" % (host_id)
                        break

        return host_id


if __name__ == "__main__":

	if len(sys.argv) != 3:
		print "Usage: %s MyHost MySan_Address" %(sys.argv[0])
		print "Example: %s MyHost MySan_Address" %(sys.argv[0])
		sys.exit(1)

	print "Host:     %s" %(sys.argv[1]) 
	print "MySan_Address:  %s" %(sys.argv[2])

	id_ret = getHostId(sys.argv[1])

        if id_ret == None:
                print "Cannot find Host"
                sys.exit(1)

	# Setting URL
	URL      = "https://" + ADDR + ":" + API_PORT + "/api/hosts/" + id_ret + "/iscsidiscover"

	xml_request ="""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<action>
		<iscsi>
			<address>"""  + sys.argv[2]  + """</address>
		</iscsi>
	</action>
	"""

	#print xml_request

	request = urllib2.Request(URL)
	print "Connecting to: " + URL

	base64string = base64.encodestring('%s:%s' % (USER, PASSWD)).strip()
	request.add_header("Authorization", "Basic %s" % base64string)
	request.add_header('Content-Type', 'application/xml')

	try:
		ret = urllib2.urlopen(request, xml_request)
	except urllib2.URLError, e:
		print "%s" %(e)
		print "possible issues:"
		print "- check if selected host is using a datacenter with iscsi support"
		print "- Are you trying to add an existing item?"
		sys.exit(-1)

	print "Done!\n"

	print "Response from server:"
	print "========================"
	# To see the response from the server 
	response = ret.read()
        tree = ElementTree.XML(response)

	#print response
        list = tree.findall("iscsi")
	for item in list:
		print "iscsi/address: %s" % (item.find("address").text)

        list = tree.findall("status")
	for item in list:
		print "status/state: %s" % (item.find("state").text)
        
	list = tree.findall("iscsi_target")
	for item in list:
		print "iscsi_target: %s:" % (item.text)
