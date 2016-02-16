import os
import textwrap
import prettytable
import time
import re
from prettytable import PrettyTable


def printPretty2(data, dict_property="Property", wrap=0):

    startTime = time.time()

    time.sleep(5)

    pt = prettytable.PrettyTable([dict_property, 'Value'], caching=False)
    pt.align = 'l'
    pt.max_width[dict_property] = 40
    pt.add_row(['Total Nodes', data.get('total_nodes')])
    str =  data.get('used_cores')  +  ", "  +  data.get('used_mem')
    pt.add_row(['Used cores and memory in size dfdsfsdfsdfsdfs ', str])


    print pt.get_string()
    print "Took %0.2f secs" %(time.time() - startTime)

data = {'oth': 9, 'total_xl': 96, 'total_cores': '5936',
        'used_mem': '22085', 'total_nodes': '201', 'used_cores': '4258', 
        'total_medium':'424', 'total_large': '51', 'free_cores': '1678',
        'free_mem': '6326', 'total_mem': '28411', 'total_xxl': 86, 'total_small': '1083'}



char_ = 'nectar!melbourne!qh2@oldkernel'
find_ = 'oldkernel'

stro = r''
print char_

if re.search(stro + find_ + stro, char_, flags=re.IGNORECASE):
    print find_
else:
    print "Not Found"

#printPretty2(data, dict_property="Property", wrap=50)
