'''
Created on Mar 8,2015

@author: qiuyx
'''
from ScanClient.Command import Command

class DelayCommand(Command):
    '''
    classdocs
    '''


    def __init__(self, seconds=1.0):
        '''
        Constructor
        '''
        self.seconds=seconds
    
    def genXML(self):
        return '<delay>'+'<seconds>'+str(self.seconds)+'</seconds>'+'</delay>'
        
    def toCmdString(self):
        return 'DelayCommand(seconds='+str(self.seconds)+')'
