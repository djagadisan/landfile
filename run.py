#!/usr/bin/env python
import sys
import jinja2
import os
import re
import datetime
import time
import locale
import collections
from novaaction import NovaAction
from novaclient.v1_1 import client
from util import GetConfig
from multiprocessing import Process, Queue, Pool, pool
from report_html_loader import ReportHTML
from config_resource import GetVar 
from client_nova import NovaConnection
from multiprocessing.pool import ThreadPool
from email_sender import SendEmail
from resource_csv import ResourceWriteCSV
from novaclient.exceptions import ClientException, BadRequest



def get_Resources(cell, client):

    res_l = []
    total_avail = total_used = total_avail_mem = total_used_mem = 0

    for i in cell:
        res_l.append(client.hosts.get(i))

    for r in res_l:
        total_avail += int(r[0]._info['resource'].
                           get('cpu'))
        total_used += int(r[1]._info['resource'].
                          get('cpu'))
        total_avail_mem += int(r[0]._info['resource'].
                               get('memory_mb'))
        total_used_mem += int(r[1]._info['resource']
                              .get('memory_mb'))

    resources = {'avail_cpu': total_avail, 'avail_mem': total_avail_mem,
                    'used_cpu': total_used, 'used_mem': total_used_mem}

    return resources


def getHostFrmZone(client, zone):
    np = re.compile(r'nectar!melbourne!np@np')
    qh2 = re.compile(r'nectar!melbourne!qh2@qh2')
    monash = re.compile(r'nectar!monash!monash-')
    qld = re.compile(r'nectar!qld@')

    np_host, qh2_host, monash_01_host, qld_host = ([] for i in range(4))
    for i in client.hosts.list_all(zone):
        if np.search(i.host_name):
            np_host.append(i.host_name)
        elif qh2.search(i.host_name):
            qh2_host.append(i.host_name)
        elif monash.search(i.host_name):
            monash_01_host.append(i.host_name)
        elif qld.search(i.host_name):
            qld_host.append(i.host_name)

    resources = {'np': np_host, 'qh2': qh2_host, 'monash': monash_01_host,
                'qld': qld_host}
    return resources


def returnNodes(client, zone, search_):

    query = re.compile(r'%s@' % search_)
    host_count = []
    for i in client.hosts.list_all(zone):
        if query.search(i.host_name):
            host_count.append(i.host_name)

    return host_count


def hypervisor_count(client, search_):

    query = re.compile(r'%s@' % search_)
    server_list = RequestRetries('host_list', client)
    data = [x for x in server_list if query.search(x.id)]

    return data


def hypervisor_usage(data):
    total_avail = total_used = total_avail_mem = total_used_mem = 0
    for i in data:
        total_avail += int(i.vcpus)
        total_used += int(i.vcpus_used)
        total_avail_mem += int(i.memory_mb)
        total_used_mem += int(i.memory_mb_used)

    resources = {'avail_cpu': total_avail, 'avail_mem': total_avail_mem,
                    'used_cpu': total_used, 'used_mem': total_used_mem}
    return resources


def stats_count(_data):
    fc = _data.get('avail_cpu')
    fm = (_data.get('avail_mem') / 1024)
    uc = _data.get('used_cpu')
    um = (_data.get('used_mem') / 1024)
    ac = fc - uc
    am = fm - um
    resources = {'nac': fc, 'nam': fm, 'nuc': uc, 'num': um,
                'nfc': ac, 'nfm': am}
    return resources


def _returnServers(client, cell):

    count_all = []
    args_a = {'all_tenants': 1, 'host': cell}
    instances = client.servers.list(search_opts=args_a)
    for i in instances:
        if isinstance(i.__dict__.get('OS-EXT-SRV-ATTR:host'), unicode):
            count_all.append(i.flavor.get('id'))

    return count_all


def return_vm_type_count(client, data):
    count_all = []
    for d in data:
        args_a = {'all_tenants': 1,
                  'host': d.hypervisor_hostname.split('.')[0]
                  }
        server = client.servers.list(search_opts=args_a)

        if not server:
            args_a = {'all_tenants': 1,
                  'host': d.hypervisor_hostname
                  }
            server = client.servers.list(search_opts=args_a)

        for i in server:
            if isinstance(i.__dict__.get('OS-EXT-SRV-ATTR:host'), unicode):
                count_all.append(i.flavor.get('id'))
    return count_all


def _returnServers2(client, cell):
    count_all = []
    count_host = []
    args_a = {'all_tenants': 1, 'host': cell}
    instances = client.servers.list(search_opts=args_a)
    for i in instances:
        if isinstance(i.__dict__.get('OS-EXT-SRV-ATTR:host'), unicode):
            count_all.append(i.flavor.get('id'))
            count_host.append(i.__dict__.get('OS-EXT-SRV-ATTR:host'))

    return count_all, count_host


def totalVMType(flavour_list, host):

    count = []
    for i in host:
        if i in flavour_list.values():
            for key, value in flavour_list.items():
                if value == i:
                    count.append(key)
        else:
            count.append('others')

    return collections.Counter(count)


def total_flavour_count(count_t):
    sum = collections.Counter()
    for k in count_t:
        sum.update(k)

    return sum


def getTopAZ(client):
    data_tc = []
    s = u"-"
    for i in client.availability_zones.list():
        if i.zoneName.find(s) == -1:
            data_tc.append(i.zoneName)

    return data_tc


