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

"""
<storage_domain id="becd522f-329e-48d5-9555-00cc893c2b01" href="/api/storagedomains/becd522f-329e-48d5-9555-00cc893c2b01">
	<name>asda</name>
	<link rel="permissions" href="/api/storagedomains/becd522f-329e-48d5-9555-00cc893c2b01/permissions"/>
	<type>data</type>
	<master>true</master>
	<storage>
		<type>iscsi</type>
		<volume_group id="lotUmR-j822-iiqB-CK0n-kuC9-1PjQ-0OHfK6">
			<logical_unit id="35000144f72387710">
				<address>192.168.1.103</address>
				<port>3260</port>
				<target>iqn.1992-04.com.emc:storage.storage.iscsidata</target>
				<username/>
				<serial>SEMC_LIFELINE-DISK_EMCDSK-723877-10</serial>
				<vendor_id>EMC</vendor_id>
				<product_id>LIFELINE-DISK</product_id>
				<lun_mapping>0</lun_mapping>
				<portal>192.168.1.103:3260,1</portal>
				<size>32212254720</size>
				<paths>0</paths>
				</logical_unit>
		</volume_group>
	</storage>
	<available>26843545600</available>
	<used>4294967296</used>
	<committed>0</committed>
	<storage_format>v2</storage_format>
</storage_domain>
"""

# Example
ADDR     = "192.168.123.176"
API_PORT = "8443"
USER     = "rhevm@ad.rhev3.com"
PASSWD   = "T0pSecreT!"

# Setting URL
URL      = "https://" + ADDR + ":" + API_PORT + "/api/storagedomains"

request = urllib2.Request(URL)
print "Connecting to: %s\n" % (URL)

base64string = base64.encodestring('%s:%s' % (USER, PASSWD)).strip()
request.add_header("Authorization", "Basic %s" % base64string)

try:
        xmldata = urllib2.urlopen(request).read()
except urllib2.URLError, e:
        print "Error: cannot connect to REST API: %s" % (e)
        print "Try to login using the same user/pass by the Admin Portal and check the error!"
        sys.exit(2)

#print xmldata 

tree = ElementTree.XML(xmldata)
list = tree.findall("storage_domain")

#print len(list)

for item in list:
	print "storage domain"
	print "=================="
	print "id:  %s"           % (item.attrib["id"])
	print "name: %s"          % (item.find("name").text)

	for subitem in item.findall("link"):
		print "link rel: %s"    % (subitem).attrib["rel"]
		print "link href: %s"   % (subitem).attrib["href"]

	print "type: %s"            % (item.find("type").text)
	print "master: %s"          % (item.find("master").text)

	print "\nstorage"
	print "=================="
	print "\ttype: %s" 	    	% (item.find("storage/type").text)

	if (item.find("storage/type").text) == "nfs":
		print "\taddress: %s"            % (item.find("storage/address").text)
		print "\tpath: %s"            % (item.find("storage/path").text)

	elif (item.find("storage/type").text) == "localfs":
		print "localfs"

	else:
		if item.find("storage/volume_group") != None:
			print "\tvolume_group id: %s"   % (item.find("storage/volume_group").attrib["id"])
		else:
			print "\tvolume_group id: "

		print "\tlogical_unit: %s"   % (item.find("storage/volume_group/logical_unit").attrib["id"])
		print "\taddress: %s"   % (item.find("storage/volume_group/logical_unit/address").text)
		print "\tport: %s"   % (item.find("storage/volume_group/logical_unit/port").text)
		print "\ttarget: %s"   % (item.find("storage/volume_group/logical_unit/target").text)

		print "\tusername: %s"   % (item.find("storage/volume_group/logical_unit/username").text)

		if (item.find("storage/volume_group/logical_unit/password")) != None:
			print "\tpassword: %s"   % (item.find("storage/volume_group/logical_unit/password").text)
		else:
			print "\tpassword: "

		print "\tserial: %s"   % (item.find("storage/volume_group/logical_unit/serial").text)
		print "\tvendor_id: %s"   % (item.find("storage/volume_group/logical_unit/vendor_id").text)
		print "\tproduct_id: %s"   % (item.find("storage/volume_group/logical_unit/product_id").text)
		print "\tlun_mapping: %s"   % (item.find("storage/volume_group/logical_unit/lun_mapping").text)
		print "\tportal: %s"   % (item.find("storage/volume_group/logical_unit/portal").text)
		print "\tsize: %s"   % (item.find("storage/volume_group/logical_unit/size").text)
		print "\tpaths: %s"   % (item.find("storage/volume_group/logical_unit/paths").text)

	print "\navailable: %s"     	% (item.find("available").text)
	print "used: %s" 	    	% (item.find("used").text)
	print "committed: %s" 	    	% (item.find("committed").text)
	print "storage_format: %s"     	% (item.find("storage_format").text)

	print "\n"

