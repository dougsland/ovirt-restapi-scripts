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

	if len(sys.argv) != 6:
		print "Usage: %s my_storage_name type NfsAddress NfsPath MyHost" %(sys.argv[0])
		print "Example: %s my_storage nfs 192.168.1.103 /nfs/dataNFS MyHost" %(sys.argv[0])
		sys.exit(1)

	print "Creating storage %s" %(sys.argv[1])
	print "Type: %s"            %(sys.argv[2])
	print "Address: %s"         %(sys.argv[3])
	print "Path: %s"         %(sys.argv[4])

	#print xml_request

	id_ret = getHostId(sys.argv[5])

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
		<type>nfs</type>
		<address>""" + sys.argv[3] + """</address>
		<path>""" + sys.argv[4] + """</path>
	</storage>
	</storage_domain>
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
		print "- nfs paths are case sensitive (/nfs/Data is diff from /nfs/data)"
		print "- Are you trying to add an existing item?"
		sys.exit(-1)

	print "Done!"

	# To see the response from the server 
	#response = ret.read()
	#print response
