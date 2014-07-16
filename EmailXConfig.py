import io
import os
import sys
import logging
import platform
import xml.etree.ElementTree as XET

class XConfig:
	"""Get XML configuration For EmailSender"""
	
	XMLConfigPath = 'EmailSenderConfig.xml'
	
	# All XPath element in xml file
	_xroot = 'EmailSenderConfig'
	
	_xelem1_LogFileName = 'LogFileName' 
	_xelem1_PathFileMSG = 'PathFileMSG' 
	
	_xelem1_EmailConfig = 'EmailConfig'
	_xelem2_EmailFrom = 'EmailFrom' 
	_xelem2_EmailToList = 'EmailToList'
	_xelem3_EmailTo = 'EmailTo'
	_xelem2_DefaultEmailSubject = 'EmailSubject_Default'
	
	_xelem1_SMTPServer = 'SMTPServer'
	_xelem2_SMTPServerName = 'ServerName'
	_xelem2_SMTPServerUsr = 'ServerUser'
	_xelem2_SMTPServerPwd = 'ServerPassword'
	_xelem2_SMTPServerPort = 'EmailPort'
	_xelem2_SMTPServerSSL = 'EnableSSL'
	
	def __init__(self):
		"""Initializes the attribute XConfig"""
		self.LogFileName = ''
		self.PathFileMSG = ''
		self.EmailFrom = ''
		self.EmailToList = []
		self.EmailSubject = ''
		self.SMTPServerName = ''
		self.SMTPServerUsr = ''
		self.SMTPServerPwd = ''
		self.SMTPServerPort = 0
		self.SMTPServerSSL = False
		
	def GetConfig(self):
		"""Get All configuration set from xml file"""
		xtree = XET.parse(XConfig.XMLConfigPath)
		xroot = xtree.getroot()
			
		#Get LogFileName
		xpath = "./{}".format(XConfig._xelem1_LogFileName)
		self.LogFileName = xroot.findall(xpath)[0].text
		print "LogFileName:	" + self.LogFileName
		
		#Get PathFileMSG
		xpath = "./{}".format(XConfig._xelem1_PathFileMSG)
		self.PathFileMSG = xroot.findall(xpath)[0].text
		print "PathFileMSG:	" + self.PathFileMSG
		
		#Get EmailFrom
		xpath = "./{}/{}".format(XConfig._xelem1_EmailConfig, XConfig._xelem2_EmailFrom)
		self.EmailFrom = xroot.findall(xpath)[0].text
		print "EmailFrom:	" + self.EmailFrom
		
		#Get EmailToList
		xpath = "./{}/{}/{}".format(XConfig._xelem1_EmailConfig, XConfig._xelem2_EmailToList, XConfig._xelem3_EmailTo)
		for xelem in xroot.findall(xpath):
			self.EmailToList.append(xelem.text)
		print "EmailToList:	"
		print self.EmailToList
		
		#Get EmailSubject
		xpath = "./{}/{}".format(XConfig._xelem1_EmailConfig, XConfig._xelem2_DefaultEmailSubject)
		self.EmailSubject = xroot.findall(xpath)[0].text
		print "EmailSubject:	" + self.EmailSubject
		
		#Get SMTPServerName
		xpath = "./{}/{}".format(XConfig._xelem1_SMTPServer, XConfig._xelem2_SMTPServerName)
		self.SMTPServerName = xroot.findall(xpath)[0].text
		print "SMTPServerName:	" + self.SMTPServerName
		
		#Get SMTPServerUsr
		xpath = "./{}/{}".format(XConfig._xelem1_SMTPServer, XConfig._xelem2_SMTPServerUsr)
		self.SMTPServerUsr = xroot.findall(xpath)[0].text
		print "SMTPServerUsr:	" + self.SMTPServerUsr
		
		#Get SMTPServerPwd
		xpath = "./{}/{}".format(XConfig._xelem1_SMTPServer, XConfig._xelem2_SMTPServerPwd)
		self.SMTPServerPwd = xroot.findall(xpath)[0].text
		print "SMTPServerPwd:	" + self.SMTPServerPwd
		
		#Get SMTPServerPort
		xpath = "./{}/{}".format(XConfig._xelem1_SMTPServer, XConfig._xelem2_SMTPServerPort)
		self.SMTPServerPort = xroot.findall(xpath)[0].text
		print "SMTPServerPort:	" + self.SMTPServerPort
		
		#Get SMTPServerSSL 
		xpath = "./{}/{}".format(XConfig._xelem1_SMTPServer, XConfig._xelem2_SMTPServerSSL)
		self.SMTPServerSSL = xroot.findall(xpath)[0].text
		print "SMTPServerSSL:	" + self.SMTPServerSSL
		
		
if __name__=='__main__':
	myconfig = XConfig()
	myconfig.GetConfig()
	raw_input("Press any key to continue")