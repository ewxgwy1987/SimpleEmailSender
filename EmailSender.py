#Read message content from message.txt
#Read email addresses from EmailAddresses.txt
import io
import os
import sys
import logging
import platform
import time
import smtplib
from email.mime.text import MIMEText

if platform.platform().startswith('Windows'):
    logging_file = os.path.join(os.getenv('PALS_LOG'),'EmailSender.log')
	
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s : %(levelname)s : %(message)s',
    filename = logging_file,
    filemode = 'a',
)

FILE_MSG = 'message.txt'
FILE_EMAILADDRESS = 'EmailAddresses.txt'

SMTP_SERVER = 'smtp.163.com'
Email_USR = 'ewxgwy1987'
Email_PWD = '21-ewxgwy'
Email_From = 'ewxgwy1987@163.com'

try:
	f_msg = open(FILE_MSG,'rt')
	msg = MIMEText(f_msg.read(), 'plain', 'utf-8')

	Email_ToList = []
	f_EmailAddr = open(FILE_EMAILADDRESS,'rt')
	tempaddr = f_EmailAddr.readline().strip().strip('\n')
	while len(tempaddr) > 0:
		Email_ToList.append(tempaddr)
		tempaddr = f_EmailAddr.readline().strip().strip('\n')

	delimiter = ','
	msg['Subject'] = 'The SVN Email of %s' % FILE_MSG
	msg['From'] = Email_From
	msg['To'] = delimiter.join(Email_ToList)
	msg['Cc'] = 'ewxgwy1987@163.com'

	sender = smtplib.SMTP(SMTP_SERVER)

	islogin = sender.login(Email_USR,Email_PWD)
	
	result = sender.sendmail(Email_From, Email_ToList, msg.as_string())
	
	if(len(result) > 0):
		logging.error(str(result))
	
except Exception as exp:
	logging.exception(str(exp))
finally:
	if f_msg:
		f_msg.close()
		
	if f_EmailAddr:
		f_EmailAddr.close()
		
	if sender:
		sender.quit()

#time.sleep(10)
# cmd /K cd /D $(CURRENT_DIRECTORY) & python -i "$(FULL_CURRENT_PATH)"