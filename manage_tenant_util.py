import sys
import os
import prettytable
import textwrap
import datetime
from multiprocessing import Process, Queue
from datetime import date
from keystoneclient.v2_0 import client as client_keystone
from novaclient.v1_1 import client as client_nova
from cinderclient.v2 import client as client_cinder
from keystoneclient.exceptions import NotFound
from novaclient.openstack.common import timeutils

AUTH_USER = os.environ.get('OS_USERNAME', None)
AUTH_PASSWORD = os.environ.get('OS_PASSWORD', None)
AUTH_TENANT_NAME = os.environ.get('OS_TENANT_NAME', None)
AUTH_URL = os.environ.get('OS_AUTH_URL', None)
AUTH_REGION = os.environ.get('OS_REGION_NAME', None)
TENANT_MANAGER = 'TenantManager'
MEMBER = 'Member'

MEMORY_VAR = 4096
START_DATE = date(2012, 01, 26)

for auth_variable in (AUTH_USER, AUTH_PASSWORD,
                      AUTH_TENANT_NAME, AUTH_URL):
    if not auth_variable:
        print "Missing Nova environment variables!"
        sys.exit(1)


def client_conn(type_):
    if type_ == 'nova':
        client = client_nova.Client(username=AUTH_USER,
                                    insecure=True,
                                    api_key=AUTH_PASSWORD,
                                    project_id=AUTH_TENANT_NAME,
                                    auth_url=AUTH_URL,
                                    region_name=AUTH_REGION)
    elif type_ == 'keystone':
        client = client_keystone.Client(username=AUTH_USER,
                                        insecure=True,
                                        password=AUTH_PASSWORD,
                                        tenant_name=AUTH_TENANT_NAME,
                                        auth_url=AUTH_URL)
    elif type_ == 'cinder':
        client = client_cinder.Client(username=AUTH_USER,
                                      insecure=True,
                                      api_key=AUTH_PASSWORD,
                                      project_id=AUTH_TENANT_NAME,
                                      auth_url=AUTH_URL,
                                      region_name=AUTH_REGION,
                                      service_type='volume'
                                      )

    return client


def pre_check(client, args_, in_data):
    if args_ == 'user':
        try:
            data_value = client.users.find(name=in_data).id
        except:
            return False
    elif args_ == 'tenant':
        try:
            data_value = client.tenants.find(name=in_data).id
        except NotFound:
            try:
                data_value = client.tenants.find(id=in_data).id
            except NotFound:
                return False
    elif args_ == 'tm_role':
        try:
            data_value = client.roles.find(name=in_data).id
        except Exception:
            return False
    elif args_ == 'm_role':
        try:
            data_value = client.roles.find(name=in_data).id
        except:
            return False

    return data_value


def setup_tenant(args_data, user_id):
    clientk = client_conn('keystone')
    if 't' in args_data:
        tenant_name = args_data.t
    else:
        tenant_name = args_data['tenant_name']
        tenant_description = args_data['tenant_name']

    tenant_name = args_data.t

    if args_data.d is None:
        args_data.d = args_data.t
    tenant_description = " ".join(args_data.d)
    role_manager_id = pre_check(clientk, "tm_role", TENANT_MANAGER)
    role_member_id = pre_check(clientk, "m_role", MEMBER)

    try:
        tenant = clientk.tenants.create(tenant_name,
                                        tenant_description
                                        )
        clientk.tenants.add_user(tenant.id,
                                 user_id,
                                 role_manager_id
                                 )
        clientk.tenants.add_user(tenant.id,
                                 user_id,
                                 role_member_id
                                 )
        keystone_update(tenant.id, args_data, _opt='add_tenant')

    except Exception:
        return False

    return tenant.id


def keystone_update(tenant_id, args_data, _opt=None):
    client = client_conn('keystone')
    #tenant_i = client.tenants.find(id=tenant_id)
    args_update = {}
    if _opt is not None:
        args_update.update({'allocation_id': args_data.a})
    else:
        if args_data.n is not None:
            args_update.update({'name': args_data.n})
        elif args_data.e is not None:
            args_update.update({'enabled': args_data.e})
        elif args_data.d is not None:
            args_update.update({'description': args_data.d})
        elif args_data.a is not None:
            args_update.update({'allocation_id': args_data.a})
        elif args_data.v is not None:
            print args_data.v
            args_update.update({'vicnode_id': args_data.v})
    try:
        client.tenants.update(tenant_id, **args_update)
    except Exception:
        return False

    return True


