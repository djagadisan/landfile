import csv
import time
import smtplib
import mimetypes
import datetime
from email.MIMEMultipart import MIMEMultipart
from email.Utils import COMMASPACE
from email.MIMEBase import MIMEBase
from email.parser import Parser
from email.MIMEText import MIMEText
from email import Encoders


def get_ordinal(num):
    ldig = num % 10
    l2dig = (num // 10) % 10
    if (l2dig == 1) or (ldig > 3) or (num == 20) or (num ==30):
        return '%d%s' % (num, 'th')
    else:
        return '%d%s' % (num, {1: 'st', 2: 'nd', 3: 'rd'}.get(ldig))

                                    


now = datetime.datetime.now()
date_gen = now.strftime("%d%m%Y")
file_w = "log_gen-%s.log"%date_gen
current_day = get_ordinal(int(now.strftime("%d")))
current_mth = now.strftime("%b")
current_year = now.strftime("%Y")
date_paste = (current_day + current_mth + current_year)

f = open(file_w,'w')

f.writelines("<HTML> <BODY>")

f.writelines( "<font face=\"Arial\" size=\"2\"><b>-- NeCTAR Research Cloud Usage Report --</b></font><br>")

f.writelines("<br>")
f.writelines("<br>")

f.writelines( "<font face=\"Arial\" size=\"2\"><b>NeCTAR Research Cloud,Melbourne Node,Noble Park Cell</b></font><br>")
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Resource Usage update as at:</b> %s</font><br>" % date_paste)
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Total available nodes, cores and memory:</b> 80 nodes, 1920 cores, 10090 GB</font><br>" )
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Used cores and memory:</font> 1386 cores, 5584 GB</font><br>")
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Free cores and memory:</b> 534 cores, 4506 GB</font><br>")
f.writelines( "<font face=\"Arial\" size=\"2\"><b>VM sizes in use (s, m, l, xl, xxl):</b> 388, 159, 2, 26, 29</font><br>")

f.writelines("<br>")
f.writelines("<br>")

f.writelines( "<font face=\"Arial\" size=\"2\"><b>NeCTAR Research Cloud,Melbourne Node,Parkville Cell</b></font><br>")
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Resource Usage update as at:</b> %s</font><br>"%date_paste)
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Total available nodes, cores and memory:</b> 80 nodes, 1920 cores, 10073 GB</font><br>")
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Used cores and memory:</b> 1370 cores, 5520 GB</font><br>")
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Free cores and memory:</b> 550 cores, 4553 GB</font><br>")
f.writelines( "<font face=\"Arial\" size=\"2\"><b>VM sizes in use (s, m, l, xl, xxl):</b> 426, 188, 10, 26, 20</font><br>")

f.writelines("<br>")
f.writelines("<br>")


f.writelines( "<font face=\"Arial\" size=\"2\"><b>NeCTAR Research Cloud,Monash Node,Monash-01 Cell</b></font><br>")
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Resource Usage update as at:</b> %s</font><br>"%date_paste)
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Total available nodes, cores and memory:</b> %s nodes, %s cores, %d GB</font><br>"
                                                                                        %(len(np_cell_nodes),np_stats.get('nac'),
                                                                                          np_stats.get('nam')
                                                                                          )
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Used cores and memory:</b> 779 cores, 3133 GB</font><br>")
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Free cores and memory:</b> 901 cores, 3478 GB</font><br>")
f.writelines( "<font face=\"Arial\" size=\"2\"><b>VM sizes in use (s, m, l, xl, xxl):</b> 67, 24, 8, 10, 7</font><br>")

f.writelines("<br>")
f.writelines("<br>")

f.writelines( "<font face=\"Arial\" size=\"2\"><b>NeCTAR Research Cloud,Queensland Node,QLD Cell</b></font><br>")
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Resource Usage update as at:</b> %s</font><br>"%date_paste)
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Total available nodes, cores and memory:</b> 8 nodes, 512 cores, 2015 GB</font><br>")
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Used cores and memory:</b> 339 cores, 1360 GB</font><br>")
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Free cores and memory:</b> 173 cores, 655 GB</font><br>")
f.writelines( "<font face=\"Arial\" size=\"2\"><b>VM sizes in use (s, m, l, xl, xxl):</b> 189, 25, 13, 13, 22</font><br>")

f.writelines("<br>")
f.writelines("<br>")

f.writelines( "<font face=\"Arial\" size=\"2\"><b>Total Resources Research Cloud</b></font><br>")
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Resource Usage update as at:</b> %s</font><br>"%date_paste)
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Total available nodes, cores and memory:</b> 203 nodes, 6032 cores, 28789 GB</font><br>")
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Used cores and memory:</b> 3874 cores, 15597 GB</font><br>")
f.writelines( "<font face=\"Arial\" size=\"2\"><b>Free cores and memory:</b> 2158 cores, 13192 GB</font><br>")
f.writelines( "<font face=\"Arial\" size=\"2\"><b>VM sizes in use (s, m, l, xl, xxl):</b> 1070, 396, 33, 75, 78</font><br>")

f.writelines("<br>")
f.writelines("<br>")

f.writelines( "<font face=\"Arial\" size=\"2\"><i>Allocation data will be added on the 22/07/2013</i><br>")

f.writelines("</BODY> <HTML>")

f.close


