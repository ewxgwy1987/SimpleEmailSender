import io
import os
import sys
import logging
import platform
import time
import xml.etree.ElementTree as XET

class XConfig:
	"""Get XML configuration For EmailSender"""
	
	XMLConfigPath = 'EmailSenderConfig.xml'
	
	# All XPath element in xml file
	_xroot = 'EmailSenderConfig'
	
	_xelem1_LogFileName = 'LogFileName' 
	_xelem1_PathFileMSG = 'PathFileMSG' 
	
	_xelem1_EmailConfig = 'EmailConfig'
	_xelem2_EmailEnable = 'EmailEnable'
	_xelem2_EmailFrom = 'EmailFrom' 
	_xelem2_EmailToList = 'EmailToList'
	_xelem3_EmailTo = 'EmailTo'
	_xelem4_User = 'User'
	_xelem4_Email = 'Email'
	_xelem2_DefaultEmailSubject = 'EmailSubject_Default'
	
	_xattb_EmailToList = 'group'
	
	_xelem1_SMTPServer = 'SMTPServer'
	_xelem2_SMTPServerName = 'ServerName'
	_xelem2_SMTPServerUsr = 'ServerUser'
	_xelem2_SMTPServerPwd = 'ServerPassword'
	_xelem2_SMTPServerPort = 'EmailPort'
	_xelem2_SMTPServerSSL = 'EnableSSL'
	
	def __init__(self, rootpath):
		"""Initializes the attribute XConfig"""
		XConfig.XMLConfigPath = os.path.join(rootpath, XConfig.XMLConfigPath)
		
		self.LogFileName = 'EmailSender.log' # default value
		self.PathFileMSG = ''
		self.EmailEnable = False
		self.EmailFrom = ''
		self.EmailToList_UsrGroup= {} #dictionary
		self.EmailToList_EmailGroup= {} #dictionary
		self.DefaultEmailSubject = ''
		self.SMTPServerName = ''
		self.SMTPServerUsr = ''
		self.SMTPServerPwd = ''
		self.SMTPServerPort = 0
		self.SMTPServerSSL = False
		self.isAllConfigOK = False
		
		# if platform.platform().startswith('Windows'):
			# logging_file = os.path.join(os.getenv('PALS_LOG'),self.LogFileName)
	
		# logging.basicConfig(
			# level=logging.DEBUG,
			# format='%(asctime)s : %(levelname)s : %(message)s',
			# filename = logging_file,
			# filemode = 'a',
		# )
		
		# self.log = logging.getLogger()
		
	def GetConfig(self):
		"""Get All configuration set from xml file"""
		
		try:
			xtree = XET.parse(XConfig.XMLConfigPath)
			xroot = xtree.getroot()
				
			#Get LogFileName
			xpath = "./{}".format(XConfig._xelem1_LogFileName)
			self.LogFileName = xroot.findall(xpath)[0].text
			# print "LogFileName:	" + self.LogFileName
			
			#Re-Initialize the logging
			# if platform.platform().startswith('Windows'):
				# logging_file = os.path.join(os.getenv('PALS_LOG'),self.LogFileName)
	
			logging.basicConfig(
				level=logging.DEBUG,
				format='%(asctime)s : %(levelname)s : %(message)s',
				filename = self.LogFileName,
				filemode = 'a',
			)
			self.log = logging.getLogger()
			
			#Get PathFileMSG
			xpath = "./{}".format(XConfig._xelem1_PathFileMSG)
			self.PathFileMSG = xroot.findall(xpath)[0].text
			# print "PathFileMSG:	" + self.PathFileMSG
			
			#Get EmailEnable
			xpath = "./{}/{}".format(XConfig._xelem1_EmailConfig, XConfig._xelem2_EmailEnable)
			if xroot.findall(xpath)[0].text.lower() == 'true':
				self.EmailEnable = True
			else:
				self.EmailEnable = False
			print "EmailEnable:	" + str(self.EmailEnable)
			
			#Get EmailFrom
			xpath = "./{}/{}".format(XConfig._xelem1_EmailConfig, XConfig._xelem2_EmailFrom)
			self.EmailFrom = xroot.findall(xpath)[0].text
			# print "EmailFrom:	" + self.EmailFrom
			
			#Get EmailToList Group
			xpath = "./{}/{}".format(XConfig._xelem1_EmailConfig, XConfig._xelem2_EmailToList)
			for xelem in xroot.findall(xpath):
				group = xelem.attrib[XConfig._xattb_EmailToList]
				
				#Get User List
				usr_list = []
				tmp_xpath_usr = "./{}/{}".format(XConfig._xelem3_EmailTo, XConfig._xelem4_User)
				for xelem_usr in xelem.findall(tmp_xpath_usr):
					usr_list.append(xelem_usr.text)
				
				#Get Email List
				email_list = []
				tmp_xpath_email = "./{}/{}".format(XConfig._xelem3_EmailTo, XConfig._xelem4_Email)
				for xelem_email in xelem.findall(tmp_xpath_email):
					email_list.append(xelem_email.text)
					
				self.EmailToList_UsrGroup[group] = usr_list
				self.EmailToList_EmailGroup[group] = email_list

			# print "EmailToList_UsrGroup:	"
			# print self.EmailToList_UsrGroup
			# print "EmailToList_EmailGroup:	"
			# print self.EmailToList_EmailGroup
			
			#Get EmailSubject
			xpath = "./{}/{}".format(XConfig._xelem1_EmailConfig, XConfig._xelem2_DefaultEmailSubject)
			self.DefaultEmailSubject = xroot.findall(xpath)[0].text
			# print "EmailSubject:	" + self.EmailSubject

			#Get SMTPServerName
			xpath = "./{}/{}".format(XConfig._xelem1_SMTPServer, XConfig._xelem2_SMTPServerName)
			self.SMTPServerName = xroot.findall(xpath)[0].text
			# print "SMTPServerName:	" + self.SMTPServerName
			
			#Get SMTPServerUsr
			xpath = "./{}/{}".format(XConfig._xelem1_SMTPServer, XConfig._xelem2_SMTPServerUsr)
			self.SMTPServerUsr = xroot.findall(xpath)[0].text
			# print "SMTPServerUsr:	" + self.SMTPServerUsr
			
			#Get SMTPServerPwd
			xpath = "./{}/{}".format(XConfig._xelem1_SMTPServer, XConfig._xelem2_SMTPServerPwd)
			self.SMTPServerPwd = xroot.findall(xpath)[0].text
			# print "SMTPServerPwd:	" + self.SMTPServerPwd
			
			#Get SMTPServerPort
			xpath = "./{}/{}".format(XConfig._xelem1_SMTPServer, XConfig._xelem2_SMTPServerPort)
			self.SMTPServerPort = xroot.findall(xpath)[0].text
			# print "SMTPServerPort:	" + self.SMTPServerPort
			
			#Get SMTPServerSSL 
			xpath = "./{}/{}".format(XConfig._xelem1_SMTPServer, XConfig._xelem2_SMTPServerSSL)
			if xroot.findall(xpath)[0].text.lower() == 'true':
				self.SMTPServerSSL = True
			else:
				self.SMTPServerSSL = False
			print "SMTPServerSSL:	" + str(self.SMTPServerSSL)
			
			self.isAllConfigOK = True
			
		except Exception as exp:
			print (str(exp))
			self.log.exception(str(exp))
			self.isAllConfigOK = False
		
if __name__=='__main__':
	rootpath = ".\\"
	myconfig = XConfig(rootpath)
	myconfig.GetConfig()
	raw_input("Press any key to continue")
	# exit()