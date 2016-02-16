import sys
import os
import time
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

HOST_ON='qh2-rcc30'
HOST_OFF='qh2-rcc29'
VM_MIGRATE = []
#live_migrate
client = client_nova.Client(username=AUTH_USER,
                            insecure=True,
                            api_key=AUTH_PASSWORD,
                            project_id=AUTH_TENANT_NAME,
                            auth_url=AUTH_URL,
                            region_name=AUTH_REGION)

search_opts = {'all_tenants': 1, 'host': HOST_ON}

servers = client.servers.list(search_opts=search_opts)
for i in servers:
    print "Migrating instances %r to %s" % (i, HOST_OFF) 
    i.live_migrate(HOST_OFF)
    time.sleep(30)

