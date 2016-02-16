#!/usr/bin/env python

import libvirt
import sys
import os
import socket
import csv
import argparse

ROOT_PATH = '/root/'


def get_running_vms():
    conn = libvirt.open("qemu:///system")
    if conn is None:
        print 'Failed to open connection to the hypervisor'
        sys.exit(1)
    doms = conn.listDomainsID()
    vms = []
    for domain in doms:
        vms.append(conn.lookupByID(domain))
    return vms


def get_shutdown_vms():
    conn = libvirt.open("qemu:///system")
    if conn is None:
        print 'Failed to open connection to the hypervisor'
        sys.exit(1)

    # shutdown vms
    dom = conn.listDefinedDomains()
    vms = []
    for domain in dom:
        vms.append(conn.lookupByName(domain))

    return vms


def return_dom(name):
    conn = libvirt.open("qemu:///system")
    if conn is None:
        print 'Failed to open connection to the hypervisor'
        sys.exit(1)
    dom = conn.listDefinedDomains()
    for domain in dom:
        if conn.lookupByName(domain).name() == name:

            return conn.lookupByName(domain)


def returnVMObj(vm_obj):

    instance_name = []
    for x in vm_obj:
        dict_var = {"name": x.name(),
                    "state": x.state()[0]}
        instance_name.append(dict_var)
    return instance_name


def filterName(vm_obj):
    filter_dir = []
    vm_obj = [x for x in vm_obj if x is not None]
    for i in vm_obj:
        filter_dir.append((os.path.dirname(i)))

    return filter_dir


def getHostName():
    return socket.gethostname()


def writeToCSV(data_w, filename):
    if os.path.exists(filename) is False:
        try:
            record = open(filename, 'w+')
            writer = csv.writer(record, delimiter=',',
                                quoting=csv.QUOTE_ALL)
            writer.writerow(['name', 'state'])
            writer.writerow([data_w.get('name'), data_w.get('state')])
        except IOError, e:
            print "File Error" % e
            raise SystemExit
    else:
        with open(filename, 'a') as w:
            writer = csv.writer(w, delimiter=',',
                                quoting=csv.QUOTE_ALL)
            writer.writerow([data_w.get('name'), data_w.get('state')])


def op_start(filename):
    if os.path.exists(filename):
        try:
            with open(filename, 'rb') as csvfile:
                vms = csv.reader(csvfile, delimiter=',', quotechar='"')
                for v in vms:
                    vm_start(return_dom(''.join(v[0])), ''.join(v[1]))
        except IOError, e:
            print "File Error" % e
            raise SystemExit
    else:
        print "File does not exists"
        raise SystemExit


def vm_shutdown(vms):
    if vms.get('state') is 1:
        op_shutdown(vms.get('name'), 'shutdown')
    elif vms.get('state') is 3:
        op_shutdown(vms.get('name'), 'destroy')


def op_shutdown(vm_name, operation):
    for doms in get_running_vms():
        if operation == 'shutdown' and vm_name == doms.name():
            doms.shutdown()
        elif operation == 'destroy' and vm_name == doms.name():
            doms.destroy()


def vm_start(vms_name, state):
    if state is '1':
        vms_name.create()
    elif state is '3':
        vms_name.create()
        vms_name.suspend()


def parse_args():

    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument('-a', '--action', nargs='?',
                        choices=['shutdown', 'resume'],
                        required=True, default='n', dest='a',
                        help='Shutdown/Start VM')

    args = parser.parse_args()

    return args


def main():
    filename = ROOT_PATH + getHostName() + ".csv"

    if parse_args().a == 'shutdown':
        data = returnVMObj(get_running_vms())
        for w in data:
            writeToCSV(w, filename)
            vm_shutdown(w)
    elif parse_args().a == 'resume':
        if os.path.exists(filename):
            op_start(filename)
        else:
            print "error file missing"


if __name__ == '__main__':
    main()