def nova_update(tenant_id, args_data):
    clientn = client_conn('nova')
    if args_data.c is not None:
        requested_ram = (args_data.c * MEMORY_VAR)

    try:
        if args_data.c is not None and args_data.i is not None:
            clientn.quotas.update(tenant_id, cores=args_data.c,
                                  ram=requested_ram,
                                  instances=args_data.i
                                  )
        elif args_data.c is not None:
            clientn.quotas.update(tenant_id, cores=args_data.c,
                                  ram=requested_ram
                                  )
        elif args_data.i is not None:
            clientn.quotas.update(tenant_id, instances=args_data.i)

        return True
    except Exception, e:
        print e
        return False


def cinder_update(tenant_id, args_data):
    clientc = client_conn('cinder')
    volume_size = args_data.g
    total_volume = args_data.v
    if 's' in args_data:
        total_snapshot = args_data.s
    try:

        if volume_size is not None and total_volume is not None:
            clientc.quotas.update(tenant_id=tenant_id,
                                  gigabytes=volume_size,
                                  volumes=total_volume,
                                  snapshots=total_volume
                                  )
        elif volume_size is not None:
            clientc.quotas.update(tenant_id=tenant_id,
                                  gigabytes=volume_size
                                  )
        elif total_volume is not None:
            clientc.quotas.update(tenant_id=tenant_id,
                                  volumes=total_volume,
                                  )
        elif total_snapshot is not None:
            clientc.quotas.update(tenant_id=tenant_id,
                                  snapshots=total_snapshot
                                  )
    except:
        return False

    return True


def pre_check_batch(args_data):
    vars_array = []

    for vars_ in args_data.s.split(','):
        vars_array.append(''.join(vars_.split()))

    if len(vars_array) == 6:
        volume_size = vars_array[4]
        allocation_id = vars_array[5]
    else:
        volume_size = 0
        allocation_id = vars_array[4]

    vars_dict = {'tenant_name': vars_array[0],
                'tenant_desc': vars_array[0],
                'tenant_email': vars_array[1],
                'tenant_cores': vars_array[2],
                'tenant_inst': vars_array[3],
                'tenant_volumes': volume_size,
                'tenant_allocat:': allocation_id
                }

    return vars_dict


def select_options(args_data, operation):

    clientk = client_conn('keystone')
    if 't' in args_data:
        tenant_id = pre_check(clientk, "tenant", args_data.t)
    else:
        args_data = pre_check_batch(args_data)
        tenant_manager = pre_check(clientk, "user", args_data['tenant_email'])

    if operation == 'add':
        tenant_manager = pre_check(clientk, "user", args_data.e)
        if tenant_manager:
            if tenant_id is False:
                    task_options(args_data, operation, user_id=tenant_manager)
            else:
                print "Project %s exists" % args_data.t
                sys.exit(1)
        else:
            print "Users %s does not exists" % args_data.e
            sys.exit(1)

    elif operation == 'search':
        if tenant_id:
            task_options(args_data, operation, tenant_id=tenant_id)
            sys.exit(1)
        else:
            print "Project does not exists %s" % args_data.t
            sys.exit(1)

    elif '_update' in operation:
        if tenant_id:
            task_options(args_data, operation, tenant_id=tenant_id)
            sys.exit(1)
        else:
            print "Project does not exists %s" % args_data.t
            sys.exit(1)

    elif operation == 'email':
        if tenant_manager:
            if pre_check(clientk, "tenant", args_data['tenant_name']) is False:
                task_options(args_data, operation, user_id=tenant_manager)
            else:
                print "Project %s exists" % args_data['tenant_name']
                sys.exit(1)
        else:
            print "Users %s does not exists" % args_data['tenant_email']
            sys.exit(1)



