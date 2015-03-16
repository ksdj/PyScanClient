'''
Created on 2015-1-2

@author: qiuyx
'''

import unittest
from ScanClient import ScanServerClient
class TestScanServerClient(unittest.TestCase):
    
    __scanID=None
    __ssc=None

    @classmethod
    def setUpClass(cls):
        
        #host = raw_input('Please input the scanserver IP:')
        #port = input('Please input the scanserver port:')
        cls.__ssc = ScanServerClient('localhost',4810)
        rtval = cls.__ssc.submitScan(scanXML='<commands><comment><address>0</address><text>Successfully adding a new scan!</text></comment></commands>',scanName='1stScan')
        #print 'rtval=',rtval
        if '<id' in rtval:
            cls.__scanID = rtval[4:rtval.find('</id>')]
        if cls.__scanID.isalnum():
            cls.__scanID = int(cls.__scanID)
        #cls.assertIsNotNone(cls.__scanID)
        print 'New scan is setted up, cls.__scanID = ' , cls.__scanID
        #print self.assertIsInstance(self.__ssc, ScanServerClient)  
        print '\n=============Setup Done.=============\n'
        
    '''
    def test_submitScan(self):
        
        rtval = self.__ssc.submitScan(scanXML='<commands><comment><address>0</address><text>Successfully adding a new scan!</text></comment></commands>',scanName='1stScan')
        #print 'rtval=',rtval
        if '<id' in rtval:
            self.__scanID = rtval[4:rtval.find('</id>')]
        if self.__scanID.isalnum():
            self.__scanID = int(self.__scanID)
        self.assertIsNotNone(self.__scanID)
        print 'self.__scanID = ' , self.__scanID
        print '\n=============Submit Done.=============\n'
    '''
        
    def test_removeCompeletedScan(self):
        
        rtval = self.__ssc.removeCompeletedScan()
        self.assertTrue(rtval==200)
        print '\n=============RemoveCompleletedScan Done.=============\n' 
         
    def test_simulateScan(self):
        
        rtval = self.__ssc.simulateScan(scanXML='<commands><comment><address>0</address><text>Successfully adding a new scan!</text></comment></commands>')
        self.assertIn('<simulation', rtval)
        print '\n=============Simulate Done.=============\n'
        
    def test_deleteScan(self):

        rtval = self.__ssc.deleteScan(self.__scanID)
        self.assertTrue(rtval==200)
        print '\n=============delete Done.=============\n'
 
    def test_getAllScanInfo(self):

        rtval = self.__ssc.getAllScanInfo()
        self.assertIn('<scans',rtval)   
        print '\n=============getAllScanInfo Done.=============\n'
        
    def test_getScanInfo(self):
        
        rtval = self.__ssc.getScanInfo(self.__scanID,'scan')
        self.assertIn('<scan',rtval)
        rtval = self.__ssc.getScanInfo(self.__scanID,'data')
        self.assertIn('<data',rtval)
        rtval = self.__ssc.getScanInfo(self.__scanID,'commands')
        self.assertIn('<commands',rtval)
        rtval = self.__ssc.getScanInfo(self.__scanID,'last_serial')
        self.assertIn('<serial',rtval)
        rtval = self.__ssc.getScanInfo(self.__scanID,'devices')
        self.assertIn('<devices',rtval)
        print '\n=============get Scaninfo Done.=============\n' 
        
    def test_pause(self):

        rtval = self.__ssc.pause(self.__scanID)
        self.assertTrue(rtval==200)
        print '\n=============Pause Done.=============\n' 
        
    def test_resume(self):

        rtval = self.__ssc.resume(self.__scanID)
        self.assertTrue(rtval==200)
        print '\n=============resume Done.=============\n' 

    def test_updateCommand(self):
        #rtval = self.__ssc.updateCommand(170, )
        None
        
    def test_abort(self):

        rtval = self.__ssc.abort(self.__scanID)
        self.assertTrue(rtval==200)
        print '\n=============abort Done.=============\n' 
    

#if __name__ == '__main__':
    #unittest.main()

print '\n',__name__
print  '==========================Test Start=========================='
suite = unittest.TestSuite()
suite.addTest(TestScanServerClient("test_simulateScan"))
#suite.addTest(TestScanServerClient("test_submitScan"))
suite.addTest(TestScanServerClient("test_getAllScanInfo"))
suite.addTest(TestScanServerClient("test_removeCompeletedScan"))
suite.addTest(TestScanServerClient("test_getAllScanInfo"))
suite.addTest(TestScanServerClient("test_getScanInfo"))
suite.addTest(TestScanServerClient("test_pause"))
suite.addTest(TestScanServerClient("test_resume"))
suite.addTest(TestScanServerClient("test_abort"))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)

#suite = unittest.TestLoader().loadTestsFromTestCase(TestScanServerClient)
