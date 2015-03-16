'''
Created on Mar 8,2015

@author: qiuyx
'''
from ScanClient.Command import Command

class WaitCommand(Command):
    '''
    classdocs
    '''


    def __init__(self, device=None,desiredValue=0.0,comparison='=',tolerance=0.1,timeout=0.0):
        '''
        Constructor
        '''
        self.device=device
        self.desiredValue=desiredValue
        self.comparison=comparison
        self.tolerance=tolerance
        self.timeout=timeout
         
    def genXML(self):
        result= '<wait>'
        result+= '<device>'+str(self.device)+'</device>'
        result+= '<value>'+str(self.desiredValue)+'</value>'
        #result+= '<comparison>'+str(self.comparison)+'</comparison>'
        if self.tolerance!=0.0:
            result+= '<tolerance>'+str(self.tolerance)+'</tolerance>'
        if self.timeout!=0.0:
            result+= '<timeout>'+str(self.timeout)+'</timeout>'
        result+= '</wait>'
        return result
        
    def toCmdString(self):
        result= 'WaitCommand('
        result+= 'device='+str(self.device)+','
        result+= 'desiredValue='+str(self.desiredValue)+','
        #result+= '<comparison>'+str(self.comparison)+'</comparison>'
        if self.tolerance!=0.0:
            result+= '<tolerance>'+str(self.tolerance)+'</tolerance>'
        if self.timeout!=0.0:
            result+= '<timeout>'+str(self.timeout)+'</timeout>'
        result+= ')'
        return result