import sys
import datetime
import time
import smtplib
import email
import os
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.Utils import COMMASPACE
from email.MIMEBase import MIMEBase
from email.parser import Parser
from email.MIMEText import MIMEText
from email import Encoders
from ConfigParser import SafeConfigParser


class SendEmail():

    def process_config(self, section, option):
        parser = SafeConfigParser()
        working_path = os.getcwd()
        #config_file = working_path + "/" + "email.ini"
        config_file = "/home/deven/workspace/tripping-octo-wight/tripping-octo-wight/email.ini"
        parser.read(config_file)
        for section_name in parser.sections():
            try:
                if section_name == section:
                    list_items = parser.get(section_name, option)
            except:
                list_items = None

        return list_items

    def email_user(self, email_file, attach):

        smtp_server = self.process_config('email_server', 'server')
        smtp_port = self.process_config('email_server', 'port')
        fromaddr = self.process_config('email_server', 'from')
        rec_user = self.process_config('email_user', 'emailaddr')

        msg = MIMEMultipart()

        server = smtplib.SMTP(smtp_server, smtp_port)
        rec_user = rec_user.split(',')

        sub = 'NeCTAR Infrastructure Resource usage'

        msg['From'] = fromaddr
        msg['To'] = ",".join(rec_user)
        msg['Subject'] = sub
        f = open(email_file, 'r')
        html_data = [i for i in f]
        body = "".join(html_data)

        if os.path.exists(attach):
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(attach, "rb").read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"'
                                                    % os.path.basename(attach))
            msg.attach(part)
            msg.attach(MIMEText(body, 'html'))
            text = msg.as_string()
            server.sendmail(fromaddr, rec_user, text)
            server.quit()
        else:
            msg.attach(MIMEText(body, 'html'))
            text = msg.as_string()
            server.sendmail(fromaddr, rec_user, text)
            server.quit()
