'''
Created on Mar 8,2015

@author: qiuyx
'''
from ScanClient.Command import Command

class IncludeCommand(Command):
    '''
    classdocs
    '''


    def __init__(self, scanFile=None,macros='macro=value'):
        '''
        Constructor
        '''
        self.scanFile=scanFile
        self.macros=macros
    
    def genXML(self):
        return '<include>'+'<scan_file>'+self.scanFile+'</scan_file>'+'<macros>'+self.macros+'</macros></include>'
        
    def toCmdString(self):
        return 'InclueCommand(scan_file='+self.scanFile+',macros='+self.macros+')'