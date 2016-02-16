#-*- coding: utf-8 -*-
import os
import sys
import random
import string
import unicodedata
import time
import util
import re
import novaaction
from write_to_csv import WriteCSV 
from util import GetConfig
from novaaction import NovaAction
from novaclient.v1_1 import client
from novaclient.exceptions import *
from config_data import GetVar
from util import GetConfig
import datetime
from random import randint
import locale
import collections



class TESTNOVA():
    
    def createConnection(self,_user,_key,_project_id,_auth_url):
        try:
            conn = client.Client(username=_user,api_key=_key,project_id=_project_id,auth_url=_auth_url)
            
        except Exception,e:
            return "Error %s" % e 
    
        return conn  

__init__='main'
encoding = (locale.getpreferredencoding() or sys.stdin.encoding or 'UTF-8')

def get_Resources(cell,client):
    total_avail=0
    total_used=0
    total_avail_mem=0
    total_used_mem=0


    for i in cell:
        total_avail+=int(client.hosts.get(i)[0]._info['resource'].get('cpu'))
        total_used+=int(client.hosts.get(i)[1]._info['resource'].get('cpu'))
        total_avail_mem+=int(client.hosts.get(i)[0]._info['resource'].get('memory_mb'))
        total_used_mem+=int(client.hosts.get(i)[1]._info['resource'].get('memory_mb'))
        
    resources = {'avail_cpu':total_avail,'avail_mem':total_avail_mem,
                    'used_cpu':total_used,'used_mem':total_used_mem}
        
    return resources

def stats_count(_data):
    fc=_data.get('avail_cpu')
    fm=(_data.get('avail_mem')/1024)
    uc=_data.get('used_cpu')
    um=(_data.get('used_mem')/1024)
    ac=fc-uc
    am=fm-um
    
    resources={'nac':fc,'nam':fm,'nuc':uc,'num':um,'nfc':ac,'nfm':am}
    return resources
    
def vm_AllTypeCount(instan_obj):
    
    count_all=[]
    for i in instan_obj:
        if isinstance(i.__dict__.get('OS-EXT-SRV-ATTR:host'),unicode):
            count_all.append(i.flavor.get('id'))
                
    return count_all

def _returnServers(client,cell):
    count_all=[]
    args_a={'all_tenants':1,'host':cell}
    instances=client.servers.list(search_opts=args_a)
    for i in instances:
        if isinstance(i.__dict__.get('OS-EXT-SRV-ATTR:host'),unicode):
            count_all.append(i.flavor.get('id'))
    
    return count_all            
   
def total_flavor_cell(flavour_list):
    m1_small=m1_medium=m1_large=m1_xlarge=m1_xxlarge=0
    for i in flavour_list:
        if i==unicode(0):
            m1_small+=1
        if i==unicode(1):
            m1_medium+=1
        if i==unicode(4):
            m1_large+=1
        if i==unicode(2):
            m1_xlarge+=1
        if i==unicode(3):
            m1_xxlarge+=1
            
    comb_resources = {'m1s':m1_small,'m1m':m1_medium,'m1l':m1_large,'m1xl':m1_xlarge,'m1xxl':m1_xxlarge}
    return comb_resources

def total_flavour_count(count_t):
    sum = collections.Counter()
    for k in count_t:
        sum.update(k)
        
    return sum
    
        
                        
    
    
        
        
    
config = GetVar('production')
nov=NovaAction()
info = GetConfig() 
client= nov.createNovaConnection(config)

print client

server_name='Ubuntu 12.04.2 â€” COMSOL Box'
dic = {'name': server_name }
print dic.get('name')



