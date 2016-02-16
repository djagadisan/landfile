import os
import sys
import random
import string
import unicodedata
import time
import util
import novaaction
from write_to_csv import WriteCSV 
from util import GetConfig
from novaaction import NovaAction
from novaclient.v1_1 import client
from novaclient.exceptions import *
from novaclient.openstack.common import timeutils
from cinderclient.v2 import client as cclient
from keystoneclient.v2_0 import client as kclient
from config_data import GetVar
from ConfigParser import SafeConfigParser
from util import GetConfig
import datetime
from datetime import date
from random import randint


class TESTNOVA():
    
    def createConnection(self,_user,_key,_project_id,_auth_url):
        try:
            conn = client.Client(username=_user,api_key=_key,project_id=_project_id,auth_url=_auth_url)
            
        except Exception,e:
            return "Error %s" % e 
    
        return conn


    def TestBool(self,sent_stuff):
        
        var_test=1
        if sent_stuff=="ok":
            return True,sent_stuff,var_test
        else:
            return False,sent_stuff,var_test
        
        
def processConfig(section, option):
    try:
        config_file = '/tmp/alloca-config.ini'
        with open(config_file):
            parser = SafeConfigParser()
            parser.read(config_file)

        for section_name in parser.sections():
            try:
                if section_name == section:
                    list_items = parser.get(section_name, option)
            except:
                list_items = None
                return list_items
        return list_items
    except IOError:
        print "Error!, Config File Not found at (/tmp/alloca-config.ini)"
        raise SystemExit


def createConnection(_user,_key,_project_id,_auth_url):
    try:
        conn = client.Client(username=_user,api_key=_key,project_id=_project_id,auth_url=_auth_url)
    except Exception,e:
        return "Error %s" % e 
    return conn

def clientKeystone(username, passwd, tname, a_url):
    try:
        keystone = kclient.Client(username=username,
                                     password=passwd,
                                     tenant_name=tname,
                                     auth_url=a_url)

    except ClientException, e:
        return "Error %s" % e
    return keystone

def getUserInfo(user_id, kclient):
        if user_id:
            get_user = kclient.users.get(user_id)._info

            if 'tenantId'in get_user:
                tenant_name = kclient.tenants.get(get_user.get('tenantId'))
            else:
                tenant_name = kclient.tenants.get(get_user.get('tenant_id'))

            name = tenant_name.description.split("'")[0]
            email = get_user.get('email')
            return {'name': name, 'email': email}
        else:
            return {'name': 'NA', 'email': 'NA'}


__init__='main'


unwanted = processConfig('tenant', 'id').split(',')
csv_temp = processConfig('csv', 'file')
username = processConfig('cred', 'user')
passwd = processConfig('cred', 'passwd')
tname = processConfig('cred', 'name')
a_url = processConfig('cred', 'url')
tm = processConfig('role', 'tm')
zone = 'melbourne-qh2'


#image_id='42857a50-0efe-4b80-b294-2f646cf4b061'
#vm_id='18d23802-14d4-4f87-a9b3-a68e90a86a08'
#vm_id='d9734166-5a02-464b-ae21-78c0a1622b37'




conn = createConnection(username,passwd,tname, a_url)


#data = conn.cells.get()

#print data 

#config = GetVar('production')
#nov=NovaAction()
#info = GetConfig() 
#client= nov.createNovaConnection(config)

#cinderclient = nov.cinderClient(config)
#cc1 = nov.cinderClientV1(config)
#instances_id ='5aabab23-3974-47c3-8b06-d18e39d281a1'
#count_limit=5
#timeout=10
#state='ACTIVE'
#flavour_name='m1.small'
#image_id='662be806-845b-4610-9895-803e0827386b'

#print nov.getImageInfo(image_id, True, client)
#print client 
#print cinderclient
#tenant_id = '42'

#data = client.aggregates.list()
#print data

