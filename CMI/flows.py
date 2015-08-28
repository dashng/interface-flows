'''
Created on Aug 28, 2015

@author: shdai
'''
from lib.snmp import SNMP

class Flows(object):
    
    def __init__(self, ip, community):
        self.ip = ip
        self.community = community
        self._get_snmp_objects()
        self.oid_dict = {
            "InterfaceName": "1,3,6,1,2,1,2,2,1,2",
            "InterfaceDescr": "1,3,6,1,2,1,31,1,1,1,18",
            "ifHighSpeed": "1,3,6,1,2,1,31,1,1,1,15",
            "ifHCInOctets": "1,3,6,1,2,1,31,1,1,1,6",
            "ifHCInUcastPkts": "1,3,6,1,2,1,31,1,1,1,7",
            "ifHCInMulticastPkts": "1,3,6,1,2,1,31,1,1,1,8",
            "ifHCInBroadcastPkts": "1,3,6,1,2,1,31,1,1,1,9",
            "ifHCOutOctets": "1,3,6,1,2,1,31,1,1,1,10",
            "ifHCOutUcastPkts": "1,3,6,1,2,1,31,1,1,1,11",
            "ifHCOutMulticastPkts": "1,3,6,1,2,1,31,1,1,1,12",
            "ifHCOutBroadcastPkts": "1,3,6,1,2,1,31,1,1,1,13"
        }
    
    def _contains(self, small, big):
        big = list(big)
        big.pop()
        return small == big
    
    def _parse_oid_str(self, oid_str):
        return [int(n) for n in oid_str.split(',')]
    
    '''
        parse result to be interface {index : val} object
    '''
    def _get_if_val(self, res, oid):
        if_index_dict = {}
        contents_key = 'TableItems'
        if contents_key in res.keys():
            contents = res.get(contents_key)
            for content in contents:
                try:
                    if isinstance(content, list) and self._contains(oid, content[0]):
                        if_index_dict[content[0][-1]] = content[-1]
                    else:
                        continue
                except Exception, e:
                    print e
                    continue
        return if_index_dict
    
    def _get_snmp_objects(self):
        self.snmp_object = SNMP(self.community, self.ip)
    
    
    '''
        get interface {index : name} object
    '''
    def get_interfaces_name(self):
        if_name_id = self._parse_oid_str(self.oid_dict.get('InterfaceName', ''))
        res = self.snmp_object.GetBulkRequest(if_name_id)
        return self._get_if_val(res, if_name_id)
    
    def get_interfaces_in_Octets(self):
        if_name_id = self._parse_oid_str(self.oid_dict.get('ifHCInOctets', ''))
        res = self.snmp_object.GetBulkRequest(if_name_id)
        return self._get_if_val(res, if_name_id)
    
    def get_interface_out_Octets(self):
        if_name_id = self._parse_oid_str(self.oid_dict.get('ifHCOutOctets', ''))
        res = self.snmp_object.GetBulkRequest(if_name_id)
        return self._get_if_val(res, if_name_id)
    
    def get_if_index_val(self, oid):
        res = self.snmp_object.GetBulkRequest(oid)
        return self._get_if_val(res, oid)

if __name__ == '__main__':
    flows = Flows('10.79.148.211', 'cisco')
    print flows.get_interfaces_name()
    print flows.get_interfaces_in_Octets()
    print flows.get_interface_out_Octets()
    
        
    
