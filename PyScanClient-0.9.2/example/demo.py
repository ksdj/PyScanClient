'''
Created on 2014-1-12
@author: qiuyx
'''
from ScanClient import ScanServerClient
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

#get the client instance
ssc=ScanServerClient('localhost','4810')

#check scan server
print ssc.getScanServerInfo()

#define a new scan
newScan = '<commands><comment><address>0</address><text>Successfully adding a new scan</text></comment></commands>'

#clear scan server
print ssc.removeCompletedScan

#simulate the new scan
print ssc.simulateScan(newScan)

#submit the new scan and get the scan id
sid = ssc.submitScan(scanXML=newScan,scanName='TestDemo')
sid = str[4:sid.find('</id>')]

#get all scans
print ssc.getAllScanInfo()

#abort the scan
print ssc.abort(sid)

####################2015-3-8 New ScanClient####################
#generalize client instance:
ssc = ScanServerClient(host='localhost',port=4810)

#Create Command Sequence:
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
# You can create multiple command sequence:
cmds2 = CommandSequence(
   CommentCommand('Another Command Sequence.'),

   LoopCommand(device='xpos',start=0.0,end=10.0,step=1.0,completion=True,wait=True,
               body=[CommentCommand(comment='haha'),
                     ConfigLogCommand(automatic=True)
                     ]),
   SetCommand(device='shutter',value=0.1,completion=True,wait=False,tolerance=0.1,timeOut=0.1),
   WaitCommand(device='shutter',desiredValue=10.0,comparison='=',tolerance=0.1,timeout=5.0)
)

#have a look at the sequence:
print cmds1.toSeqString()
#have a look at the generated .scn file:
print cmds1.genSCN()

#old submit:
ssc.submitScanXML(cmds1.genSCN())
#or new submit:
ssc.submitScan(cmds1)