#zone='nova'
#service='compute'
#host=[]
#id='e08380fcb814436ab28ac2ddb45466f1'
#total_volume = 0
#totald_volume = 0
#snap_volume = []

#quota = cinderclient.quotas.get(tenant_id)
ksclient = clientKeystone(username, passwd, tname, a_url)
#print ksclient
tenant_data = ksclient.tenants.get('3f6533bcb63d43a3a27711df6f750334')
vicnode_id='2014R11.07'
print tenant_data.id
ksclient.tenants.update(tenant_data.id, vicnode_id=vicnode_id)
'''
all_tenants = 1
search_opts = {'all_tenants': all_tenants}
tenant_id = '42'
search_opts = {'all_tenants': all_tenants, 'tenant':tenant_id}

aggr = conn.aggregates.list()
for i in aggr:
    #print i.name, i.metadata.get('production'), i.metadata.get('availability_zone')
    if i.metadata.get('production') !='false':
        print i.name, i.metadata.get('production'), i.hosts

'''

#h_host = 'cc4'
# marker = None

# if marker:
    #search_opts['marker'] = marker
#server = conn.servers.list(search_opts=search_opts)
#print server
#data = conn.aggregates.list()
#for i in data:
#    print i.name
    
#conn.aggregates

#var_ = 'nova'
#server = conn.hosts.list_all(var_)#

#for i in server:
#    print conn.hosts.get(i.host_name)
#host = 'np-rcc11'
#server = conn.hosts.get(host)

#server = conn.hypervisors.list(False)
#for i in server:
#    print i.__dict__

#server = conn.hypervisors.get('qh2-rcc41.melbourne.nectar.org.au')





#print server
    


#else
#count = 0
#for s in server:
#    print s.__dict__

    
#print count
        


        
    

#    print s.name
#    print getUserInfo(s.user_id, kc)

#availability_zones = cc1.availability_zones.list(detailed=False)
#vol_ = cinderclient.quotas.get(tenant_id,usage=True)
#print vol_

#vol_ = cinderclient.quotas.get(tenant_id)
#print vol_


#print kc
#user_list = kc.users.list()
#for u in user_list:
#    print u
    
#zone='nova'
#host_server = client.hosts.list_all(zone)
#print host_server


'''
volumes_list = cinderclient.volume_snapshots.list(search_opts=search_opts)
for v in volumes_list:
    snap_volume.append(v.volume_id)

volume_list = cinderclient.volumes.list(search_opts=search_opts)

cs = [ z for z in volume_list for y in snap_volume if z.id == y]

for i in cs:
    if i.availability_zone == 'melbourne-qh2':
        total_volume += v.size
        
print total_volume
        

    
'''
'''
volumek_list = cinderclient.volumes.list(search_opts=search_opts)
for v in volumek_list:
    print v
    if v._info['availability_zone'] == 'melbourne-qh2':
        if v._info['status'] == 'in-use' or v._info['status'] == 'available':
            print v._info['availability_zone'], v._info['status']
            totald_volume += v.size

print totald_volume
'''
    
#print quota._info.keys()
#print cinderclient
##pdat = client.hypervisors.list()
#for i in pdat:
#    print i.id, i._loaded, i.hypervisor_hostname

