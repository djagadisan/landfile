import sys
import re
import datetime
from novaaction import NovaAction
from novaclient.v1_1 import client
from util import GetConfig
import locale
import collections
import prettytable
import textwrap
from report_html_loader import ReportHTML
from config_resource import GetVar
from client_nova import NovaConnection
from novaclient import exceptions
from novaclient.exceptions import BadRequest



config = GetVar()
nov = NovaAction()
info = GetConfig()
client = nov.createNovaConnection(config)

zone = 'nova'
cell = config.hyper_name.split(',')
service = 'nova-compute'
encoding = (locale.getpreferredencoding() or sys.stdin.encoding or 'UTF-8')

#client.availability_zones.list()
#client.aggregates.list()
'''
data_tc = []
s = u"-"
for i in client.availability_zones.list():
    if i.zoneName.find(s) == -1:
        data_tc.append(i.zoneName)

print data_tc
        


for u in client.aggregates.list():
    print u.__dict__
'''
name = 'nectar!melbourne!qh2@61'
#name = 'cn7'
#name = 'netapp'
zone = 'melbourne-qh2'
host = 'rccomdc3'
query = re.compile(r'%s' % name)
qz = re.compile(r'%s' % zone)
hz = re.compile(r'%s' % host)

all_host = client.hypervisors.list(False)
node_info = []
node_print = []
hyper_ob = {}

data = client.hypervisors.get(name)
print data.vcpus_used


'''
for i in all_host:
    if hz.search(i.hypervisor_hostname):
       try:
           node_info.append(i.manager.get(i.id)._info.copy())
       except BadRequest:
           pass


for g in node_info:
    print g
''' 

















        
            #node_info.append(manager.get(i.id)._info.copy())












        #node_info.append(i.manager.get(i.id)._info.copy())
        


















'''
agg_list = client.aggregates.list()

data_test = []
for i in agg_list:
    if query.search(i.name):
        data_test.append(i._info)

val = (az for az in data_test if az['availability_zone'] == zone).next()

print len(val.get('hosts'))
'''













    
'''
    new_data['vcpus'] = data_name.get('vcpus')
    new_data['vcpus_used'] = data_name.get('vcpus_used')
    print data_name.get('vcpus')
    #new_data['vcpus_avail'] = (avail_cpu)
    new_data['memory_mb'] = data_name.get('memory_mb')
    new_data['memory_mb_used'] = data_name.get('memory_mb_used')
    new_data['free_ram_mb'] = data_name.get('free_ram_mb')

'''
'''
for k,v in new_data.iteritems():
    print k, v


dict_property="Property"
wrap=50
pt = prettytable.PrettyTable([dict_property, 'Value'], caching=False)
pt.align = 'l'
for k, v in sorted(new_data.iteritems()):
        if isinstance(v, dict):
            v = str(v)
        if wrap > 0:
            v = textwrap.fill(str(v), wrap)

        if v and isinstance(v, basestring) and r'\n' in v:
            lines = v.strip().split(r'\n')
            col1 = k
            for line in lines:
                pt.add_row([col1, line])
                col1 = ''
        else:
            pt.add_row([k, v])
print(pt.get_string())
'''


    
    