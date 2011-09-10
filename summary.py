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
import getopt

from xml.dom.minidom import parse, parseString

def show_summary(optName):

	# Reading XML
	for node in dom.getElementsByTagName(optName):
		for i in range(len(node.childNodes)):
			if node.childNodes[i].nodeName != "#text":
				print "%s: %s %s" % (optName, node.childNodes[i].nodeName,
					node.childNodes[i].firstChild.nodeValue)

def usage():
	print "Usage: %s [options] arg\n" % (sys.argv[0])

	print "Options:\n"
	print "\t-h, --help               \t Show this help message and exit"
	print "\t-i IP, --ip=IP           \t IP address or host of RHEV-M"
	print "\t-u USER, --user=USER     \t User to login, include @domain. Ex: rhevm@ad.rhev3.com"
	print "\t-p PASSWD, --passw=PASSWD\t Password"

	print "\nExample"
	print "\t%s -i 192.168.123.176 -u rhevm@ad.rhev3.com -p T0pSecreT!" % (sys.argv[0])

if __name__ == "__main__":

	ADDR     = ""
	USER     = ""
	PASSWD   = ""
	API_PORT = "8443"

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:u:p:", ["help", "user", "passwd"])
	except getopt.error, msg:
		print msg
		print "for help use --help"
		sys.exit(2)

	# Checking number of arguments	
	if len(opts) < 3:
		print "please check the number of arguments required"
		usage()
		sys.exit()

	# process options
	for o, argument in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit(0)

		if o in ("-i", "--ip"):
			ADDR = argument

		if o in ("-u", "--user"):
			USER = argument

		if o in ("-p", "--passwd"):
			PASSWD = argument

	# process arguments
	for arg in args:
		process(arg) # process() is defined elsewhere

	# Let's start doing a connect
	request = urllib2.Request("https://" + ADDR + ":" + API_PORT + "/api")
	print "Connecting to: " + "https://" + ADDR + ":" + API_PORT + "/api"

	base64string = base64.encodestring('%s:%s' % (USER, PASSWD)).strip()
	request.add_header("Authorization", "Basic %s" % base64string)   

	try:
		file = urllib2.urlopen(request)
	except urllib2.URLError, e:
		print "Error: cannot connect to REST API: %s" % (e)
		sys.exit(2)
	
	data = file.read()
	file.close()
	
	#DEBUG - show the whole XML tree
	#print data

	dom = parseString(data)

	show_summary("hosts")
	show_summary("users")
	show_summary("vms")
	show_summary("storage_domains")
