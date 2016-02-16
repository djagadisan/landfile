from novaclient.v1_1 import client
from novaclient.exceptions import ClientException


class NovaConnection():

    def createConnection(self, obj):
            try:
                conn = client.Client(username=obj.username, api_key=obj.passwd,
                                     project_id=obj.name, auth_url=obj.url)
                return conn
            except ClientException:
                return False
