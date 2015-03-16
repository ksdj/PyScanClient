'''
Created on Mar 8,2015

@author: qiuyx
'''
from string import lower
from ScanClient.Command import Command

class ConfigLogCommand(Command):
    '''
    classdocs
    '''


    def __init__(self, automatic=False):
        '''
        Constructor
        '''
        self.automatic=automatic
        
    def genXML(self):
        return '<config_log>'+'<automatic>'+lower(str(self.automatic))+'</automatic>'+'</config_log>'
        
    def toCmdString(self):
        return 'ConfigLogCommand(Automatic='+lower(str(self.automatic))+')'
    
        