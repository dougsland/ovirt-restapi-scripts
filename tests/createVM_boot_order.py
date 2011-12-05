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

if len(sys.argv) <= 3:
	print "Usage: %s cluster_name vm_NAME memory (in bytes) template (if you have one, otherwise it will be Blank)" %(sys.argv[0])
	print "Example: %s cluster_ISCSI myNEW_VM 536870912" %(sys.argv[0])
	print "Note:"
	print "536870912 (bytes) = (512MB) "
	sys.exit(1)

print "Creating vm %s" %(sys.argv[2])

if len(sys.argv) < 5: 
	xml_request ="""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<vm>
	  <name>""" + sys.argv[2] + """</name>
	  <cluster>
	    <name>""" + sys.argv[1] + """</name>
	  </cluster>
	  <template>
	    <name>Blank</name>
	  </template>
	  <memory>""" + sys.argv[3] + """</memory> 
	  <os>
	     <boot dev="network"/> 
	     <boot dev="hd"/> 
	     <kernel/>
	     <initrd/>
             <cmdline/>
	  </os>
        </vm>
	"""
# All boot options
#	  <os>
#	     <boot dev="hd"/> 
#	     <boot dev="cdrom"/> 
#	     <boot dev="network"/> 
#	  </os>
else:
	xml_request ="""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<vm>
	  <name>""" + sys.argv[2] + """</name>
	  <cluster>
	    <name>""" + sys.argv[1] + """</name>
	  </cluster>
	  <template>
	    <name>""" + sys.argv[4] + """</name>
	  </template>
	  <memory>""" + sys.argv[3] + """</memory> 
	  <os>
	    <boot dev="network"/> 
	    <boot dev="hd"/> 
	    <kernel/>
	    <initrd/>
            <cmdline/>
	  </os>
	</vm>
	"""
# All boot options
#	  <os>
#	     <boot dev="hd"/> 
#	     <boot dev="cdrom"/> 
#	     <boot dev="network"/> 
#	  </os>

#print xml_request

# Example
ADDR     = "192.168.123.176"
API_PORT = "8443"
USER     = "rhevm@ad.rhev3.com"
PASSWD   = "T0pSecreT!"

# Setting URL
URL      = "https://" + ADDR + ":" + API_PORT + "/api/vms"


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