'''
all_tenants = 1
search_opts = {'all_tenants': all_tenants}
volume_list = cinderclient.volumes.list(search_opts=search_opts)
for v in volume_list:
    if getattr(v,'os-vol-tenant-attr:tenant_id') == id:
        total_volume += v.size

print total_volume
'
#start_a = date(2012,01,26)
#today_year = datetime.datetime.now().strftime("%Y")
#today_month = datetime.datetime.now().strftime("%m")
#today_day = datetime.datetime.now().strftime("%d")
#end_date = date(int(today_year), int(today_month), int(today_day))
#sc = end_date - start_a
#print sc.days
#now = datetime.datetime.utcnow()

#total_hours = 0
#end = now + datetime.timedelta(days=1)
#start = now - datetime.timedelta(days=(end_date - start_a).days)
#start = now - datetime.timedelta(weeks=100)


#total_cpu = 0
#total_memory = 0
#data_report = client.usage.get(id, start, end).server_usages
#print len(data_report)











for i in client.hosts.list_all():
    if i.service == unicode(service):
        print i.host_name
        host.append(i.host_name)
        #print i.host_name
        


        
   
     
#    
total_avail=0
total_used=0
print len(host)
#for i in host:
    
#    total_avail=total_avail+int(client.hosts.get(i)[0]._info['resource'].get('cpu'))
#    total_used=total_used+int(client.hosts.get(i)[1]._info['resource'].get('cpu'))

#print "Avail %r" % total_avail
#print "Used %r"% total_used
  
    
     
    #print i._

     
    
    
#for i in range(1,100):
#    print "No:%r" % i
#    
#    print nov.getInstancesInfo(instances_id,client)[0].status
#    time.sleep(2)



while nov.getImageInfo(image_id,False, client)==None:
    print "OK"
    time.sleep(5)

print nov.deleteSnapshot(image_id, client)

print snap_image
try:
    snap_image.delete()
except Forbidden, e:
    print e
#remote_file='test-U0WKXO-290513150258'
#ssh_client = info.connectSSH('118.138.240.234','ec2-user','/tmp/.key_rc-U0WKXO-290513150258')
#cmd2="md5sum "+remote_file+" | cut -d' ' -f1"

#print "Value %s" % (info.runCommand(ssh_client,cmd=cmd2,_type=2))
#vm_id='77ae1ffa-d8fe-4aa8-89c4-f86cd2df130d'

#print info._pollStatus(config.timeout,vm_id,'ACTIVE',10,client)


#for i in range(5):
#    for i in client.images.list():
        #if i.id==unicode(image_id):
         #   print i    



#data1=nov.getInstancesInfo(instances_id,client)
#count_limit=5
#print info._pollInstancesTerminated(config.timeout,count_limit, vm_id, client)
#data=['1','2','3','4','5','6']
#print data
#write_data = WriteCSV().createCSVFile(config.csv_file,data)
#now = 

#print datetime.datetime.now().strftime("%d%m%y%H%M%S")
#print config.cp_file
#print info.sampleFile(config.cp_file)
 









print 

'''




'''
test_ = NovaAction()
client=test_.createNovaConnection(config)
test_.removeSecurityGroupRules(secure_group, client)
'''



