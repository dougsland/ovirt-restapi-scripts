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

import unittest
import base64
import urllib2
import sys
from xml.etree import ElementTree

ADDR        = "192.168.123.176"
API_PORT    = "8443"
USER        = "rhevm@ad.rhev3.com"
PASSWD      = "T0pSecreT!"

DCNAME      = "unitTestDC"
CLUSTERNAME = "unitTestCluster"

totalTests = 0

class TestURLs(unittest.TestCase):


	def test_run(self):

		global totalTests

		print "================================================"
		print "Searching all URLs"
		print "================================================"
		resource = ["capabilities", "clusters", "datacenters",
			    "events", "hosts", "networks", "roles", "storagedomains",
			    "tags", "templates", "users", "groups", "domains", "vmpools", "vms" ] 

		for val in resource:
			# Setting URL
			URL      = "https://" + ADDR + ":" + API_PORT + "/api/" + val

			request = urllib2.Request(URL)
			print "Connecting to: " + URL

			base64string = base64.encodestring('%s:%s' % (USER, PASSWD)).strip()
			request.add_header("Authorization", "Basic %s" % base64string)

			try:
				xmldata = urllib2.urlopen(request).read()
			except urllib2.URLError, e:
				print "Error: cannot connect to REST API: %s" % (e)
				print "Try to login using the same user/pass by the Admin Portal and check the error!"
				assert()

		totalTests += 1
			
		print "TestURLs [OK]"

class AddElements(unittest.TestCase):


	def test_addDataCenter(self):

		global totalTests

		print "================================================"
		print "Adding DataCenter: %s" %(DCNAME)
		print "================================================"

		xml_request ="""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
		<data_center>
			<name>""" + DCNAME + """</name>
			<storage_type>nfs</storage_type>
			<version minor=\"0\" major=\"3\"/>
		</data_center>
		"""

		# Setting URL
		URL      = "https://" + ADDR + ":" + API_PORT + "/api/datacenters"

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
			assert()

		totalTests += 1
		print "test_addDataCenter [OK]"

	def test_addClusters(self):

		global totalTests
		print "================================================"
		print "Adding Cluster: %s" %(DCNAME)
		print "================================================"
		totalTests += 1
	
class SearchElements(unittest.TestCase):
  

	def test_searchDataCenter(self):

		global totalTests

		print "================================================"
		print "Starting test_searchDataCenter..."
		print "================================================"

		# Setting URL
		URL      = "https://" + ADDR + ":" + API_PORT + "/api/datacenters?search=" + DCNAME

		request = urllib2.Request(URL)
		print "Connecting to: " + URL

		base64string = base64.encodestring('%s:%s' % (USER, PASSWD)).strip()
		request.add_header("Authorization", "Basic %s" % base64string)
		request.add_header('Content-Type', 'application/xml')

		try:
			xmldata = urllib2.urlopen(request).read()
		except urllib2.URLError, e:
			print "%s" %(e)
			print "Are you trying to add an existing item?"
			assert()

		tree = ElementTree.XML(xmldata)
		lst = tree.findall("data_center/name")

		# if len is 0, no valid return
		if len(lst) == 0:
			assert()

		print "test_searchDataCenter [OK]"

		totalTests += 1

class Aux:

	def _getDataCenterId(self, dc_name):
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

class RemoveElements(unittest.TestCase):


	def test_removeDataCenter(self):
		global totalTests

		print "================================================"
		print "Starting test_removeDataCenter (%s)" %(DCNAME)
		print "================================================"
		aux = Aux()
		retId = aux._getDataCenterId(DCNAME)

		# Setting URL
		URL      = "https://" + ADDR + ":" + API_PORT + "/api/datacenters/" + str(retId)

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

		print "test_removeDataCenter [OK]"
		totalTests += 1
			
if __name__ == '__main__':

	# Test 1 - search all URLs
	suite = unittest.TestLoader().loadTestsFromTestCase(TestURLs)
	unittest.TextTestRunner(verbosity=0).run(suite)

	# Test 2 - Add new Elements
	suite = unittest.TestLoader().loadTestsFromTestCase(AddElements)
	unittest.TextTestRunner(verbosity=0).run(suite)

	# Test 3 - Search Elementes Added before
	suite = unittest.TestLoader().loadTestsFromTestCase(SearchElements)
	unittest.TextTestRunner(verbosity=0).run(suite)

	# Test 4 - Remove Elements
	suite = unittest.TestLoader().loadTestsFromTestCase(RemoveElements)
	unittest.TextTestRunner(verbosity=0).run(suite)

	print "Total tests executed: %s" % (totalTests)
