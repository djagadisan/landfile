from ConfigParser import SafeConfigParser


class GetOptions():

    try:
        config_file = '/tmp/resources.ini'
        with open(config_file):
            parser = SafeConfigParser()
            parser.read(config_file)
    except IOError:
        print "Error!, Config File Not found at (/tmp/resources.ini)"
        raise SystemExit

    def process_config(self, section, option):
        for section_name in self.parser.sections():
            try:
                if section_name == section:
                    list_items = self.parser.get(section_name, option)
            except:
                list_items = None
                return list_items
        return list_items


class GetVar(object):
    def __init__(self):
        func = GetOptions()
        self.username = func.process_config('cred', 'user')
        self.passwd = func.process_config('cred', 'passwd')
        self.name = func.process_config('cred', 'name')
        self.url = func.process_config('cred', 'url')
        self.hyper_name = func.process_config('hypervisor_name', 'name')
        self.zone_name = func.process_config('zone', 'name')
