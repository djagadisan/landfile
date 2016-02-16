#!/bin/bash

if [ "$1" == "" ] ; then
    echo "usage: ./$0 node-to-evacuate"
    echo "e.g. ./$0 np-rcc5"
    exit 1
fi

ssh $1 nova-manage service disable --service=nova-compute --host=$1
ssh $1 nova-manage service disable --service=nova-network --host=$1

#dom_ids=`ssh $1 "virsh list | tail -n +3 | head -n -1" | awk '{print $1}'`
dom_ids=`nova list --all-tenants --host=np-rcc7$ --fields=id  | sed -e "s/|//g" | tail -n +4 | head -n -1 | awk '{print $1}'`
for id in $dom_ids ; do
    uuid=`ssh $1 virsh dumpxml $id | grep uuid | grep -v entry | sed -e "s/ *<uuid>\(.*\)<\/uuid>.*/\1/g"`
    cmd="nova live-migration $uuid"
    echo $cmd
    eval $cmd
done

echo "Ensure that all vms migrated successfully, install updates etc:"
echo ssh $1 apt-get update
echo ssh $1 aptitude -y full-upgrade
echo ssh $1 dpkg -i mlnx-en-dkms_2.0_all.deb

echo "Ensure that all vms migrated successfully, install updates,"
echo "then reboot, and change the following settings in BIOS:"
echo "HPC Mode => Enabled"
echo "OnChip SATA Type => AMD_AHCI"
echo "Fan Speed => Full Speed"
echo "ACPI APIC Support => enabled"

echo ssh $1 apt-get update
echo ssh $1 aptitude -y full-upgrade
echo ssh $1 nova-manage service enable --service=nova-compute --host=$1
echo ssh $1 nova-manage service enable --service=nova-network --host=$1
