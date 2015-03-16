'''
Copyright (c) 2014 
All rights reserved. Use is subject to license terms and conditions.
Created on 30 12, 2014
@author: Yongxiang Qiu
'''

import requests
from ScanClient.CommandSequence import CommandSequence
from ScanClient.CommentCommand import CommentCommand
from ScanClient.ConfigLogCommand import ConfigLogCommand 
from ScanClient.DelayCommand import DelayCommand
from ScanClient.IncludeCommand import IncludeCommand
from ScanClient.LogCommand import LogCommand
from ScanClient.LoopCommand import LoopCommand
from ScanClient.ScriptCommand import ScriptCommand
from ScanClient.SetCommand import SetCommand
from ScanClient.WaitCommand import WaitCommand

class ScanServerClient(object):
    '''
    The ScanServerClient provides interfaces to interact with java-ScanServer,
    which includes methods such as Start,Pause,GetScanInfo... to manipulate 
    the behaviors and retrieve data from Scan.
    '''
    __baseURL = None
    __serverResource = "/server"
    __serverInfoResource = "/info"
    __simulateResource = "/simulate"
    __scansResource = "/scans"
    __scansCompletedResource = "/completed"
    __scanResource = "/scan"
    #__curScanXML = "No contents."
    #__curScanName = "No name."
    SCN = '<commands></commands>'
    
    def __new__(cls, host = 'localhost',port=4810):
        '''   
        Singleton method to make sure there is only one instance alive.
        '''
        
        if not hasattr(cls, 'instance'):
            cls.instance = super(ScanServerClient,cls).__new__(cls)
        return cls.instance
    
    def __init__(self, host = 'localhost',port=4810):
        
        self.__baseURL = "http://"+host+':'+str(port)
        
        try:  
            requests.get(self.__baseURL+'/scans', verify=False).raise_for_status()
        except:
            raise Exception, 'Failed to create client to ' + self.__baseURL
        
        
        
    def submitScanXML(self,scanXML=None,scanName='UnNamed'):
        '''
        Create and submit a new scan from raw XML-form.
        
        Using   POST {BaseURL}/scan/{scanName}
        Return  <id>{scanId}</id>
        
        :param scanXML: The XML content of your new scan
        :param scanName: The name you want to give the new scan
        
        Usage::

        >>> import ScanServerClient
        >>> ssc=ScanServerClient('localhost',4810)
        >>> scanId = ssc.submitScan(scanXML='<commands><comment><address>0</address><text>Successfully adding a new scan!</text></comment></commands>',scanName='1stScan')
        '''
        
        if scanXML == None:
            scanXML = raw_input('Please enter your scanXML:') 
        try:
            url = self.__baseURL+self.__scanResource+'/'+scanName
            r = requests.post(url = url,data = scanXML,headers = {'content-type': 'text/xml'}) 
        except:
            raise Exception, 'Failed to submit scan.'
        
        self.__curScanXML = scanXML
        self.__curScanName = scanName
        if r.status_code == 200:
            return r.text
        else:
            return None
    
    def submitScan(self,cmdSeq=None,scanName='UnNamed'):
        '''
        Create and submit a new scan from Command Sequence.
        
        Using   POST {BaseURL}/scan/{scanName}
        Return  <id>{scanId}</id>
        
        :param cmdSeq: The Command Sequence of a new scan
        :param scanName: The name needed to give the new scan
        
        Usage::

        >>> import ScanServerClient
        >>> ssc=ScanServerClient('localhost',4810)
        >>> cmds1 = CommandSequence(
                       CommentCommand(comment='haha'),
                       CommentCommand('hehe'),
                       ConfigLogCommand(automatic=True),
                       DelayCommand(seconds=2.0),
                       IncludeCommand(scanFile='1.scn',macros='macro=value'),
                       LogCommand('shutter','xpos','ypos'),
                       LoopCommand(device='xpos',start=0.0,end=10.0,step=1.0,completion=True,wait=True,
                                   body=[CommentCommand(comment='haha'),
                                         ConfigLogCommand(automatic=True)
                                         ]),
                       ScriptCommand('submit.py',1,'abc',0.05),
                       SetCommand(device='shutter',value=0.1,completion=True,wait=False,tolerance=0.1,timeOut=0.1),
                       WaitCommand(device='shutter',desiredValue=10.0,comparison='=',tolerance=0.1,timeout=5.0)
                    )
        >>> scanId = ssc.submitScan(scanXML='<commands><comment><address>0</address><text>Successfully adding a new scan!</text></comment></commands>',scanName='1stScan')
        '''
        
        if cmdSeq!=None:
            self.submitScanXML(cmdSeq.genSCN(),scanName)
        else:
            print 'No scan defined!'
    
    def simulateScan(self,scanXML=None):
        '''
        Simulate a scan.
        
        Using   POST {BaseURL}/simulate
        Return  Success Messages in XML form
        
        :param scanXML: The XML content of your new scan
        
        Usage::

        >>> import ScanServerClient
        >>> ssc=ScanServerClient('localhost',4810)
        >>> sid = ssc.simulateScan(scanXML='<commands><comment><address>0</address><text>Successfully simulating a new scan!</text></comment></commands>')
      
        '''
        if scanXML == None:
            scanXML = raw_input('Please enter your scanXML:') 
        r = requests.post(url = self.__baseURL+self.__simulateResource,data = scanXML,headers = {'content-type': 'text/xml'}) 
        if r.status_code == 200:
            return r.text
        else:
            return None
        
    def deleteScan(self,scanID = None):
        '''
        Remove a unique scans.
        
        Using DELETE {BaseURL}/scan/{scanID}.
        Return HTTP status code.
        
        :param scanID: The id of scan you want to delete.Must be an integer.
        
        Usage::

        >>> import ScanServerClient
        >>> ssc=ScanServerClient('localhost',4810)
        >>> st = ssc.deleteScan(153)
      
        Return the status code. 0 if Error parameters.
        '''
        if scanID == None:
            scanID = raw_input('Please enter your scan ID:')
        elif not isinstance(scanID, int):
            scanID = input('Scan ID must be an integer.Please reenter:')
        
        try:
            r=requests.delete(url = self.__baseURL+self.__scanResource+'/'+str(scanID))
            print 'Scan %d deleted.'%scanID
        except:
            raise Exception, 'Failed to deleted scan '+str(scanID)
        return r.status_code

    def removeCompeletedScan(self):
        '''
        Remove completed scan.
        
        Using DELETE {BaseURL}/scans/completed.
        Return HTTP status code.
        
        Usage::

        >>> import ScanServerClient
        >>> ssc=ScanServerClient('localhost',4810)
        >>> st = ssc.removeCompeletedScan()
        '''
        
        try:
            r = requests.delete(url = self.__baseURL+self.__scansResource+self.__scansCompletedResource)
            print 'All completed scans are deleted.'
        except:
            raise Exception, 'Failed to remove completed scan.'
        return r.status_code
    
    #############Detailed Design Needed#############
    def getScanInfo(self,scanID = None,infoType = None):
        '''
        Get all information of one scan.
        Using  GET {BaseURL}/scan/{scanID}                - get scan info
               GET {BaseURL}/scan/{scanID}/commands       - get scan commands
               GET {BaseURL}/scan/{scanID}/data           - get scan data
               GET {BaseURL}/scan/{scanID}/last_serial    - get scan data's last serial
               GET {BaseURL}/scan/{scanId}/devices        - get devices used by a scan
        Return all scan info in XML form.
        
        :param scanID: The id of scan you want to get.Must be an integer.
        
        Usage::

        >>> import ScanServerClient
        >>> ssc=ScanServerClient('localhost',4810)
        >>> st = ssc.getScanInfo(153,scan)
        '''
        
        if scanID == None:
            scanID = raw_input('Please enter your scan ID:')
        elif not isinstance(scanID, int):
            scanID = input('Scan ID must be an integer.Please reenter:')
            
        if infoType == None:
            infoType = raw_input('Select the type of the info you want below-(scan, data, commands, last_serial, devices):')
        
        try:
            if infoType == 'scan':
                url = self.__baseURL+self.__scanResource+'/'+str(scanID)
            else:
                url = self.__baseURL+self.__scanResource+'/'+str(scanID)+'/'+infoType
            r = requests.get(url)
        except:
            raise Exception, 'Failed to get info from scan '+str(scanID)
        return r.text
                
    def getScanServerInfo(self):
        '''
        Get information of current server
        Using GET {BaseURL}/server/info
        Return:<Server></Server>
        
        Usage::

        >>> import ScanServerClient
        >>> ssc=ScanServerClient('localhost',4810)
        >>> st = ssc.getScanServerInfo()
        '''
        
        try:
            r = requests.get(url = self.__baseURL+self.__serverResource+self.__serverInfoResource)
        except:
            raise Exception, 'Failed to get info from scan server.'
        return r.text
        
    def getAllScanInfo(self):
        '''
        Get information of all scans 
        Using GET {BaseURL}/scans - get all scan infos
        Return all info of all scans in XML form.
        
        Usage::

        >>> import ScanServerClient
        >>> ssc=ScanServerClient('localhost',4810)
        >>> st = ssc.getAllScanInfo()
        '''
        try:
            r = requests.get(url = self.__baseURL+self.__scansResource)
        except:
            raise Exception, 'Failed to get info from scan server.'
        return r.text

    def pause(self,scanID=None):
        ''' 
        Pause a running scan
        
        Using PUT {BaseURL}/scan/{id}/pause
        Return Http Status Code
        
        Usage::

        >>> import ScanServerClient
        >>> ssc=ScanServerClient('localhost',4810)
        >>> st = ssc.pause(153)
        '''

        if scanID == None:
            scanID = input('Enter id of the scan you want to pause:')
        elif not isinstance(scanID, int):
            scanID = input('Scan ID must be an integer.Please reenter:')
        
        try:
            r = requests.put(url=self.__baseURL+self.__scanResource+'/'+str(scanID)+'/pause')
        except:
            raise Exception, 'Failed to get info from scan server.'
        return r.status_code
        
    def abort(self,scanID=None):
        '''
        Abort running or paused scan
        
        Using PUT {BaseURL}/scan/{id}/abort
        Return Http Status Code
        
        Usage::

        >>> import ScanServerClient
        >>> ssc=ScanServerClient('localhost',4810)
        >>> st = ssc.abort(153)
        '''
        
        if scanID == None:
            scanID = input('Enter id of the scan you want to abort:')
        elif not isinstance(scanID, int):
            scanID = input('Scan ID must be an integer.Please reenter:')
    
        try:
            r = requests.put(url=self.__baseURL+self.__scanResource+'/'+str(scanID)+'/abort')
        except:
            raise Exception, 'Failed to abort scan '+str(scanID)
        return r.status_code
    
    def resume(self,scanID=None):
        '''
        Resume paused scan
        Using PUT {BaseURL}/scan/{scanID}/resume
        
        Return Http Status Code
        
        Usage::

        >>> import ScanServerClient
        >>> ssc=ScanServerClient('localhost',4810)
        >>> st = ssc.abort(153)
        '''
        
        if scanID == None:
            scanID = input('Enter id of the scan you want to resume:')
        elif not isinstance(scanID, int):
            scanID = input('Scan ID must be an integer.Please reenter:')
        
        try:
            r = requests.put(url=self.__baseURL+self.__scanResource+'/'+str(scanID)+'/resume')
        except:
            raise Exception, 'Failed to resume scan ',scanID
        return r.status_code        
        
    def updateCommand(self,scanID=None,scanXML=None):
        '''
        Update property of a scan command.
        
        Using PUT {BaseURL}/scan/{scanID}/patch
        Return Http Status Code.
        
        Requires description of what to update:
          
            <patch>
                <address>10</address>
                <property>name_of_property</property>
                <value>new_value</value>
            </patch>
          
        '''
        if scanXML == None:
            scanXML = raw_input('Please enter your scanXML:') 
        
        if scanID == None:
            scanID = input('Enter id of the scan you want to update:')
        elif not isinstance(scanID, int):
            scanID = input('Scan ID must be an integer.Please reenter:')
        
        try:
            r = requests.put(url=self.__baseURL+self.__scanResource+'/'+str(scanID)+'/patch',data=scanXML,headers= {'content-type': 'text/xml'})
        except:
            raise Exception, 'Failed to resume scan '+str(scanID)
        return r.status_code
    
    #Guobao's requirement:
    '''
    def resubmit(self):
        self.submitScan(self.__curScanXML, self.__curScanName)
    '''
     

        
'''
ssc=ScanServerClient(host='localhost',port=4810)
for i in range(278,283):
    ssc.abort(i)
else:
    print 'All scans aborted.'
'''

'''
ssc = ScanServerClient(host='localhost',port=4810)
cmds1 = CommandSequence(
   CommentCommand(comment='haha'),
   CommentCommand('hehe'),
   ConfigLogCommand(automatic=True),
   DelayCommand(seconds=2.0),
   IncludeCommand(scanFile='1.scn',macros='macro=value'),
   LogCommand('shutter','xpos','ypos'),
   LoopCommand(device='xpos',start=0.0,end=10.0,step=1.0,completion=True,wait=True,
               body=[CommentCommand(comment='haha'),
                     ConfigLogCommand(automatic=True)
                     ]),
   ScriptCommand('submit.py',1,'abc',0.05),
   SetCommand(device='shutter',value=0.1,completion=True,wait=False,tolerance=0.1,timeOut=0.1),
   WaitCommand(device='shutter',desiredValue=10.0,comparison='=',tolerance=0.1,timeout=5.0)
)

cc=CommentCommand('hehe')
print cc.toCmdString()
print cmds1.toSeqString()
print cmds1.genSCN()
ssc.submitScanXML(cmds1.genSCN())
'''
