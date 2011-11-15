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

def getVMId(vm_name):

        URL      = "https://" + ADDR + ":" + API_PORT + "/api/vms"

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
        list = tree.findall("vm")

        vm_id = None
        for item in list:
                if vm_name == item.find("name").text:
                        vm_id = item.attrib["id"]
                        print "vm id %s" % (vm_id)
                        break

        return vm_id

def getStorageId(st_name):

        URL      = "https://" + ADDR + ":" + API_PORT + "/api/storagedomains"

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
        list = tree.findall("storage_domain")

        st_id = None
        for item in list:
                if st_name == item.find("name").text:
                        st_id = item.attrib["id"]
                        print "st id %s" % (st_id)
                        break

        return st_id

if __name__ == "__main__":

	#print len(sys.argv)
	if len(sys.argv) != 9:
		print "Usage: %s vm_name StorageName size_in_bytes disk_type (system/data) disk_type (virtio/ide) disk_format (cow/raw) bootable (true/false) wipe_after_delete (true/false)" %(sys.argv[0])
		print "Example (1): %s myVirtualMachine iscsiData150g 8589934592 system virtio cow true false" %(sys.argv[0])
		print "Example (2): %s myVirtualMachine iscsiData150g 8589934592 data virtio raw false false" %(sys.argv[0])
		print "Note: 8589934592 = 8G"
		sys.exit(1)

	print "creating storage to vm: %s" %(sys.argv[1])

	id_vm = getVMId(sys.argv[1])

	if id_vm == None:
		print "Cannot find virtual machine"
		sys.exit(1)

	id_st = getStorageId(sys.argv[2])

	if id_st == None:
		print "Cannot find storage id"
		sys.exit(1)

	if sys.argv[6] == "raw":
		xml_request ="""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
		<disk>
			<storage_domains>
				<storage_domain id="""+"\""+ """""" + id_st + """"""+ "\""+"""/>
			</storage_domains>    
			<size>""" + sys.argv[3] + """</size>
			<type>""" + sys.argv[4] + """</type>
			<interface>""" + sys.argv[5] + """</interface>
			<format>""" + sys.argv[6] + """</format>
			<sparse>false</sparse>
			<bootable>""" + sys.argv[7] + """</bootable>
			<wipe_after_delete>""" + sys.argv[8] + """</wipe_after_delete>
		 </disk>
		"""
	else:
		xml_request ="""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
		<disk>
			<storage_domains>
				<storage_domain id="""+"\""+ """""" + id_st + """"""+ "\""+"""/>
			</storage_domains>    
			<size>""" + sys.argv[3] + """</size>
			<type>""" + sys.argv[4] + """</type>
			<interface>""" + sys.argv[5] + """</interface>
			<format>""" + sys.argv[6] + """</format>
			<sparse>true</sparse>
			<bootable>""" + sys.argv[7] + """</bootable>
			<wipe_after_delete>""" + sys.argv[8] + """</wipe_after_delete>
		 </disk>
		"""


	#print xml_request

	# Setting URL
	URL      = "https://" + ADDR + ":" + API_PORT + "/api/vms/" + id_vm + "/disks"

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
