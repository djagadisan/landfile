import sys
import os
import subprocess
from subprocess import Popen


def main():

    arg1 = '--insecure'
    arg2 = ' --os-tenant-name=admin'
    arg3 = '--os-username=sam'
    arg4 = '--os-password=nectar'
    arg5 = '--os-auth-url=https://keystone.test.rc.nectar.org.au:5000/v2.0/'
     
    p1 = Popen(['swift', '--insecure', '--os-tenant-name=admin', '--os-username=sam', '--os-password=nectar', '--os-auth-url=https://keystone.test.rc.nectar.org.au:5000/v2.0/', 'list']
               ,shell=False, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = p1.communicate()[0].split()
    ob_app = []
    for i in output:
        if i.find('dispersion_')!= -1:
            ob_app.append(i)


    for u in ob_app:
        print u
        p2 = Popen(['swift', '--insecure', '--os-tenant-name=admin', '--os-username=sam', '--os-password=nectar', '--os-auth-url=https://keystone.test.rc.nectar.org.au:5000/v2.0/', 'delete', u]
               ,shell=False, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = p2.communicate()[0].split()
        
if __name__ == '__main__':
    main()
