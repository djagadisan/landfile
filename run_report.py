import sys
import os
import re
import datetime
from novaaction import NovaAction
from novaclient.v1_1 import client
from config_data import GetVar
from util import GetConfig
import locale
import collections
from report_html_loader import ReportHTML 




class TESTNOVA():

    def createConnection(self, user, key, project_id, auth_url):
        try:
            conn = client.Client(username=user, api_key=key,
                                 project_id=project_id, auth_url=auth_url)

        except Exception, e:
            return "Error %s" % e

        return conn

__init__ = 'main'
encoding = (locale.getpreferredencoding() or sys.stdin.encoding or 'UTF-8')


def get_Resources(cell, client):

    total_avail = total_used = total_avail_mem = total_used_mem = 0
    for i in cell:
        total_avail += int(client.hosts.get(i)[0]._info['resource'].
                           get('cpu'))
        total_used += int(client.hosts.get(i)[1]._info['resource'].
                          get('cpu'))
        total_avail_mem += int(client.hosts.get(i)[0]._info['resource'].
                               get('memory_mb'))
        total_used_mem += int(client.hosts.get(i)[1]._info['resource']
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


def total_flavor_cell(flavour_list):
    m1_small = m1_medium = m1_large = m1_xlarge = m1_xxlarge = others = 0
    for i in flavour_list:
        if i == '0':
            m1_small += 1
        elif i == '1':
            m1_medium += 1
        elif i == '4':
            m1_large += 1
        elif i == '2':
            m1_xlarge += 1
        elif i == '3':
            m1_xxlarge += 1
        else:
            others += 1

    comb_resources = {'m1s': m1_small, 'm1m': m1_medium, 'm1l': m1_large,
                      'm1xl': m1_xlarge, 'm1xxl': m1_xxlarge, 'oth': others}
    return comb_resources


def total_flavour_count(count_t):
    sum = collections.Counter()
    for k in count_t:
        sum.update(k)

    return sum


def getZones(res):

    get_zones = []
    for i in res:
        get_zones.append(i.zone)

    zone_list = set(get_zones)
    return list(zone_list)


def getHostZone(res, zone):

    get_host = []
    for i in res:
        if i.zone == zone:
            get_host.append(i.host.split('@')[1])

    res_z = {'zone': zone, 'hosts': get_host}
    return res_z


def createHostName(top_az, az, cell, host):
    if not cell:
        node_hostname = top_az + "!" + az + "!" + "@" + host
    else:
        node_hostname = top_az + "!" + az + "!" + cell + "@" + host

    return node_hostname


def get_ordinal(num):
    ldig = num % 10
    l2dig = (num // 10) % 10

    if (l2dig == 1) or (ldig > 3) or (num == 20) or (num == 30):
        return '%d%s' % (num, 'th')
    else:
        return '%d%s' % (num, {1: 'st', 2: 'nd', 3: 'rd'}.get(ldig))

now = datetime.datetime.now()
current_date = get_ordinal(int(now.strftime("%d")))
current_mth = now.strftime("%b")
current_year = now.strftime("%Y")
report_date = {"gen_report": current_date + " "
               + current_mth + "," + current_year}


config = GetVar('production')
nov = NovaAction()
info = GetConfig()
client = nov.createNovaConnection(config)

zone = 'nova'
cell = ['np', 'qh2', 'rccomdc', 'cn']
service = 'nova-compute'


np_cur_run_types = total_flavor_cell(_returnServers(client, cell[0]))
qh2_cur_run_types = total_flavor_cell(_returnServers(client, cell[1]))
mon_cur_run_types = total_flavor_cell(_returnServers(client, cell[2]))
qld_cur_run_types = total_flavor_cell(_returnServers(client, cell[3]))

total_s = [qld_cur_run_types, qh2_cur_run_types,
           np_cur_run_types, mon_cur_run_types]
np_cell_nodes = (getHostFrmZone(client, zone).get('np'))
qh2_cell_nodes = (getHostFrmZone(client, zone).get('qh2'))
monash01_cell_nodes = (getHostFrmZone(client, zone).get('monash'))
qld_cell_nodes = (getHostFrmZone(client, zone).get('qld'))

np_data = get_Resources(np_cell_nodes, client)
np_stats = stats_count(np_data)
qh2_data = get_Resources(qh2_cell_nodes, client)
qh2_stats = stats_count(qh2_data)
monash_data = get_Resources(monash01_cell_nodes, client)
monash_stats = stats_count(monash_data)
qld_data = get_Resources(qld_cell_nodes, client)
qld_stats = stats_count(qld_data)




print "NeCTAR Research Cloud Usage Report"
print "\n"
print "Melbourne Node, Noble Park Cell"
print "Total available nodes, cores and memory: %s nodes, %s cores, %d GB"%(len(np_cell_nodes),np_stats.get('nac'),np_stats.get('nam'))
print "Used cores and memory: %s cores, %s GB"%(np_stats.get('nuc'),np_stats.get('num'))
print "Free cores and memory: %s cores, %s GB"%(np_stats.get('nfc'),np_stats.get('nfm'))
print "VM sizes in use(s, m, l, xl, xxl,others):%s, %s, %s, %s, %s, %s"%(np_cur_run_types.get('m1s'),
                                                              np_cur_run_types.get('m1m'),
                                                              np_cur_run_types.get('m1l'),
                                                              np_cur_run_types.get('m1xl'),
                                                              np_cur_run_types.get('m1xxl'),
                                                              np_cur_run_types.get('oth')
                                                             )


print "\n"                                                
print "\n"

print "Melbourne Node, Parkville Cell"
print "Total available nodes, cores and memory: %s nodes, %s cores, %d GB"%(len(qh2_cell_nodes),qh2_stats.get('nac'),qh2_stats.get('nam'))
print "Used cores and memory: %s cores, %s GB"%(qh2_stats.get('nuc'),qh2_stats.get('num'))
print "Free cores and memory: %s cores, %s GB"%(qh2_stats.get('nfc'),qh2_stats.get('nfm'))
print "VM sizes in use(s, m, l, xl, xxl,others):%s, %s, %s, %s, %s, %s"%(qh2_cur_run_types.get('m1s'),
                                                              qh2_cur_run_types.get('m1m'),
                                                              qh2_cur_run_types.get('m1l'),
                                                              qh2_cur_run_types.get('m1xl'),
                                                              qh2_cur_run_types.get('m1xxl'),
                                                              qh2_cur_run_types.get('oth')
                                                             )
print "\n"                                                
print "\n"                                                

print "Monash Node, Monash-01 Cell"
print "Total available nodes, cores and memory: %s nodes, %s cores, %d GB"%(len(monash01_cell_nodes),monash_stats.get('nac'),monash_stats.get('nam'))
print "Used cores and memory: %s cores, %s GB"%(monash_stats.get('nuc'),monash_stats.get('num'))
print "Free cores and memory: %s cores, %s GB"%(monash_stats.get('nfc'),monash_stats.get('nfm'))
print "VM sizes in use(s, m, l, xl, xxl,others):%s, %s, %s, %s, %s, %s"%(mon_cur_run_types.get('m1s'),
                                                              mon_cur_run_types.get('m1m'),
                                                              mon_cur_run_types.get('m1l'),
                                                              mon_cur_run_types.get('m1xl'),
                                                              mon_cur_run_types.get('m1xxl'),
                                                              mon_cur_run_types.get('oth')
                                                             )
print "\n"                                                
print "\n"


print "Queensland Node, QLD Cell"
print "Total available nodes, cores and memory: %s nodes, %s cores, %d GB"%(len(qld_cell_nodes),qld_stats.get('nac'),qld_stats.get('nam'))
print "Used cores and memory: %s cores, %s GB"%(qld_stats.get('nuc'),qld_stats.get('num'))
print "Free cores and memory: %s cores, %s GB"%(qld_stats.get('nfc'),qld_stats.get('nfm'))
print "VM sizes in use(s, m, l, xl, xxl,others):%s, %s, %s, %s, %s, %s"%(qld_cur_run_types.get('m1s'),
                                                              qld_cur_run_types.get('m1m'),
                                                              qld_cur_run_types.get('m1l'),
                                                              qld_cur_run_types.get('m1xl'),
                                                              qld_cur_run_types.get('m1xxl'),
                                                              qld_cur_run_types.get('oth')
                                                             )
print "\n"
print "\n"

print "Total Resources Research Cloud"
print "Total available nodes, cores and memory: %s nodes, %s cores, %d GB"%((len(np_cell_nodes)+len(qh2_cell_nodes)+len(monash01_cell_nodes)+len(qld_cell_nodes)),
                                                                            (np_stats.get('nac')+qh2_stats.get('nac')+monash_stats.get('nac')+qld_stats.get('nac')),
                                                                            (np_stats.get('nam')+qh2_stats.get('nam')+monash_stats.get('nam')+qld_stats.get('nam'))
                                                                            )

print "Total used cores and memory: %s cores, %s GB"%((np_stats.get('nuc')+qh2_stats.get('nuc')+monash_stats.get('nuc')+qld_stats.get('nuc')),
                                                      (np_stats.get('num')+qh2_stats.get('num')+monash_stats.get('num')+qld_stats.get('num')), 
                                                      )

print "Free cores and memory: %s cores, %s GB"%((np_stats.get('nfc')+qh2_stats.get('nfc')+monash_stats.get('nfc')+qld_stats.get('nfc')),
                                                      (np_stats.get('nfm')+qh2_stats.get('nfm')+monash_stats.get('nfm')+qld_stats.get('nfm')), 
                                                      )
print "VM sizes in use (s, m, l, xl, xxl,others): %s, %s, %s, %s, %s, %s" % (total_flavour_count(total_s)['m1s'],
                                                                 total_flavour_count(total_s)['m1m'],
                                                                 total_flavour_count(total_s)['m1l'],
                                                                 total_flavour_count(total_s)['m1xl'],
                                                                 total_flavour_count(total_s)['m1xxl'],
                                                                 total_flavour_count(total_s)['oth']
                                                                )


