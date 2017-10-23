#coding:utf-8  
fromctypes import*  
importos   
importsys   
importftplib   
class myFtp:   
  ftp=ftplib.FTP()   
  bIsDir=False  
  path=""   
  def __init__(self, host, port='21'):  
    self.ftp.set_debuglevel(2)#打开调试级别2，显示详细信息   
    #self.ftp.set_pasv(0)  #0主动模式 1 #被动模式   
    self.ftp.connect( host, port )   
  def Login(self, user, passwd ):   
    self.ftp.login( user, passwd )   
    printself.ftp.welcome  
  def DownLoadFile( self, LocalFile, RemoteFile ):   
    file_handler=open( LocalFile, 'wb')   
    self.ftp.retrbinary("RETR %s" %( RemoteFile ), file_handler.write )    
    file_handler.close()  
    return True  
  def UpLoadFile( self, LocalFile, RemoteFile ):   
    if os.path.isfile( LocalFile ) ==False:  
      return False  
    file_handler=open( LocalFile, "rb")   
    self.ftp.storbinary('STOR %s'%RemoteFile, file_handler, 4096)  
    file_handler.close()  
    return True  
  def UpLoadFileTree( self, LocalDir, RemoteDir ):   
    if os.path.isdir( LocalDir ) ==False:  
      return False  
    LocalNames=os.listdir( LocalDir )   
    printRemoteDir   
    self.ftp.cwd( RemoteDir )   
    for Local inLocalNames:   
      src=os.path.join( LocalDir, Local)   
      if os.path.isdir( src ):   
        self.UpLoadFileTree( src, Local )   
      else:  
        self.UpLoadFile( src, Local )   
    self.ftp.cwd("..")   
    return  
  def DownLoadFileTree( self, LocalDir, RemoteDir ):   
    if os.path.isdir( LocalDir ) ==False:  
      os.makedirs( LocalDir )   
    self.ftp.cwd( RemoteDir )   
    RemoteNames=self.ftp.nlst()   
    for file in RemoteNames:   
      Local=os.path.join( LocalDir, file)   
      if self.isDir(file):   
        self.DownLoadFileTree( Local, file)           
      else:  
        self.DownLoadFile( Local, file)   
    self.ftp.cwd("..")   
    return  
  def show( self,list):   
    result=list.lower().split(" " )   
    if self.pathinresult and"<dir>" in result:   
      self.bIsDir=True  
  def isDir( self, path ):   
    self.bIsDir=False  
    self.path=path   
    #this ues callback function ,that will change bIsDir value   
    self.ftp.retrlines('LIST',self.show )   
    return self.bIsDir  
  def close( self):   
    self.ftp.quit()  
ftp=myFtp('********')  
ftp.Login('*****','*****')  
#ftp.DownLoadFile('TEST.TXT', 'others\\runtime.log')#ok   
#ftp.UpLoadFile('runtime.log', 'others\\runtime.log')#ok   
#ftp.DownLoadFileTree('bcd', 'others\\abc')#ok   
#ftp.UpLoadFileTree('aaa',"others\\" )   
ftp.close()  
print"ok!"  

