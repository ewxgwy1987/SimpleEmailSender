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
from EmailXConfig import XConfig

#There are 4 arguments for this program
#The first one is the author who commits the new version to SVN
#The second one is the repository path
#The third one is the revision 
#The forth one is the root path of this program for current repository
if(len(sys.argv)!=5):
	print 'The command must have 4 arguments'
	print str(sys.argv)
	exit(1)
	
# print sys.argv
	
SVN_author = sys.argv[1]
tmp_repos = sys.argv[2]
SVN_repos = tmp_repos[tmp_repos.rfind(os.sep)+1:]
SVN_rev = sys.argv[3]
RootPath = sys.argv[4]

if(len(SVN_author)<=0):
	print 'The fisrt argument(author) is empty'
	exit(1)
if(len(SVN_repos)<=0):
	print 'The second argument(SVN Repository) is empty'
	exit(1)
if(len(SVN_rev)<=0):
	print 'The third argument(SVN Revision) is empty'
	exit(1)
if(len(RootPath)<=0):
	print 'The forth argument(RootPath) is empty'
	exit(1)

#Get configuration from xml file
_xcfg= XConfig(RootPath)
_xcfg.GetConfig()

if _xcfg.isAllConfigOK:
	try:
		UsrExists = False
		filepath = os.path.join(RootPath, _xcfg.PathFileMSG)
		f_msg = open(filepath, 'rb')
		msg = MIMEText(f_msg.read(),'plain','us-ascii')

		EmailSubject = '{}(Author:{}, Repository:{}, Revision:{})'.format(	
			_xcfg.DefaultEmailSubject,
			SVN_author,
			SVN_repos,
			SVN_rev
		)
		_xcfg.log.debug('Email Subject: {}'.format(EmailSubject))
		
		msg['Subject'] = EmailSubject
		msg['From'] = _xcfg.EmailFrom
		# msg['Cc'] = 'ewxgwy1987@163.com'
		
		sender = smtplib.SMTP(_xcfg.SMTPServerName)
		# sender.set_debuglevel(1)

		# If the author is in one Email Group, then send emails to all users in this group
		delimiter = ', '
		for group,  usr_list in _xcfg.EmailToList_UsrGroup.items():
			if SVN_author in usr_list:
				
				if not UsrExists:
					UsrExists = True
				
				EmailList = _xcfg.EmailToList_EmailGroup[group]
				msg['To'] = delimiter.join(EmailList)
				
				try:
					islogin = sender.login(_xcfg.SMTPServerUsr, _xcfg.SMTPServerPwd)
					result = sender.sendmail(
						_xcfg.EmailFrom, 
						EmailList,
						msg.as_string()
					)
					
					_xcfg.log.info("Send Email({0}) to: {1}".format(EmailSubject, str(EmailList)))
					if(len(result) > 0):
						_xcfg.log.error(str(result))
						
				except Exception as exp:
					_xcfg.log.error('Sending Email is failed. To: {}'.format(str(EmailList))) 
					_xcfg.log.exception(str(exp)) 
		
		if not UsrExists:
			_xcfg.log.error('Author {} cannot be found in any groups'.format(SVN_author)) 
		sender.quit()

	except Exception as exp:
		_xcfg.log.exception(str(exp))
	finally:
		if f_msg:
			f_msg.close()
		
# if __name__=='__main__':
	# raw_input("Press any key to continue")

#time.sleep(10)
# cmd /K cd /D $(CURRENT_DIRECTORY) & python -i "$(FULL_CURRENT_PATH)"