'''

zone='nova'
service='compute'
host=[]

cell='qh2-*'
qh2_servers=(_returnServers(client,cell))
print len(vm_AllTypeCount(qh2_servers))
cell='np-*'
np_servers=(_returnServers(client,cell))
print len(vm_AllTypeCount(np_servers))
cell='rccomdc-*'
monash_servers=(_returnServers(client,cell))
print len(vm_AllTypeCount(monash_servers))

cell='cn-*'
qld_cur_run_types=total_flavor_cell(_returnServers(client,cell))
print "QLD"
print "M1.small %d" %qld_cur_run_types.get('m1s')
print "M1.medium %d" %qld_cur_run_types.get('m1m')
print "M1.large %d" %qld_cur_run_types.get('m1l')
print "M1.xlarge %d" %qld_cur_run_types.get('m1xl')
print "M1.xxlarge %r" %qld_cur_run_types.get('m1xxl')

cell='qh2-*'
qh2_cur_run_types=total_flavor_cell(_returnServers(client,cell))

print "\n"
print "QH2"
print "M1.small %d" %qh2_cur_run_types.get('m1s')
print "M1.medium %d" %qh2_cur_run_types.get('m1m')
print "M1.large %d" %qh2_cur_run_types.get('m1l')
print "M1.xlarge %d" %qh2_cur_run_types.get('m1xl')
print "M1.xxlarge %r" %qh2_cur_run_types.get('m1xxl')


cell='np-*'
np_cur_run_types=total_flavor_cell(_returnServers(client,cell))
print "\n"
print "NP"
print "M1.small %d" %np_cur_run_types.get('m1s')
print "M1.medium %d" %np_cur_run_types.get('m1m')
print "M1.large %d" %np_cur_run_types.get('m1l')
print "M1.xlarge %d" %np_cur_run_types.get('m1xl')
print "M1.xxlarge %r" %np_cur_run_types.get('m1xxl')
print "\n"

cell='rccomdc-*'
mon_cur_run_types=total_flavor_cell(_returnServers(client,cell))
print "Monash"
print "M1.small %d" %mon_cur_run_types.get('m1s')
print "M1.medium %d" %mon_cur_run_types.get('m1m')
print "M1.large %d" %mon_cur_run_types.get('m1l')
print "M1.xlarge %d" %mon_cur_run_types.get('m1xl')
print "M1.xxlarge %r" %mon_cur_run_types.get('m1xxl')

total_s =[qld_cur_run_types,qh2_cur_run_types,np_cur_run_types,mon_cur_run_types]

print "\n"
print "Total"
print "M1.small: %s" % total_flavour_count(total_s)['m1s']
print "M1.medium: %s" % total_flavour_count(total_s)['m1m'] 
print "M1.large: %s" % total_flavour_count(total_s)['m1l'] 
print "M1.xlarge: %s" % total_flavour_count(total_s)['m1xl']
print "M1.xxlarge: %s" % total_flavour_count(total_s)['m1xxl']  
print "\n"





#instances=client.servers.list(search_opts=args_a)

print len(vm_AllTypeCount(instances,'cn'))
print "VM sizes in use(s, m, l, xl, xxl):%s, %s, %s, %s, %s"%()
print len(vm_AllTypeCount(instances,'np'))
print len(vm_AllTypeCount(instances,'rccomdc'))
'''
#qld_inst=re.compile(r'^qh-rcc')
#
#for i in instances:
#    qld_flavour.append(i.id)
    #if isinstance(i.__dict__.get('OS-EXT-SRV-ATTR:host'),unicode):
        #print type(i.__dict__.get('OS-EXT-SRV-ATTR:host')),i.__dict__.get('OS-EXT-SRV-ATTR:host')
    #   qld_flavour.append(i.status)
        
        #if qld_inst.search(i.__dict__.get('OS-EXT-SRV-ATTR:host').encode(encoding)):
        #    qld_flavour.append(i.flavor.get('id'))
        #    print i.__dict__.get('OS-EXT-SRV-ATTR:host')
   

