import os
import sys
import unicodedata
import re
from util import GetConfig
from client_keystone import KeyStoneConnection
from client_nova import NovaConnection
from keystoneclient import utils
from ConfigParser import SafeConfigParser
from config_data import GetVar
from novaaction import NovaAction


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
                data = i.list_users()

        for u in data:
            user_id.append(u.id)

        return user_id


def getUserRoleManager(u_frmT, ksclient, tenant_id, tm_id):
        user_id = ''
        for u in u_frmT:
            data = ksclient.roles.roles_for_user(u, tenant_id)
            for i in data:
                if i.id == tm_id:
                    user_id = u

        return user_id


def getUserInfo(user_id, ksclient):
        if user_id:
            get_user = ksclient.users.get(user_id)._info

            if 'tenantId'in get_user:
                tenant_name = ksclient.tenants.get(get_user.get('tenantId'))
            else:
                tenant_name = ksclient.tenants.get(get_user.get('tenant_id'))

            name = tenant_name.description.split("'")[0]
            email = get_user.get('email')
            return {'name': name, 'email': email}
        else:
            return {'name': 'NA', 'email': 'NA'}




config = GetVar('production')
ks =  KeyStoneConnection()
ns = NovaConnection()
info = GetConfig()
ksclient = ks.createConnection(config)
nclient = ns.createConnection(config)
test_tenant = '752939ab077048d28f4d33002f7409aa'


tenant_list = ksclient.tenants.list()


alloc_tenant = getTenant(tenant_list).get('at')
unwanted = ['1', '10', '11', '11bd70e7f6b74632876322f084f5f1f0', '12',
           '13', '16', '2', '373', '17', '18', '19', '20', '21',
           '2627e1941db3497c93b05e5cb2ca2a02', '28eadf5ad64b42a4929b2fb7df99275c'
           , '2f6f7e75fc0f453d9c127b490b02e9e3', '400', '42', '3',
           '36c4c535b77a4795992b3f907f797929', '3900a1d8667f495d93348fc3d093d206'
           , '5', '7', '8', '9', 'e183df4e2bd045f7a9cbdb37a99929a5',
           'a6cf29e7e30e4749975a18f52cbd7724',
           '6246729dd2e64110ad36877e0640efc9'
           ]

#user_id='2f667b73c2b24d289279dc0cc708b2f8'
#print getUserInfo(user_id, ksclient)


'''
for i in tenant_list:
    if i.id == test_tenant:
        for attr in dir(i):
            print (attr, getattr(i, attr))








role_ = []
print len(data)
    for i in data:
        print i



user_id='03a439e9a2d24df6b10ea1f66930d16b '

#print getRoleManager(user_id, test_tenant, ksclient, tm)

tm='14'

for i in getUserFromTenant(tenant_list, test_tenant):
    print getUserRoleManager(i,ksclient,test_tenant,tm)
    
    
#    print getUserRoleManager(i, ksclient,test_tenant,tm)
    
    #print getUserRoleManager(i.id,test_tenant,ksclient, tm)
    #


'''
tm = '14'


getTenantID = filterTenant(alloc_tenant, unwanted)


for i in getTenantID:
    tenant_name = "".join(getTenantName(tenant_list, i))
    user = getUserFromTenant(tenant_list, i)
    manager_id = getUserRoleManager(user, ksclient, i, tm)
    cores = nclient.quotas.get(i).cores
    manager_details = getUserInfo(manager_id, ksclient) 
    print "Tenant Name: %s, Cores %s,Project Leader ID:%s,Project Leader Name: %s, Project Leader Email: %s, Num of Users: %s" %( 
                                            tenant_name,cores,manager_id,
                                            manager_details.get('name'),manager_details.get('email'),
                                            len(user)
                                            )


'''
role_list = ksclient.roles.list()

for i in role_list:
    print i.id

'''