def task_options(args_data, operation, user_id=None, tenant_id=None):
    if operation == 'add':
        tenant_id = setup_tenant(args_data, user_id)

        while tenant_id:
            nova_quota = nova_update(tenant_id, args_data)

            if nova_quota:
                if args_data.g is not None or args_data.v is not None:
                    cinder_quota = cinder_update(tenant_id, args_data)

                tenant_details(tenant_id, options='display')
                break
            else:
                print "Error adding quota %s %s" % (nova_quota, cinder_quota)
                sys.exit(1)
        else:
            print "Error creating tenant"
            sys.exit(1)
    elif operation == 'email':
        print "Email"
    elif operation == 'keystone_update':
        if keystone_update(tenant_id, args_data):
            tenant_details(tenant_id, options='display')
        else:
            print "Error updating tenant"

    elif operation == 'nova_update':
        nova_quota = nova_update(tenant_id, args_data)
        if nova_quota:
            tenant_details(tenant_id, options='display')
        else:
            print "Error adding quota %s" % (nova_quota)
            sys.exit(1)
    elif operation == 'cinder_update':
        cinder_quota = cinder_update(tenant_id, args_data)
        if cinder_quota:
            tenant_details(tenant_id, options='display')
        else:
            print "Error adding quota %s" % (cinder_quota)
            sys.exit(1)
    elif operation == 'search':
        if tenant_details(tenant_id) is not True:
            print "Erro unable to get tenant info %s" % (tenant_id)
            sys.exit(1)


def tenant_details(tenant_id, options=None):
    tenant_info = get_tenant_info(tenant_id)

    print_pretty(tenant_info, wrap=50,
                 dict_property="Tenant Details"
                 )
    resource = get_resource_details(tenant_id)
    print_pretty(resource, wrap=50,
                 dict_property="Quota Allocated"
                 )
    print_text(tenant_info)
    print_text(resource)
    if options is None:

        if resource.get('Allocated Gigabytes') is 0:
            used_resource = get_resource_usage(tenant_id,
                                               volume_status=0
                                               )
            print_pretty(used_resource, wrap=50,
                         dict_property="Current Usage"
                         )
        else:
            used_resource = get_resource_usage(tenant_id)
            print_pretty(used_resource, wrap=50,
                         dict_property="Current Usage"
                         )

    return True


def get_resource_details(tenant_id):
    nclient = client_conn('nova')
    cclient = client_conn('cinder')
    allocated_cores = nclient.quotas.get(tenant_id).cores
    allocated_ram = (nclient.quotas.get(tenant_id).ram) / 1024
    allocated_instances = nclient.quotas.get(tenant_id).instances
    allocated_gigabytes = cclient.quotas.get(tenant_id).gigabytes
    allocated_volumes = cclient.quotas.get(tenant_id).volumes
    allocated_snapshot = cclient.quotas.get(tenant_id).snapshots

    resource_data = {'Allocated Cores:': allocated_cores,
                     'Allocated RAM:': allocated_ram,
                     'Allocated Instances:': allocated_instances,
                     'Allocated Gigabytes:': allocated_gigabytes,
                     'Allocated Volumes:': allocated_volumes,
                     'Allocated Snapshots:': allocated_snapshot}
    return resource_data


def get_resource_usage(tenant_id, volume_status=None):
    nclient = client_conn('nova')
    cclient = client_conn('cinder')
    now = timeutils.utcnow()
    end = now + datetime.timedelta(days=1)
    start = now - datetime.timedelta(days=1)
    total_cpu = 0
    total_memory = 0
    total_volumes = 0
    number_of_vms = 0
    active_servers = []
    total_vcpus_used = 0
    total_memory_used = 0
    total_hours = 0
    timeout = 45
    tenant_report = nclient.usage.get(tenant_id, start, end)
    
    print tenant_report.server_usages
    
        #if hasattr(i, 'server_usages'):
         #   data_v += 1
            
    #print data_v

    if hasattr(tenant_report, 'server_usages'):
        data_report = tenant_report.server_usages
        active_servers = [i for i in data_report if i.get('state') == 'active'
                           or i.get('state') == 'stopped'
                           or i.get('state') == 'suspended'
                           or i.get('state') == 'paused']

        for ac in active_servers:
            total_cpu += ac.get('vcpus')
            total_memory += ac.get('memory_mb')
        number_of_vms = count_num_vms(nclient, tenant_id)

        total_vcpus_used = tenant_report.total_vcpus_usage
        total_memory_used = tenant_report.total_memory_mb_usage
        total_hours = tenant_report.total_hours

    if volume_status is None:

        #total_volumes = spawn_process(tenant_id, cclient, timeout)
        total_volumes = get_volume_usage(tenant_id, cclient)

    if total_volumes is False:
        total_volumes = 'N/A'

    usage_data = {'CPU:': total_cpu,
                  'Memory:': total_memory,
                  'Volumes Size Used:': total_volumes['disk_used'],
                  'No volumes :': total_volumes['no_volumes'],
                  'No snapshots :': total_volumes['no_snapshots'],
                  'No active VMs:': len(active_servers),
                  'Total VM Launched:': number_of_vms,
                  'Total CPU Usage:': total_vcpus_used,
                  'Total Memory Usage:': total_memory_used,
                  'Total Hour Usage:': total_hours
                  }
    return usage_data


