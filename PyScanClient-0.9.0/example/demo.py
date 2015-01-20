'''
Created on 2014-1-12
@author: qiuyx
'''
import ScanServerClient

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