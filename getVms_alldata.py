#!/usr/bin/python
#
# Copyright (C) 2011
#
# Author: Douglas Schilling Landgraf <dougsland@redhat.com>
# Contributor: Amador Pahim <amador@pahim.org>
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
 <vm id="163f2a45-e2db-4de0-b76d-3863d3852969" href="/api/vms/163f2a45-e2db-4de0-b76d-3863d3852969">
        <name>vm01</name>
        <description>My first VM</description>
        <actions>
            <link rel="shutdown" href="/api/vms/163f2a45-e2db-4de0-b76d-3863d3852969/shutdown"/>
            <link rel="start" href="/api/vms/163f2a45-e2db-4de0-b76d-3863d3852969/start"/>
            <link rel="stop" href="/api/vms/163f2a45-e2db-4de0-b76d-3863d3852969/stop"/>
            <link rel="suspend" href="/api/vms/163f2a45-e2db-4de0-b76d-3863d3852969/suspend"/>
            <link rel="detach" href="/api/vms/163f2a45-e2db-4de0-b76d-3863d3852969/detach"/>
            <link rel="export" href="/api/vms/163f2a45-e2db-4de0-b76d-3863d3852969/export"/>
            <link rel="move" href="/api/vms/163f2a45-e2db-4de0-b76d-3863d3852969/move"/>
            <link rel="ticket" href="/api/vms/163f2a45-e2db-4de0-b76d-3863d3852969/ticket"/>
            <link rel="migrate" href="/api/vms/163f2a45-e2db-4de0-b76d-3863d3852969/migrate"/>
        </actions>
        <link rel="disks" href="/api/vms/163f2a45-e2db-4de0-b76d-3863d3852969/disks"/>
        <link rel="nics" href="/api/vms/163f2a45-e2db-4de0-b76d-3863d3852969/nics"/>
        <link rel="cdroms" href="/api/vms/163f2a45-e2db-4de0-b76d-3863d3852969/cdroms"/>
        <link rel="snapshots" href="/api/vms/163f2a45-e2db-4de0-b76d-3863d3852969/snapshots"/>
        <link rel="tags" href="/api/vms/163f2a45-e2db-4de0-b76d-3863d3852969/tags"/>
        <link rel="permissions" href="/api/vms/163f2a45-e2db-4de0-b76d-3863d3852969/permissions"/>
        <link rel="statistics" href="/api/vms/163f2a45-e2db-4de0-b76d-3863d3852969/statistics"/>
        <type>server</type>
        <status>
            <state>down</state>
        </status>
        <memory>536870912</memory>
        <cpu>
            <topology cores="3" sockets="2"/>
        </cpu>
        <os type="rhel_6x64">
            <boot dev="hd"/>
            <boot dev="cdrom"/>
            <kernel>/boot/vmlinuz.img</kernel>
            <initrd>/boot/initrd.img</initrd>
            <cmdline>quiet</cmdline>
        </os>
        <high_availability>
            <enabled>true</enabled>
            <priority>50</priority>
        </high_availability>
        <display>
            <type>spice</type>
            <address>0</address>
            <monitors>1</monitors>
        </display>
        <cluster id="2dc22d46-0a0a-11e1-ba0d-0017a4a73a29" href="/api/clusters/2dc22d46-0a0a-11e1-ba0d-0017a4a73a29"/>
        <template id="00000000-0000-0000-0000-000000000000" href="/api/templates/00000000-0000-0000-0000-000000000000"/>
        <start_time>2011-11-22T10:36:46.941Z</start_time>
        <creation_time>2011-11-21T15:33:40.398-02:00</creation_time>
        <origin>rhev</origin>
        <stateless>false</stateless>
        <custom_properties>
            <custom_property value="1:true" name="vhost"/>
            <custom_property value="false" name="sap_agent"/>
        </custom_properties>
        <placement_policy>
            <host id="e0ff8a68-0a0d-11e1-b84b-0017a4a73a29"/>
            <affinity>user_migratable</affinity>
        </placement_policy>
        <memory_policy>
            <guaranteed>357564416</guaranteed>
        </memory_policy>
        <usb>
            <enabled>true</enabled>
        </usb>
    </vm>