def get_volume_usage(tenant_id, client):
    volume_info = {}
    used = client.quotas.get(tenant_id, usage=True)
    volume_info['disk_used'] = used.gigabytes['in_use']
    volume_info['no_volumes'] = used.volumes['in_use']
    volume_info['no_snapshots'] = used.snapshots['in_use']

    return volume_info

'''
def get_volume_usage(tenant_id, client, queue):
    total_volumes = 0
    search_opts = {'all_tenants': 1}
    volume_list = client.volumes.list(search_opts=search_opts)
    for v in volume_list:
        if getattr(v, 'os-vol-tenant-attr:tenant_id') == tenant_id:
            total_volumes += v.size

    queue.put(total_volumes)

'''


def spawn_process(tenant_id, client, timeout):
    queue = Queue()
    p = Process(target=get_volume_usage,
                args=(tenant_id, client, queue)
                )
    p.start()
    p.join(int(timeout))
    if p.is_alive():
        p.terminate()
        return False

    return queue.get()


def get_tenant_info(tenant_id):
    #first get the the tenant obj

    client = client_conn('keystone')
    manager_id = pre_check(client, "tm_role", TENANT_MANAGER)
    member_id = pre_check(client, "m_role", MEMBER)
    user_manager = []
    user_member = []
    tenant = client.tenants.find(id=tenant_id)
    user_data = tenant.list_users()

    manager = [u for u in user_data for r in
               client.roles.roles_for_user(u, tenant_id)
               if r.id == manager_id]
    member = [u for u in user_data for r in
              client.roles.roles_for_user(u, tenant_id)
              if r.id == member_id]
    for m in manager:
        user_manager.append(str(m.name))
    for e in member:
        user_member.append(str(e.name))

    tenant_info = {'Tenant Name:': tenant.name,
                   'Tenant ID:': tenant.id,
                   'Tenant Manager:': ' '.join(user_manager),
                   'Tenant Member:': ' '.join(user_member)}

    return tenant_info


def count_num_vms(client, tenant_id):
    today_year = datetime.datetime.now().strftime("%Y")
    today_month = datetime.datetime.now().strftime("%m")
    today_day = datetime.datetime.now().strftime("%d")
    END_DATE = date(int(today_year), int(today_month), int(today_day))
    now = datetime.datetime.utcnow()
    END = now + datetime.timedelta(days=1)
    START = now - datetime.timedelta(days=(END_DATE - START_DATE).days)

    data_report = client.usage.get(tenant_id, START, END).server_usages
    return len(data_report)


def print_pretty(data, wrap=0, dict_property=None, val=None):
    if dict_property is None:
        dict_property = 'Property'
    if val is None:
        val = 'Value'
    pt = prettytable.PrettyTable([dict_property, val], caching=False)
    pt.align = 'l'
    for k, v in sorted(data.iteritems()):
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
    print pt.get_string()
    #print pt.get_html_string()


def print_text(data):
    print "Tenant Created"
    print "\n"
    for k, v in sorted(data.iteritems()):

        print k, v
        
    print "\n"
    print "Congratulations on obtaining NeCTAR Research Cloud resources for your project."
    print "For hints on the next steps to access these resources, add users and launch VMs, please visit"
    print "https://support.rc.nectar.org.au/wiki/AllocationsGettingStarted:_Allocations_GettingStarted" 

