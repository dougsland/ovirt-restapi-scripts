#!/usr/local/bin/python2.7
# encoding: utf-8
'''
this module performs a smoke test procedure of ovirt node / rhevh

@author:     Tolik

@copyright:  2015 Red Hat . All rights reserved.

@license:    GPL

@contact:    tlitovsk@redhat.com
'''

import sys
import os
import datetime
import subprocess
import time

from ovirtsdk.api import API
from ovirtsdk.xml import params


__all__ = []
__version__ = 0.1
__date__ = '2015-02-24'
__updated__ = '2015-03-09'

node_name = "node1"
engine_url = "https://192.168.100.100/api"
password = "12345"
testvm = "centos7"


def approve(api, node_name):

    def wait_for_status(host, state, timeout_in_sec=60):
        if host is None:
            raise TypeError("Host value must have some type")

        start = datetime.datetime.now()

        while True:
            if host.status.state == state:
                return
            if (datetime.datetime.now() - start).seconds < timeout_in_sec:
                break
            host = host.update()

        print ("\033[1m Error: \033[0m timeout waiting for " +
               "%s , current state %s " % (host.status.state, state))

        raise RuntimeError('Cant reach desired state %s' % state)

    start = datetime.datetime.now()

    while api.hosts.get(node_name) is None:
        if (datetime.datetime.now() - start).seconds > 60:
            print "\033[1m Error: \033[0m node not found"
            raise LookupError('Cant find the node %s' % node_name)

    host = api.hosts.get(node_name)
    # validate the status
    wait_for_status(host, 'pending_approval', 0)
    host.approve()
    wait_for_status(host, 'up', 0)

    return host
'''
    def remove(self):
        # maintance
        self.__host.deactivate()
        if WaitForStatus(self.__host, 'maintenance', 0) is False:
            raise RuntimeError

        # and remove
        self.__host.delete()
        # TODO : add check the host was deleted
        # Its not really going tostop us nut worth to test all functionality
'''


def import_vm(api, vm_name):

    export_storage = api.storagedomains.get("export")
    main_storage = api.storagedomains.get("data")
    imported_vm = export_storage.vms.get(vm_name)
    imported_vm.import_vm(params.Action(storage_domain=main_storage,
                                        cluster=api.clusters.get(name="Default")))
    print 'VM was imported successfully'
    print 'Waiting for VM to reach Down status'
    start = datetime.datetime.now()
    while api.vms.get(vm_name).status.state != 'down':
        if (datetime.datetime.now() - start).seconds > 600:
            print "\033[1m Error: \033[0m import fail"
            raise RuntimeError("Cant reach down state in imported VM")
        print api.vms.get(vm_name).status.state
        time.sleep(10)
    return api.vms.get(vm_name)


def create_nfs_storage(api, spm, storage_type):
    # TODO : make a better function with dynamic storage selection
    # for making it simple the type and the name are the same
    storage_formats = {'data': 'V3', 'export': 'V1'}

    storage_params = params.StorageDomain(name=storage_type,
                                          data_center=api.datacenters.get(
                                              "Default"),
                                          storage_format=storage_formats[
                                              storage_type],
                                          type_=storage_type,
                                          host=spm,
                                          storage=params.Storage(type_="NFS",
                                                                 address="192.168.100.100",
                                                                 path='/' + storage_type))
    api.storagedomains.add(storage_params)
    api.datacenters.get(name="Default").storagedomains.add(
        api.storagedomains.get(name=storage_type))


def main(argv=None):

    # setup connection
    engine_api = API(url=engine_url,
                     username="admin@internal",
                     password=password, insecure=True)

    print "Starting smoke testing"
    rhevh = approve(engine_api, node_name)
    print "Host approved"

    create_nfs_storage(engine_api, rhevh, 'data')
    print "Data storage created"

    create_nfs_storage(engine_api, rhevh, 'export')
    print "Export storage created"

    subprocess.check_call(
        ["rhevm-image-uploader",
         "--insecure",
         "-u",
         "admin@internal",
         "-p",
         password,
         "-e",
         "export",
         "upload",
         testvm])

    print "Uploaded VMs"

    test_vm = import_vm(engine_api, testvm)
    print "Vm imported"

    start = datetime.datetime.now()
    test_vm.start()
    while test_vm.status.state != 'up':
        if (datetime.datetime.now() - start).seconds > 600:
            print "\033[1m Error: \033[0m start fail"
            raise RuntimeError("Cant start imported VM")
        time.sleep(5)
        test_vm = test_vm.update()

    print "All success"
    return 0

if __name__ == "__main__":
    sys.exit(main())
