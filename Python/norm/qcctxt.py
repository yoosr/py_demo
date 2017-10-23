#!/usr/bin/python
# -*- coding:UTF-8 -*-
#Author liusonglin
#20090807
import sys
import os
import time
import datetime
from ftplib import FTP

##################################
#  ���� CLASS ��������           #
##################################		
#���ں���
def getDate():
	today = time.strftime('%Y%m%d')
	return today

#��ù���Ŀ¼����Ч���ļ��б�
def getFileList(dir,workdate):
	filelist = os.listdir(dir)
	newlist =[]
	for tf in filelist:
		if (tf.startswith('QCC') or tf.startswith('qcc')) and (tf.find(workdate)==15) and (len(tf)==27):
			newlist.append(tf)
	#print newlist
	return newlist
#�ֶζ���
class Field:
	def __init__(self,content,len,justdir):
		self.content=content
		self.len=len
		self.justdir=justdir
	def toString(self):
		if self.justdir=='L':
			tmpstr=self.content.ljust(self.len)

		elif self.justdir=='R':
			tmpstr=self.content.rjust(self.len)
		elif self.justdir=='N': #����ֶ�zfill()
			tmpstr=self.content.zfill(self.len)		
		else:
			tmpstr=self.content
		return tmpstr
		
#��¼����
class Record:
	def __init__(self,cardid,amt,trancode,merchid,msgflag):

		self.cardid=cardid
		self.amt=amt
		self.trancode=trancode
		self.MerchId=merchid
		self.CreditCF=msgflag
		#FIX PART
		self.BranchCode=Field('4222208',7,'L')
		self.RecordType=Field('1',1,'L')
		self.SeqNumber=Field('1',8,'N')   #��ű���
		self.TBAmt=Field(' ',15,'L')
		self.DepNum=Field('4220899',10,'L')       #���ļ���ƥ��
		
		#self.CreditCF=Field('0',1,'N')
		self.IdType=Field(' ',1,'L')
		self.IdCode=Field(' ',20,'L')
		self.ApproveCode=Field(' ',6,'L')
		self.RespCode=Field(' ',3,'L')
		self.Desc=Field(' ',40,'L')
		self.Filler=Field(' ',32,'L')

	def toString(self):
		return \
			self.BranchCode.toString()+\
			self.RecordType.toString()+\
			self.SeqNumber.toString()+\
	 		self.cardid.toString()+\
			self.amt.toString()+\
 			self.TBAmt.toString()+\
 			self.DepNum.toString()+\
       		        self.MerchId.toString()+\
			self.trancode.toString()+\
       		        self.CreditCF.toString()+\
       		        self.IdType.toString()+\
       		        self.IdCode.toString()+\
       		        self.ApproveCode.toString()+\
       		        self.RespCode.toString()+\
       		        self.Desc.toString()+\
       		        self.Filler.toString()
		pass

def checkin(instr):

	tstrs=instr.split(',')
	
	if (not len(tstrs)==4) and (not len(tstrs)==5):
		return False
	if not len(tstrs[0])==16 :
		return False
	if not tstrs[0].isdigit():
		return False
	if not tstrs[1].isdigit():
		return False
	if not tstrs[2][:2].isdigit():
		return False
	if (not tstrs[2][:2] == '00') \
		and (not tstrs[2][:2] == '01') \
		and (not tstrs[2][:2] == '02') \
		and (not tstrs[2][:2] == '03') \
		and  (not tstrs[2][:2] == '04'):
		return False
	return True	
	
#����ļ�
def crtOutFile(targetfile,records):
	fout = file(targetfile,'w')
	for rec in records:
		if isinstance(rec,Record):
			fout.write(rec.toString()+'\n')
		else:
			fout.write(rec+'\n')	
	fout.close()
