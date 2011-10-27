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

def getClusterId(cluster_name):

        URL      = "https://" + ADDR + ":" + API_PORT + "/api/clusters"

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
        list = tree.findall("cluster")

        cluster_id = None
        for item in list:
                if cluster_name == item.find("name").text:
                        cluster_id = item.attrib["id"]
                        print "cluster id %s" % (cluster_id)
                        break

        return cluster_id


if __name__ == "__main__":

	if len(sys.argv) != 5:
		print "Usage: %s my_hostname address password cluster" %(sys.argv[0])
		print "Example: %s myhost 192.168.1.54 T0pSecreT! MyCluster" %(sys.argv[0])
		sys.exit(1)

	print "Creating host %s" %(sys.argv[1])
	print "Address: %s"      %(sys.argv[2])


	#print xml_request

	id_ret = getClusterId(sys.argv[4])

        if id_ret == None:
                print "Cannot find Cluster"
                sys.exit(1)

	# Setting URL
	URL      = "https://" + ADDR + ":" + API_PORT + "/api/hosts"

	xml_request ="""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<host>
	  <name>""" + sys.argv[1] + """</name>
	  <address>""" + sys.argv[2] + """</address>
	  <root_password>""" + sys.argv[3] + """</root_password>
	  <cluster id="""+"\""+ """"""+id_ret+""""""+ "\""+"""/>
	</host>
	"""

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

	# To see the response from the server 
	#response = ret.read()
	#print response