def filterAz(client, zone):
    fil_az, fil_name, fil_cell, fil_pcell, fil_host = ([] for i in range(5))
    host_server = RequestRetries('host_list_all', client, zone)
    for i in host_server:
        fil_pcell.append(i.host_name.split('@')[0])
        fil_host.append(re.split(r'\d',
                                 i.host_name.split('@')[1].split('-')[0])[0])

    fil_name = sorted(list(set(fil_pcell)))
    for i in fil_name:
        fil_az.append(i.split('!'))

    for i in fil_az:
        if len(i) > 2:
            fil_cell.append(i[2])
        else:
            fil_cell.append(i[1])

    return fil_name, fil_cell, list(set(fil_host))


def getAvailFlav(client):
    data_flav = {}
    for i in client.flavors.list(False):
        data_flav[i.name] = i.id

    return data_flav


def createHostName(top_az, az, cell, host):
    if not cell:
        node_hostname = top_az + "!" + az + "!" + "@" + host
    else:
        node_hostname = top_az + "!" + az + "!" + cell + "@" + host

    return node_hostname


def computeStats(node_name, dic, zone, i, client, z, r_outs):

    print "Getting data from zone %s" % node_name
    #node_info = returnNodes(client, zone, i)
    node_info = hypervisor_count(client, i)
    nodes_count = len(node_info)

    #nodes_rc = stats_count(get_Resources(node_info, client))
    nodes_rc = stats_count(hypervisor_usage(node_info))
    #type_ = totalVMType(dic, _returnServers(client, _az2))
    type_ = totalVMType(dic, return_vm_type_count(client, node_info))
    if 'others' in list(type_.elements()):
        others = type_['others']
    else:
        others = 0

    print "%s done!" % node_name

    stats_q = {'node_name': node_name, 'node_count': nodes_count,
                'nac': nodes_rc.get('nac'), 'nam': nodes_rc.get('nam'),
                'nuc': nodes_rc.get('nuc'), 'num': nodes_rc.get('num'),
                'nfc': nodes_rc.get('nfc'), 'nfm': nodes_rc.get('nfm'),
                't_s': type_['m1.small'], 't_m': type_['m1.medium'],
                't_l': type_['m1.large'], 't_xl': type_['m1.xlarge'],
                't_xxl': type_['m1.xxlarge'], 'oth': others
                }
    r_outs.put(stats_q)


def RequestRetries(meth, client, var_=None):

    attempt = 10

    for x in xrange(int(attempt)):
        try:
            if meth == 'gr':
                return client.hosts.get(var_)
                break
            if meth == 'host_list':
                return client.hypervisors.list()
            if meth == 'host_list_all':
                return client.hosts.list_all(var_)
        except Exception:
            time.sleep(5)
    return False


def get_ordinal(num):
    ldig = num % 10
    l2dig = (num // 10) % 10

    if (l2dig == 1) or (ldig > 3) or (num == 20) or (num == 30):
        return '%d%s' % (num, 'th')
    else:
        return '%d%s' % (num, {1: 'st', 2: 'nd', 3: 'rd'}.get(ldig))

start_time = time.time()
html_data = []
now = datetime.datetime.now()
current_date = get_ordinal(int(now.strftime("%d")))
report_date = current_date + " " + now.strftime("%b, %Y, %H:%M")
send_date = now.strftime("%d_%m_%Y_%H_%M")
working_path = os.getcwd()

config = GetVar()
nov = NovaAction()
info = GetConfig()

zone = 'nova'
cell = config.hyper_name.split(',')
service = 'nova-compute'

client = nov.createNovaConnection(config)
dic = getAvailFlav(client)


_info_az = filterAz(client, zone)

t_nodes = t_cores = t_mem = 0
u_cores = u_mem = f_cores = f_mem = 0
t_s = t_m = t_l = t_xl = t_xxl = oth = 0
total_type = []


if __name__ == '__main__':

    jobs = []

    r_outs = [Queue() for q in range(len(_info_az[0]))]
    print  _info_az
    print len((_info_az[0]))
    for z, i in enumerate(_info_az[0]):
        try :
            client_hy = nov.createNovaConnection(config)
            p = Process(name=z, target=computeStats,
                    args=(_info_az[1][z], dic,
                          zone, i, client_hy, z, r_outs[z]))
            jobs.append(p)
            p.start()
        except IndexError:
            pass 

    for p in jobs:
        p.join()
    html_array = []
    for q in r_outs:
        html_array.append(q.get())


for i in html_array:
    nfc = i.get('nfc')
    nfm = i.get('nfm')
    if nfc < 0 and nfm < 0:
        nfc = 0
        nfm = 0

    t_nodes += i.get('node_count')
    t_cores += i.get('nac')
    t_mem += i.get('nam')
    u_cores += i.get('nuc')
    u_mem += i.get('num')
    f_cores += nfc
    f_mem += nfm
    t_s += i.get('t_s')
    t_m += i.get('t_m')
    t_l += i.get('t_l')
    t_xl += i.get('t_xl')
    t_xxl += i.get('t_xxl')
    oth += i.get('oth')


dict_final = {'total_nodes': t_nodes, 'total_cores': t_cores,
              'total_mem': t_mem, 'used_cores': u_cores,
              'used_mem': u_mem, 'free_cores': f_cores,
              'free_mem': f_mem, 'total_small': t_s,
              'total_medium': t_m, 'total_large': t_l,
              'total_xl': t_xl, 'total_xxl': t_xxl,
              'oth': oth
              }

pass_report = ReportHTML()
send_email = SendEmail()
write_to_csv = ResourceWriteCSV()
html_file = "/tmp/" + now.strftime("%d_%m_%Y_%H_%M") + ".html"
attach = "/tmp/allocation_report.csv"
pass_report.templateLoader(html_array, dict_final, report_date, html_file)
send_email.email_user(html_file, attach)
write_to_csv.createCSVFileNode('/tmp', html_array)
write_to_csv.createCSVFileCloud('/tmp', dict_final)
os.remove(attach)
