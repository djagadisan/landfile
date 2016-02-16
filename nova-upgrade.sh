#!/bin/bash

export DEBIAN_FRONTEND='noninteractive'
apt-get update
rm /etc/apt/preferences.d/qemu-kvm.pref
rm /etc/apt/sources.list.d/ubuntu-virtualisation.list 
aptitude remove kvm-ipxe
aptitude -y -o Dpkg::Options::=--force-confold install qemu-kvm
aptitude -y -o Dpkg::Options::=--force-confold full-upgrade
dpkg -i /root/mlnx-en-dkms_2.1_all.deb
puppet agent --enable
