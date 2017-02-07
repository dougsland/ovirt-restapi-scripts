#!/usr/bin/python
#
# Copyright (C) 2011-2017
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
import ssl
from xml.etree import ElementTree

# Example
ADDR = "10.0.0.10"
API_PORT = "443"
USER = "admin@internal"
PASSWD = "T0pS3cr3t!!"


def getHostId(host_name):

        URL = "https://" + ADDR + ":" + API_PORT + "/ovirt-engine/api/hosts"

        request = urllib2.Request(URL)

        base64string = base64.encodestring('%s:%s' % (USER, PASSWD)).strip()
        request.add_header("Authorization", "Basic %s" % base64string)

        context = ssl._create_unverified_context()
        try:
                xmldata = urllib2.urlopen(request, context=context).read()
        except urllib2.URLError, e:
                print("Error: cannot connect to REST API: %s" % (e))
                print("\tTry to login using the same user/pass by the "
                      "Admin Portal and check the error!")
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

    if len(sys.argv) != 2:
        print("Usage: %s my_host_name" % (sys.argv[0]))
        print("Example: %s 192.168.1.60" % (sys.argv[0]))
        sys.exit(1)

    print("Approving host: %s" % (sys.argv[1]))

    id_ret = getHostId(sys.argv[1])

    if id_ret is None:
        print("Cannot find Host")
        sys.exit(1)

    xml_request = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <action/>
        """

    # Setting URL
    URL = "https://" + ADDR + ":" + API_PORT + "/ovirt-engine" + \
          "/api/hosts/" + id_ret + "/upgrade"

    request = urllib2.Request(URL)
    print("Connecting to: " + URL)

    base64string = base64.encodestring('%s:%s' % (USER, PASSWD)).strip()
    request.add_header("Authorization", "Basic %s" % base64string)
    request.add_header('Content-Type', 'application/xml')
    context = ssl._create_unverified_context()

    try:
        ret = urllib2.urlopen(request, xml_request, context=context)
    except urllib2.URLError, e:
        print("%s" % (e))
        print("Are you trying to add an existing item?")
        raise

    print("Done!")

# To see the response from the server
# response = ret.read()
# print response