#print len(qld_flavour)        
'''
    #print i.id,i.flavor.get('id'),


#for k in qld_flavour:
#    print k
    


#

for i in client.hosts.list_all(zone):
#    print i.__dict__
     print i.host_name


np=re.compile(r'nectar!melbourne!np@np')
qh2=re.compile(r'nectar!melbourne!qh2@qh2')
monash=re.compile(r'nectar!monash!monash-')
qld=re.compile(r'nectar!qld@')
np_host,qh2_host,monash_01_host,qld_host = ([] for i in range(4))


for i in client.hosts.list_all(zone):
    if np.search(i.host_name):
        np_host.append(i.host_name)
    elif qh2.search(i.host_name):
        qh2_host.append(i.host_name)
    elif monash.search(i.host_name):
        monash_01_host.append(i.host_name)
    elif qld.search(i.host_name):
        qld_host.append(i.host_name)
        

np_node_count=len(np_host)
qh2_node_count=len(qh2_host)
monash_node_count=len(monash_01_host)
qld_node_count=len(qld_host)

print "total %r" %(len(np_host)+len(qh2_host)+len(monash_01_host)+len(qld_host))    
    #if i.service == unicode(service):
        
    #    host.append(i.host_name)
        #print i.host_name


np_data=get_Resources(np_host, client)
np_stats=stats_count(np_data)
qh2_data=get_Resources(qh2_host, client)
qh2_stats=stats_count(np_data)
monash_data=get_Resources(monash_01_host, client)
monash_stats=stats_count(monash_data)
qld_data=get_Resources(qld_host, client)
qld_stats=stats_count(qld_data)


print "NeCTAR Research Cloud Usage Report"
print "\n"
print "Melbourne Node, Noble Park Cell"
print "Total available nodes, cores and memory: %s nodes, %s cores, %d GB"%(np_node_count,np_stats.get('nac'),np_stats.get('nam'))
print "Used cores and memory: %s cores, %s GB"%(np_stats.get('nuc'),np_stats.get('num'))
print "Free cores and memory: %s cores, %s GB"%(np_stats.get('nfc'),np_stats.get('nfm'))
print "VM sizes in use(s, m, l, xl, xxl):%s, %s, %s, %s, %s"%(np_cur_run_types.get('m1s'),
                                                              np_cur_run_types.get('m1m'),
                                                              np_cur_run_types.get('m1l'),
                                                              np_cur_run_types.get('m1xl'),
                                                              np_cur_run_types.get('m1xxl')
                                                             )

print "\n"                                                
print "\n"



print "M1.small %d" %np_cur_run_types.get('m1s')
print "M1.medium %d" %np_cur_run_types.get('m1m')
print "M1.large %d" %np_cur_run_types.get('m1l')
print "M1.xlarge %d" %np_cur_run_types.get('m1xl')
print "M1.xxlarge %r" %np_cur_run_types.get('m1xxl')


print "Melbourne Node, Parkville Cell"
print "Total available nodes, cores and memory: %s nodes, %s cores, %d GB"%(qh2_node_count,qh2_stats.get('nac'),qh2_stats.get('nam'))
print "Used cores and memory: %s cores, %s GB"%(qh2_stats.get('nuc'),qh2_stats.get('num'))
print "Free cores and memory: %s cores, %s GB"%(qh2_stats.get('nfc'),qh2_stats.get('nfm'))
print "VM sizes in use(s, m, l, xl, xxl):%s, %s, %s, %s, %s"%(qh2_cur_run_types.get('m1s'),
                                                              qh2_cur_run_types.get('m1m'),
                                                              qh2_cur_run_types.get('m1l'),
                                                              qh2_cur_run_types.get('m1xl'),
                                                              qh2_cur_run_types.get('m1xxl')
                                                             )
print "\n"                                                
print "\n"                                                

print "Monash Node, Monash-01 Cell"
print "Total available nodes, cores and memory: %s nodes, %s cores, %d GB"%(monash_node_count,monash_stats.get('nac'),monash_stats.get('nam'))
print "Used cores and memory: %s cores, %s GB"%(monash_stats.get('nuc'),monash_stats.get('num'))
print "Free cores and memory: %s cores, %s GB"%(monash_stats.get('nfc'),monash_stats.get('nfm'))
print "VM sizes in use(s, m, l, xl, xxl):%s, %s, %s, %s, %s"%(mon_cur_run_types.get('m1s'),
                                                              mon_cur_run_types.get('m1m'),
                                                              mon_cur_run_types.get('m1l'),
                                                              mon_cur_run_types.get('m1xl'),
                                                              mon_cur_run_types.get('m1xxl')
                                                             )
print "\n"                                                
print "\n"


print "Queensland Node, QLD Cell"
print "Total available nodes, cores and memory: %s nodes, %s cores, %d GB"%(qld_node_count,qld_stats.get('nac'),qld_stats.get('nam'))
print "Used cores and memory: %s cores, %s GB"%(qld_stats.get('nuc'),qld_stats.get('num'))
print "Free cores and memory: %s cores, %s GB"%(qld_stats.get('nfc'),qld_stats.get('nfm'))
print "VM sizes in use(s, m, l, xl, xxl):%s, %s, %s, %s, %s"%(qld_cur_run_types.get('m1s'),
                                                              qld_cur_run_types.get('m1m'),
                                                              qld_cur_run_types.get('m1l'),
                                                              qld_cur_run_types.get('m1xl'),
                                                              qld_cur_run_types.get('m1xxl')
                                                             )
print "\n"                                                
print "\n"

print "Total Resources Research Cloud"
print "Total available nodes, cores and memory: %s nodes, %s cores, %d GB"%((np_node_count+qh2_node_count+monash_node_count+qld_node_count),
                                                                            (np_stats.get('nac')+qh2_stats.get('nac')+monash_stats.get('nac')+qld_stats.get('nac')),
                                                                            (np_stats.get('nam')+qh2_stats.get('nam')+monash_stats.get('nam')+qld_stats.get('nam'))
                                                                            )
                                                                            
print "Total used cores and memory: %s cores, %s GB"%((np_stats.get('nuc')+qh2_stats.get('nuc')+monash_stats.get('nuc')+qld_stats.get('nuc')),
                                                      (np_stats.get('num')+qh2_stats.get('num')+monash_stats.get('num')+qld_stats.get('num')), 
                                                      )

print "Free cores and memory: %s cores, %s GB"%((np_stats.get('nfc')+qh2_stats.get('nfc')+monash_stats.get('nfc')+qld_stats.get('nfc')),
                                                      (np_stats.get('nfm')+qh2_stats.get('nfm')+monash_stats.get('nfm')+qld_stats.get('nfm')), 
                                                      )
print "VM sizes in use (s, m, l, xl, xxl): %s, %s, %s, %s, %s" % (total_flavour_count(total_s)['m1s'],
                                                                 total_flavour_count(total_s)['m1m'],
                                                                 total_flavour_count(total_s)['m1l'],
                                                                 total_flavour_count(total_s)['m1xl'],
                                                                 total_flavour_count(total_s)['m1xxl']
                                                                )


                                                                        
                                                                            






count=0
match=re.compile(r'nectar!melbourne!qh2@qh2')
print len(host)
for i in host:
    if match.search(i):
        count+=1
 
print count            
print client.hosts.get('nectar!melbourne!qh2@qh2-rcc84')[0].__dict__
       

total_avail=0
total_used=0
total_avail_mem=0
total_used_mem=0
#print len(host)

for i in np_host:
    #print client.hosts.get()

    total_avail+=int(client.hosts.get(i)[0]._info['resource'].get('cpu'))
    total_used+=int(client.hosts.get(i)[1]._info['resource'].get('cpu'))
    total_avail_mem+=int(client.hosts.get(i)[0]._info['resource'].get('memory_mb'))
    total_used_mem+=int(client.hosts.get(i)[1]._info['resource'].get('memory_mb'))

print "Avail CPUS%r" % total_avail
print "Used CPUS %r"% total_used
print "Avail Memory%r" % total_avail_mem
print "Used Memory %r"% total_used_mem
'''
