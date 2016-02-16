from keystoneclient.v2_0 import client


class KeyStoneConnection():

    def createConnection(self, obj):
        try:
            keystone = client.Client(username=obj.username,
                                     password=obj.passwd,
                                     tenant_name=obj.name, auth_url=obj.url)

        except Exception, e:
            return "Error %s" % e
        return keystone
