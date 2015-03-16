'''
Created on Mar 8,2015

@author: qiuyx
'''
from ScanClient.Command import Command

class CommentCommand(Command):
    '''
    CommentCommand Class.
    SubClass of Command.
    '''
    
    def __init__(self, comment="This is an example comment."):
        '''
        params comment Comments needed to add.
        '''
        self.comment=comment
    
    def genXML(self):
        return '<comment>'+'<text>'+self.comment+'</text>'+'</comment>'
        
    def toCmdString(self):
        return 'CommentCommand(Comment='+self.comment+')'
    
    
        