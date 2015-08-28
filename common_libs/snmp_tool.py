#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pysnmp.entity.rfc3413.oneliner import cmdgen

class SNMP(object):
    def __init__(self, community, ip, port=161, timeout=20, retries=5):
        '''
        Constructor
        '''
        self.cmd = cmdgen.CommunityData('my-agent', community, 1)
        self.target = cmdgen.UdpTransportTarget((ip, 161), timeout, retries)

    def GetRequest(self, oid):
        '''
        GetRequest Operation
        Return the value of a particular OID
        '''
        appreturn = {'errorIndication': None, 'errorStatus': None, 'value': None}
        errorIndication, errorStatus, errorIndex, varBindTable = cmdgen.CommandGenerator().getCmd(self.cmd, self.target,
                                                                                                  oid)
        if errorIndication:
            appreturn['errorIndication'] = errorIndication
            return appreturn
        else:
            if errorStatus:
                appreturn['errorStatus'] = '%s at %s\n' % (
                errorStatus.prettyPrint(), varBindTable[-1][int(errorIndex) - 1])
                return appreturn
            else:
                appreturn['value'] = str(varBindTable[0][1])

        return appreturn
        pass

    def GetBulkRequest(self, oid, non_repeaters=0, max_repeaters=25):

        ''' 
        GetBulkRequest Operation
        Get all the OIDs belongs to a particular Table  
        '''

        appreturn = {'errorIndication': None, 'errorStatus': None, 'TableItems': None}
        # get bulk request 
        errorIndication, errorStatus, errorIndex, varBindTable = cmdgen.CommandGenerator().bulkCmd(self.cmd,
                                                                                                   self.target,
                                                                                                   non_repeaters,
                                                                                                   max_repeaters, oid)
        if errorIndication:
            appreturn['errorIndication'] = errorIndication
            return appreturn
        else:
            if errorStatus:
                appreturn['errorStatus'] = '%s at %s\n' % (errorStatus.prettyPrint(), varBinds[-1][int(errorIndex) - 1])
                return appreturn
            else:
                TableItems = []
                for varBindTableRow in varBindTable:
                    for oid, val in varBindTableRow:
                        oid = list(oid)
                        TableItems.append([oid, str(val)])
        appreturn['TableItems'] = TableItems
        return appreturn

    def SetRequest(self, oid):
        pass

    def _del_(self):
        pass

# test
if __name__ == '__main__':
    snmp_object = SNMP('cisco', '10.79.148.211')
    # get host name through OID: 1.3.6.1.2.1.1.5.0 
    oid_sysName = (1, 3, 6, 1, 2, 1, 1, 5, 0)
    oid_ifHighSpeed = (1, 3, 6, 1, 2, 1, 31, 1, 1, 1, 15)
    result = snmp_object.GetRequest(oid_sysName)
    #print result
    result = snmp_object.GetBulkRequest(oid_ifHighSpeed)
