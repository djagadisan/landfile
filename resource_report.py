import sys
import time
import smtplib
import email
import os
import mimetypes
import sys
import random
import string
import unicodedata
import time
import re
import novaaction
import datetime
import locale
import collections
from util import GetConfig
from novaaction import NovaAction
from novaclient.v1_1 import client
from novaclient.exceptions import *
from config_data import GetVar
from random import randint
from email.MIMEMultipart import MIMEMultipart
from email.Utils import COMMASPACE
from email.MIMEBase import MIMEBase
from email.parser import Parser
from email.MIMEText import MIMEText
from email import Encoders
from ConfigParser import SafeConfigParser



parser = SafeConfigParser()
config_file='/home/deven/scripts/config.ini'
parser.read(config_file)


def set_email(user,password,smtp_server,smtp_port):
    conn = smtplib.SMTP()
    conn.connect(smtp_server,smtp_port)
    conn.ehlo()
    conn.starttls()
    conn.login(user,password)

    return conn

def process_config(section,option):
    for section_name in parser.sections():
        try:
            if section_name == section:
                list_items = parser.get(section_name,option)
        except:
            list_items=None
    return list_items

def get_ordinal(num):
    ldig = num % 10
    l2dig = (num // 10) % 10

    if (l2dig == 1) or (ldig > 3) or (num == 20) or (num ==30):
        return '%d%s' % (num, 'th')
    else:
        return '%d%s' % (num, {1: 'st', 2: 'nd', 3: 'rd'}.get(ldig))



alloc='/tmp/allocation.csv'
user=process_config('email_server','user')
password = process_config('email_server','password')
smtp_server = process_config('email_server','server')
smtp_port = process_config('email_server','port')
now = datetime.datetime.now()
date_gen = now.strftime("%d%m%Y")
file_w = "log_gen-%s.log"%date_gen
current_day = get_ordinal(int(now.strftime("%d")))
current_mth = now.strftime("%b")
current_year = now.strftime("%Y")
data_t = ''
f = open(file_w, 'w')



f.writelines("<HTML> <BODY>")
#_return_np = read_types_value(vm_types,1,data_vm_np)
f.writelines( "<font face=\"Arial\" size=\"2\"><b>-- NeCTAR Research Cloud, Melbourne Node, Noble Park Cell --</b></font><br>")
f.writelines( "<font face=\"Arial\" size=\"2\"><b>-- Resource Usage update as at: %s --</b></font><br>" % data_t.join(data_np[0]))
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Total available nodes, cores and memory:</b> %s nodes, %s cores, %d GB </font><br>" %  (data_t.join(data_np[1]),data_t.join(data_np[2]),(int(data_t.join(data_np[5]))/1024)))
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Used cores and memory:</b> %s cores, %s GB </font><br>" % (data_t.join(data_np[3]),(int(data_t.join(data_np[6]))/1024)))
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Free cores and memory:</b> %s cores, %s GB </font><br>" % (data_t.join(data_np[4]),(int(data_t.join(data_np[7]))/1024)))
f.writelines( "<font face=\"Arial\" size=\"2\"><b>VM sizes in use (s, m, l, xl, xxl):</b> %s, %s, %s, %s, %s</font><br>" % (_return_np[2], _return_np[1], _return_np[0], _return_np[3], _return_np[4]))

f.writelines("<br>")
f.writelines("<br>")

#_return_qh2 = read_types_value(vm_types,1,data_vm_qh2)
f.writelines( "<font face=\"Arial\" size=\"2\"><b>-- NeCTAR Research Cloud, Melbourne Node, Parkville Cell --</b></font><br>")
f.writelines( "<font face=\"Arial\" size=\"2\"><b>-- Resource Usage update as at: %s --</b></font><br>" % data_t.join(data_qh2[0]))
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Total available nodes, cores and memory:</b> %s nodes, %s cores, %s GB </font><br>" %  (data_t.join(data_qh2[1]),data_t.join(data_qh2[2]),(int(data_t.join(data_qh2[5]))/1024)))
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Used cores and memory:</b> %s cores, %s GB</font><br>" % (data_t.join(data_qh2[3]),(int(data_t.join(data_qh2[6]))/1024)))
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Free cores and memory:</b> %s cores, %s GB</font><br>" % (data_t.join(data_qh2[4]),(int(data_t.join(data_qh2[7]))/1024)))
f.writelines( "<font face=\"Arial\" size=\"2\"><b>VM sizes in use (s, m, l, xl, xxl):</b> %s, %s, %s, %s, %s</font><br>" % (_return_qh2[2], _return_qh2[1], _return_qh2[0], _return_qh2[3], _return_qh2[4]))

f.writelines("<br>")
f.writelines("<br>")

f.writelines( "<font face=\"Arial\" size=\"2\"><b>Total VM sizes in use <b></font><br>")
#get_total = read_types_value(vm_types,0,data_vm_np,data_vm_qh2)
f.writelines( "<font face=\"Arial\" size=\"2\"><b>VM sizes in use (s, m, l, xl, xxl):</b> %s, %s, %s, %s, %s</font><br>" % (get_total[2],get_total[1],get_total[0],get_total[3],get_total[4]))
f.writelines("</BODY> <HTML>")

f.close()


#Email Part

msg = MIMEMultipart()
server = set_email(smtp_server,smtp_port)


fromaddr = "support@rc.nectar.org.au"
toaddr = process_config('email_user','emailaddr')
toaddr = toaddr.split(',')
sub = 'NeCTAR Infrastructure Resource usage as %s %s, %s'% (current_day,current_mth,current_year)

msg['From'] = fromaddr
msg['To'] = ",".join(toaddr)
msg['Subject'] = sub
f = open(file_w,'r')
html_data = [i for i in f]
body = data_t.join(html_data)

if os.path.exists(alloc):
    part = MIMEBase('application',"octet-stream")
    part.set_payload(open(alloc,"rb").read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition','attachment; filename="%s"' %os.path.basename(alloc))
    msg.attach(part)
#    msg.attach(MIMEText(body, 'plain'))
    msg.attach(MIMEText(body,'html'))
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr,text)
    server.quit()
else:
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr,text)
    server.quit()
    
#remove all files from temp



