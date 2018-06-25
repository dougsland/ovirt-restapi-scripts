#!/usr/bin/python

import urllib2
import base64
import sys
import ssl
from xml.etree import ElementTree

# Example
ADDR = "10.0.0.10"
API_PORT = "443"
USER = "admin@internal"
PASSWD = "T0pS3cr3t!!"

def getSDId(sd_name):

        URL      = "https://" + ADDR + ":" + API_PORT + "/ovirt-engine/api/storagedomains"

        request = urllib2.Request(URL)

        base64string = base64.encodestring('%s:%s' % (USER, PASSWD)).strip()
        request.add_header("Authorization", "Basic %s" % base64string)

	context = ssl._create_unverified_context()

        try:
                xmldata = urllib2.urlopen(request, context=context).read()
        except urllib2.URLError, e:
                print "Error: cannot connect to REST API: %s" % (e)
                print "\tTry to login using the same user/pass by the Admin Portal and check the error!"
                sys.exit(2)

        tree = ElementTree.XML(xmldata)
        list = tree.findall("storage_domain")

        sd_id = None
        for item in list:
                if sd_name == item.find("name").text:
                        sd_id = item.attrib["id"]
                        print "SD ID: %s" % (sd_id)
                        break

        return sd_id

if __name__ == "__main__":

	if len(sys.argv) != 3:
		print "Usage: %s StorageDomain_Name LUN_WWID " %(sys.argv[0])
		print "Example: %s myStorageDomain 35005907f88181c20" %(sys.argv[0])
		sys.exit(1)

	print "Removing LUN: %s from StorageDomain: %s" %(sys.argv[2], sys.argv[1])

	id_ret = getSDId(sys.argv[1])

	if id_ret == None:
		print "Cannot find Storage Domain"
		sys.exit(1)

	xml_request ="""
	<action>
	  <logical_units>
	    <logical_unit id = """ + "'" + sys.argv[2] + "'" + """/>
	  </logical_units>
	</action>
	"""

	print xml_request

	# Setting URL
	URL      = "https://" + ADDR + ":" + API_PORT + "/ovirt-engine/api/storagedomains/" + id_ret + "/reduceluns"

	request = urllib2.Request(URL)
	print "Connecting to: " + URL

	base64string = base64.encodestring('%s:%s' % (USER, PASSWD)).strip()
	request.add_header("Authorization", "Basic %s" % base64string)

	context = ssl._create_unverified_context()

	request.add_header('Accept', 'application/xml')
	request.add_header('Content-Type', 'application/xml')
	request.get_method = lambda: 'POST'
	
	try:
		ret = urllib2.urlopen(request, xml_request, context=context)
	except urllib2.URLError, e:
		print "%s" %(e)
		sys.exit(-1)

	print "Done!"
