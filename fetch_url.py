import urllib2
import time

hosts = ["http://www.yahoo.com", "http://www.google.com", "http://www.amazon.com",
         "http://www.ibm.com" , "http://www.apple.com"]

start = time.time()
#grabs urls of hosts and prints first 1024 bytes of page
for host in hosts:
    url = urllib2.urlopen(host)
    print url.read(1024)

print "Elasped Time; %s" % (time.time() - start)