#��ȡ�ļ�����	
def readFileContent(filelist,sourcedir):
	records=[]
	seqnum = 1
	amtsum = 0
	flag=0
	for index,filename in enumerate(filelist):
		#print filename
	
		fin = file(sourcedir+os.sep+filename,'r')
		i = 0
		while True:
			i = i + 1
			line   = fin.readline()
			if len(line)==0:
				break;
			if not checkin(line):
				print filename+'�ĵ�(',i,')�� �������� '+line
				flag = 1
				continue
				raw_input('���س�������')
				#sys.exit(-1)
			tt=line.split(',')
			
					
			fields = line.split(',')	
			
			cardid  =Field(fields[0],28,'L')
			amt     =Field(fields[1],15,'N')
			trancode=Field(fields[2][:2],2,'R')			
			merchid =Field(fields[3][:15],15,'Z')
			
			if (len(tt)==5): 
				msgflag =Field(fields[4][:1],1,'Z')
			if (len(tt)==4):
				msgflag =Field('0',1,'Z')
			
			amtsum=amtsum+int(fields[1])
			
			record  =Record(cardid,amt,trancode,merchid,msgflag)
	
			record.SeqNumber=Field(str(seqnum),8,'N')
			record.DepNum=Field(filename.split('.')[1],10,'L')
	
	 		records.append(record)
			#print record.toString()
			seqnum = seqnum + 1
		fin.close()
	rsize=len(records)	
	header='4222208000000000RECR'+time.strftime('%Y%m%d%H:%M:%S')+'  '+str(amtsum).zfill(18)+'  '+str(seqnum-1).zfill(18)+'   '+' '.ljust(125)
	tailer='42222082'+str(seqnum).zfill(8)+time.strftime('%Y%m%d%H:%M:%S')+'  '+str(amtsum).zfill(18)+'  '+str(seqnum-1).zfill(18)+' '.ljust(132)
	records.insert(0,header)
	records.append(tailer)
	return records	
def dismenu():
	os.system('cls')
	menu='''            QCC���շ��ı�����
	     1:���������ļ��嵥
	     2:������Ч��
	     3:������Ч�Բ������ϴ��ı�
	     4:�������е����ı�
	     5:�������ս���ı�
	     0:�˳���'''		
	print menu
	cmd=raw_input('      ��ѡ��:')
	  
	return cmd  
	
def sendtxt(user,passwd,rdir,filename):
	ftp=FTP('21.123.76.152')
	ftp.login(user,passwd)
	#print ftp.getwelcome()
	ftp.cwd(rdir)
	bufsize = 1024*1024
	file_handler = open(filename,'rb')
	ftp.storbinary('STOR '+os.path.basename(filename),file_handler,bufsize)   #�ϴ��ļ�
	ftp.set_debuglevel(0)

	file_handler.close()         #�ر��ļ�
	ftp.quit()
def getresptxt(user,passwd,rdir,filename):
	ftp=FTP('21.123.76.118')
	ftp.login(user,passwd)
	print ftp.getwelcome()
	ftp.cwd(rdir)
	bufsize = 1024*1024
	file_handler = open(filename,'wb').write
	print ftp.retrbinary('RETR '+os.path.basename(filename),file_handler,bufsize) 
	ftp.set_debuglevel(0)

	ftp.quit()	
##################################
#  ��ʼ����
##################################		

workdate = getDate() 	 #���������ı�ƥ�������8λ
workdate2= workdate[2:]	 #���������ļ�ƥ�������6λ
d2=datetime.date.today() + datetime.timedelta(days=-1)
yestd=str(d2)[:4]+str(d2)[5:7]+str(d2)[8:10]
workdir = 'D:\\ftproot\\qcctxt'
sourcedir = workdir+os.sep+'txt'+os.sep+'source'
targetfile= workdir+os.sep+'txt'+os.sep+'target'\
		+os.sep+'QCCR.B4222208.D'+workdate2+'.TEMP'
respfile1 = workdir+os.sep+'txt'+os.sep+'target'\
		+os.sep+'QCCR.B4222208.D'+yestd[2:]+'.REPT.SUCC'	
respfile2 = workdir+os.sep+'txt'+os.sep+'target'\
		+os.sep+'QCCR.B4222208.D'+yestd[2:]+'.REPT.FAIL'			
#print 	respfile1,respfile2	
while True:
	cmd = dismenu()
	if not cmd.isdigit() or cmd not in ['0','1','2','3','4','5']:
		raw_input('        ��Ч��ѡ����,�س�����')
		continue
	if cmd == '0':
		exit(9)
	if cmd == '1':
		filelist = getFileList(sourcedir,workdate)
		print '\n'.join(filelist)
		pass
	if cmd == '2':
		
		#print '�Ժ�..'
		filelist = getFileList(sourcedir,workdate)
		readFileContent(filelist,sourcedir)
			
	if cmd == '3':
		print '�Ժ�..'
		filelist = getFileList(sourcedir,workdate)
		crtOutFile(targetfile,readFileContent(filelist,sourcedir))
		print 'ִ�����'	
	if cmd == '4':
		
		sendtxt('s2200000','zaxs!e3r4','issu/out',targetfile)
		pass
	if cmd == '5':
		print 	respfile1
		print 	respfile2
		getresptxt('7222208','7222208@1q','result',respfile1) #
		getresptxt('7222208','7222208@1q','result',respfile2)
		pass	
	raw_input('�س�����')				
#��ù���Ŀ¼����Ч�ļ����б�
