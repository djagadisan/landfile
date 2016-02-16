#!/usr/bin/env python
import re
import time
from alloc_write_to_csv import WriteCSV
from ConfigParser import SafeConfigParser
from keystoneclient.v2_0 import client as ckeystone
from novaclient.v1_1 import client as cnova
from cinderclient.v2 import client as ccinder
from keystoneclient.exceptions import ClientException, Unauthorized
from novaclient.exceptions import ClientException, Unauthorized
from cinderclient.exceptions import ClientException, Unauthorized
import keystoneclient


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


def clientKeystone(username, passwd, tname, a_url):
    try:
        keystone = ckeystone.Client(username=username,
                                     password=passwd,
                                     tenant_name=tname,
                                     auth_url=a_url)

    except ClientException, e:
        return "Error %s" % e
    return keystone


def clientNova(username, passwd, tname, a_url):
    try:
        nova = cnova.Client(username=username,
                            api_key=passwd,
                            project_id=tname,
                            auth_url=a_url)

    except ClientException, e:
        return "Error %s" % e
    return nova


def clientCinder(username, passwd, tname, a_url):
    try:
        conn = ccinder.Client(username=username,
                              api_key=passwd,
                              project_id=tname,
                              auth_url=a_url,
                              service_type='volume')

    except ClientException, e:
            return "Error %s" % e

    return conn


def getTenant(tenant):
    search_tenant = re.compile(r'pt-')
    personal_tenant, alloc_tenant = ([] for i in range(2))

    for i in tenant:
        if search_tenant.search(i.name):
            personal_tenant.append(i)
        else:
            alloc_tenant.append(i)

    return {'pt': personal_tenant, 'at': alloc_tenant}


def filterTenant(tenant, tenant_id):
        tenant_aid = []
        for i in tenant:
            tenant_aid.append(i.id)

        tenant_t = set(tenant_aid)
        return tenant_t.difference(tenant_id)


def getTenantName(tenant, ids):

        get_Tenant_detail = []

        for i in tenant:
            if i.id == unicode(ids):
                get_Tenant_detail.append(i.name)
        return get_Tenant_detail


def getUserFromTenant(tenant, tenant_id):
        user_id = []
        for i in tenant:
            if i.id == tenant_id:
                data = RequestRetries('guft', i)

        for u in data:
            user_id.append(u.id)

        return user_id


def getUserRoleManager(u_frmT, ksclient, tenant_id, tm_id):
        user_id = ''
        for u in u_frmT:
            #data = ksclient.roles.roles_for_user(u, tenant_id)
            data = RequestRetries('gurm', ksclient, [u, tenant_id])
            for i in data:
                if i.id == tm_id:
                    user_id = u

        return user_id


def getUserInfo(user_id, ksclient):
        if user_id:
            #get_user = ksclient.users.get(user_id)._info
            get_user = RequestRetries('guiu', ksclient, user_id)

            if 'tenantId'in get_user:
                #tenant_name = ksclient.tenants.get(get_user.get('tenantId'))
                tenant_name = RequestRetries('gui', ksclient, [get_user,
                                                               'tenantId'])
            else:
                #tenant_name = ksclient.tenants.get(get_user.get('tenant_id'))
                tenant_name = RequestRetries('gui', ksclient, [get_user,
                                                               'tenant_id'])

            name = tenant_name.description.split("'")[0]
            email = get_user.get('email')
            return {'name': name, 'email': email}
        else:
            return {'name': 'NA', 'email': 'NA'}


def RequestRetries(meth, client=None, *args):
    attempt = processConfig('config', 'retries')

    for x in xrange(int(attempt)):
        try:

            if meth == 'gurm':
                return client.roles.roles_for_user(args[0][0], args[0][1])
                break
            elif meth == 'gui':
                return client.tenants.get(args[0][0].get(args[0][1]))
                break
            elif meth == 'guft':
                return client.list_users()
            elif meth == 'guiu':
                return client.users.get(args[0])._info
        except keystoneclient.exceptions.Unauthorized:
            time.sleep(5)

    return False


unwanted = processConfig('tenant', 'id').split(',')
csv_temp = processConfig('csv', 'file')
username = processConfig('cred', 'user')
passwd = processConfig('cred', 'passwd')
tname = processConfig('cred', 'name')
a_url = processConfig('cred', 'url')
tm = processConfig('role', 'tm')

start_time = time.time()
print "Process Started"
ksclient = clientKeystone(username, passwd, tname, a_url)
nclient = clientNova(username, passwd, tname, a_url)
cclient = clientCinder(username, passwd, tname, a_url)

tenant_list = ksclient.tenants.list()
writer_ = WriteCSV()
alloc_tenant = getTenant(tenant_list).get('at')
getTenantID = filterTenant(alloc_tenant, unwanted)


for i in getTenantID:

    tenant_name = "".join(getTenantName(tenant_list, i))
    user = getUserFromTenant(tenant_list, i)
    manager_id = getUserRoleManager(user, ksclient, i, tm)
    cores = nclient.quotas.get(i).cores
    volumes = cclient.quotas.get(i).volumes
    manager_details = getUserInfo(manager_id, ksclient)
    data_insert = [tenant_name, cores,volumes,
                   manager_id, manager_details.get('name'),
                   manager_details.get('email'),
                   len(user)]

    WriteCSV().createCSVFile(csv_temp, data_insert)

print "Process finished, took  %0.2f seconds to complete" % (
                                                    time.time() - start_time)
