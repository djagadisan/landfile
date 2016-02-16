import smtplib
from smtplib import SMTPException

sender = 'devendran.jagadisan@unimelb.edu.au'
receivers = ['devendran.jagadisan@unimelb.edu.au']

message = """From: Infra Usage Report
To: Deven <devendran.jagadisan@unimelb.edu.au>
Subject: Infra Report Mail Failed

API Issue, unable to generate report.
"""

try:
   smtpObj = smtplib.SMTP('localhost')
   smtpObj.sendmail(sender, receivers, message)         
   print "Successfully sent email"
except SMTPException:
   print "Error: unable to send email"