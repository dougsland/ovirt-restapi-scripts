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

	if len(sys.argv) != 4:
		print "Usage: %s My_Storage_Name MyHostAddress path" %(sys.argv[0])
		print "Example: %s my_storage 192.168.1.60 /data/image/pendriveFS" %(sys.argv[0])
		sys.exit(1)

	print "Creating storage %s" %(sys.argv[1])

	#print xml_request

	print "Host: %s" %(sys.argv[2])
	id_ret = getHostId(sys.argv[2])

        if id_ret == None:
                print "Cannot find Host"
                sys.exit(1)

	# Setting URL
	URL      = "https://" + ADDR + ":" + API_PORT + "/api/storagedomains"

	xml_request ="""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<storage_domain>
		<name>""" + sys.argv[1] + """</name>
		<type>data</type>
		<host id="""+"\""+ """"""+id_ret+""""""+ "\""+"""/>
	<storage>
		<type>localfs</type>
		<path>""" + sys.argv[3] + """</path>
	</storage>
	</storage_domain>
	"""

	#print xml_request

	request = urllib2.Request(URL)
	print "Connecting to: " + URL
	print "Executing..."
	base64string = base64.encodestring('%s:%s' % (USER, PASSWD)).strip()
	request.add_header("Authorization", "Basic %s" % base64string)
	request.add_header('Content-Type', 'application/xml')

	try:
		ret = urllib2.urlopen(request, xml_request)
	except urllib2.URLError, e:
		print "%s" %(e)
		print "possible issues:"
		print "- wrong path?"
		print "- localfs should be located /data/images/rhev and be set as 36:36 permission"
		print "- Are you trying to add an existing item?"
		sys.exit(-1)

	print "Done!"

	# To see the response from the server 
	#response = ret.read()
	#print response
