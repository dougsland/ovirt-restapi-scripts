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
EXAMPLE XML output
========================
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<hosts>
    <host id="beaea688-cd59-11e0-a86f-5254006cd06b" href="/api/hosts/beaea688-cd59-11e0-a86f-5254006cd06b">
        <name>192.168.1.54</name>
        <actions>
            <link rel="install" href="/api/hosts/beaea688-cd59-11e0-a86f-5254006cd06b/install"/>
            <link rel="activate" href="/api/hosts/beaea688-cd59-11e0-a86f-5254006cd06b/activate"/>
            <link rel="fence" href="/api/hosts/beaea688-cd59-11e0-a86f-5254006cd06b/fence"/>
            <link rel="deactivate" href="/api/hosts/beaea688-cd59-11e0-a86f-5254006cd06b/deactivate"/>
            <link rel="approve" href="/api/hosts/beaea688-cd59-11e0-a86f-5254006cd06b/approve"/>
            <link rel="iscsilogin" href="/api/hosts/beaea688-cd59-11e0-a86f-5254006cd06b/iscsilogin"/>
            <link rel="iscsidiscover" href="/api/hosts/beaea688-cd59-11e0-a86f-5254006cd06b/iscsidiscover"/>
            <link rel="commitnetconfig" href="/api/hosts/beaea688-cd59-11e0-a86f-5254006cd06b/commitnetconfig"/>
        </actions>
        <link rel="storage" href="/api/hosts/beaea688-cd59-11e0-a86f-5254006cd06b/storage"/>
        <link rel="nics" href="/api/hosts/beaea688-cd59-11e0-a86f-5254006cd06b/nics"/>
        <link rel="tags" href="/api/hosts/beaea688-cd59-11e0-a86f-5254006cd06b/tags"/>
        <link rel="permissions" href="/api/hosts/beaea688-cd59-11e0-a86f-5254006cd06b/permissions"/>
        <link rel="statistics" href="/api/hosts/beaea688-cd59-11e0-a86f-5254006cd06b/statistics"/>
        <address>192.168.1.54</address>
        <status>
            <state>non_responsive</state>
        </status>
        <cluster id="99408929-82cf-4dc7-a532-9d998063fa95" href="/api/clusters/99408929-82cf-4dc7-a532-9d998063fa95"/>
        <port>54321</port>
        <storage_manager>false</storage_manager>
        <power_management>
            <enabled>false</enabled>
            <options/>
        </power_management>
        <ksm>
            <enabled>true</enabled>
        </ksm>
        <transparent_hugepages>
            <enabled>true</enabled>
        </transparent_hugepages>
        <iscsi>
            <initiator>iqn.1994-05.com.redhat:3ece8aa1d7f1</initiator>
        </iscsi>
        <cpu>
            <topology cores="2"/>
            <name>Intel(R) Pentium(R) D CPU 3.00GHz</name>
            <speed>3000</speed>
        </cpu>
        <summary>
            <active>0</active>
            <migrating>0</migrating>
            <total>0</total>
        </summary>
    </host>
</hosts>
"""

# Example
ADDR     = "192.168.123.176"
API_PORT = "8443"
USER     = "rhevm@ad.rhev3.com"
PASSWD   = "T0pSecreT!"

# Setting URL
URL      = "https://" + ADDR + ":" + API_PORT + "/api/hosts"

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
list = tree.findall("host")

#print len(list)

for item in list:
	print "id:  %s"           % (item.attrib["id"])
	print "href:  %s"         % (item.attrib["href"])
	print "name: %s"          % (item.find("name").text)

	for subitem in item.findall("actions/link"):
		print "actions: link rel: %s"   % (subitem).attrib["rel"]#.find("rel"))
		print "actions: link href: %s"  % (subitem).attrib["href"]#.find("rel"))

	for subitem in item.findall("link"):
		print "link rel: %s"   % (subitem).attrib["rel"]
		print "link href: %s"  % (subitem).attrib["href"]

	print "address: %s"                   % (item.find("address").text)
	print "status: %s"                    % (item.find("status/state").text)
	print "cluster id: %s"                % (item.find("cluster").attrib["id"])
	print "cluster href: %s"              % (item.find("cluster").attrib["href"])
	print "port: %s"  		      % (item.find("port").text)
	print "storage_manager: %s"  	      % (item.find("storage_manager").text)
	print "power_management/enabled: %s"  % (item.find("power_management/enabled").text)
	print "ksm: %s"  		      % (item.find("ksm/enabled").text)
	print "transparent_hugepages: %s"     % (item.find("transparent_hugepages/enabled").text)
	print "iscsi -> initiator: %s"        % (item.find("iscsi/initiator").text)
	print "cpu -> name: %s"  	      % (item.find("cpu/name").text)
	print "cpu -> speed: %s"  	      % (item.find("cpu/speed").text)
	print "cpu -> topology -> cores: %s"  % (item.find("cpu/topology").attrib["cores"])
	print "summary -> active: %s"         % (item.find("summary/active").text)
	print "summary -> migrating: %s"      % (item.find("summary/migrating").text)
	print "summary -> total: %s"          % (item.find("summary/total").text)
	print "\n"