'''
dict ={'sg':'xxxxx','keypair':'key'}



config = GetVar('deven')
images_test = NovaAction()
#image='b025abeb-d07c-4dfa-9b31-ad791203a101'

#results = images_test.getImageInfo(image,False, images_test.createNovaConnection(config))
#print results
#images_test.deleteSnapshot(image, images_test.createNovaConnection(config))
seg = '07DVXB-160513173723'
print images_test.getSecurityGroup(seg,images_test.createNovaConnection(config))


helper_ = GetConfig()
nova_action = NovaAction()

infra='preproduction'
username = helper_.process_config(infra,'user')
passwd = helper_.process_config(infra,'passwd')
name = helper_.process_config(infra,'name')
url = helper_.process_config(infra,'url')
image_id = helper_.process_config('image','image_id')
image_username = helper_.process_config('image','user_name')
work_directory = helper_.process_config('config','directory')
ssh_key_name = helper_.process_config('config','ssh_key_name') 
timeout = helper_.process_config('timeout','period')
flavour_name = helper_.process_config('flavour','flavour_type')
cp_file = helper_.process_config('file_check','local_file')
tmp_dir = helper_.process_config('file_check','tmp_dir')
cell = helper_.process_config('cell','location')
client = nova_action.createNovaConnection(username,passwd,name,url)
scheduler={'cell':cell}

ssh_key_name = work_directory+"/"+ssh_key_name
startTime = time.time()
test_name = helper_._randomName()
keypair = nova_action.createKeypair(test_name,client)

stat=helper_.writeFiles(ssh_key_name,keypair.private_key)

print "Test started at %r" % startTime 
if keypair!=None and stat==0:
    print "Keypair %s created" %test_name

security_group = nova_action.createSecurityGroup(test_name,client)
security_grouprules = nova_action.createSecurityGroupRules(security_group.id,'tcp','22','22',client)

print "Security %s Group Created" % security_group.name
print "Rules 'tcp', '22' 0.0.0.0/0 added"


flavour_info=nova_action.getFlavour(flavour_name,client)

print "Image %s " % image_id
print "Instances type %s" % flavour_info.name
print "Instances launching in 30 seconds"
time.sleep(20)
print "Running Instances "

run_instances = nova_action.runInstances(test_name,image_id,flavour_info.id,keypair.name,security_group.name.split(','),client,placement=scheduler)       

if run_instances!=None: 
    print "Instances launched Sucessfully"
else:
    print "Error Instances Failed to launch, Cleaning Up"

#poll the instances status until it becomes active
if helper_._pollStatus(timeout,run_instances.id,'ACTIVE',10,client)==True:
   vm_info = nova_action.getInstancesInfo(run_instances.id,client)
   print "Instances: %s, IP: %s, Status: %s" %(vm_info[0].name,vm_info[1][0],vm_info[0].status)
   print "Port 22 Test"
   if helper_.checkPortAlive(vm_info[1][0],int(timeout),22)==True:
       print "Port alive"
       print "Run File Check"
       time.sleep(10)
       if helper_.fileCheck(vm_info[1][0],image_username,cp_file,tmp_dir,ssh_key_name)==True:
           print "Check File ok"
           print "Reboot Server"
           nova_action.rebootInstances(vm_info[0])
           time.sleep(int(timeout))
           if helper_.checkPortAlive(vm_info[1][0],int(timeout),22)==True:
               print "Reboot OK"
               print "Run Snapshot"
               snapshot_ = nova_action.createSnapshot(test_name,vm_info[0].id,client)
               
               count=0
               while nova_action.getImageInfo(snapshot_,client)!='ACTIVE':
                   if count!=30:
                       
                       print nova_action.getImageInfo(snapshot_,client)
                
                       if nova_action.getImageInfo(snapshot_,client)!='ERROR':
                           time.sleep(10)
                           count=count+1
                           print count
                       elif nova_action.getImageInfo(snapshot_,client)==None:
                               print "Snapshot Failed, most likely killed"
                               raise SystemExit
                   else:
                        print "Snapshot failed, timeout after %s seconds" % (int(time.time()-startTime))
                        raise SystemExit
                        
                        
               print "Snapshot %s is ok," % snapshot_
               print "Test took %r seconds to finish" %  (int(time.time()-startTime))
               print "Launching VM from snapshot"
               run_snap = nova_action.runInstances("from-snap-"+test_name,snapshot_,flavour_info.id,keypair.name,security_group.name.split(','),client) 
             
                        
           else:
               print "Reboot Failed"
               raise SystemExit       
       else:
           print "Check File Failed"
           raise SystemExit
               
       
   else:
        print "Timeout from boot, it took %s seconds" %(time.time()- startTime)
        raise SystemExit
       
else:
    print "Timeout from build, stuck in %r for more than %r" % (run_instances.status, (time.time()-startTime)) 
    raise SystemExit    
    








#nova_action.deleteKeypair(keypair.name,client)
#helper_.removeFiles(work_directory+"/"+ssh_key_name)
#nova_action.removeSecurityGroupRules(security_group.id,client)

#vm_id='5888c8cc-d9f3-44d0-8aae-0c21650daec4'
#nova_action.deleteInstances(vm_id,client)
'''