"""

# Example
ADDR     = "192.168.123.176"
API_PORT = "8443"
USER     = "rhevm@ad.rhev3.com"
PASSWD   = "T0pSecreT!"

# Setting URL
URL      = "https://" + ADDR + ":" + API_PORT + "/api/vms"

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
list = tree.findall("vm")

#print len(list)

for item in list:
	print "id:  %s"				% (item.attrib["id"])
	print "href:  %s"			% (item.attrib["href"])
	print "name: %s"			% (item.find("name").text)
	print "description: %s"			% (item.find("description").text)

	for subitem in item.findall("actions/link"):
		print "actions: link rel: %s"		% (subitem).attrib["rel"]
		print "actions: link href: %s"		% (subitem).attrib["href"]

	for subitem in item.findall("link"):
		print "link rel: %s"			% (subitem).attrib["rel"]
		print "link href: %s"			% (subitem).attrib["href"]

	print "type: %s"			% (item.find("type").text)
	print "status: %s"			% (item.find("status/state").text)
	print "memory: %s"			% (item.find("memory").text)
	print "cpu topology: %s cores"		% (item.find("cpu/topology").attrib["cores"])
	print "cpu topology: %s sockets"	% (item.find("cpu/topology").attrib["sockets"])
	print "os type: %s "			% (item.find("os").attrib["type"])

	for subitem in item.findall("os/boot"):
		print "os: boot dev: %s"		% (subitem).attrib["dev"]

	print "os kernel: %s "			% (item.find("os/kernel").text)
	print "os initrd: %s "			% (item.find("os/initrd").text)
	print "os cmdline: %s "			% (item.find("os/cmdline").text)
	print "high_availability/enabled: %s "	% (item.find("high_availability/enabled").text)
	print "high_availability/priority: %s "	% (item.find("high_availability/priority").text)
	print "display/type: %s "		% (item.find("display/type").text)

	if item.find("display/address") is not None:
		print "display/address: %s "		% (item.find("display/address").text)

	if item.find("display/port") is not None:
		print "display/port: %s "		% (item.find("display/port").text)

	print "display/monitors: %s "			% (item.find("display/monitors").text)

	if item.find("host") is not None:
		print "host id: %s "			% (item.find("host").attrib["id"])
		print "host href: %s "			% (item.find("host").attrib["href"])

	print "cluster id: %s "			% (item.find("cluster").attrib["id"])
	print "cluster href: %s "		% (item.find("cluster").attrib["href"])
	print "template id: %s "		% (item.find("template").attrib["id"])
	print "template href: %s "		% (item.find("template").attrib["href"])
	print "start time: %s "			% (item.find("start_time").text)
	print "creation time: %s "		% (item.find("creation_time").text)
	print "origin: %s "			% (item.find("origin").text)
	print "stateless: %s "			% (item.find("stateless").text)

	if item.find("custom_properties") is not None:
		for subitem in item.findall("custom_properties/custom_property"):
			print "custom_properties/custom_property value: %s "	% (subitem).attrib["value"]
			print "custom_properties/custom_property name: %s "	% (subitem).attrib["name"]

	if item.find("timezone") is not None:
		print "timezone: %s "			% (item.find("timezone").text)

	if item.find("domain") is not None:
		print "domain name: %s "		% (item.find("domain/name").text)
		
	if item.find("placement_policy/host") is not None:
		print "placement_policy/host id: %s "	% (item.find("placement_policy/host").attrib["id"])

	print "placement_policy/affinity: %s "	% (item.find("placement_policy/affinity").text)
	print "memory_policy/guaranteed: %s "	% (item.find("memory_policy/guaranteed").text)
	print "usb/enabled: %s "		% (item.find("usb/enabled").text)
	print "\n"
