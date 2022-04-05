


################# classes ##########################

class MacAddress(object):
    '''
    A class for manipulating mac addresses
    '''
    ## endianness - big endian, little endian, group/multicast bit, global/admin bit, oui lookup
    ## see also https://www.macvendorlookup.com/api - oui lookup
    def __init__(self,mac):
        '''
        :param mac: a mac address
                    instantiation func attempts to normalize
                    and validate typical forms of a mac
                    accepts the following f orms:
                    xx:xx:xx:xx:xx:xx
                    xxxx.xxxx.xxxx
                    xxxxxxxxxxxx
        '''
        import re
        ## if in xx:xx:xx:xx:xx:xx
        if re.match('(?:[0-9A-Fa-f]{2}[-.:]){5}[0-9A-Fa-f]{2}',mac):
            self.bytes = [x.lower() for x in re.split('[-.:]',mac)]
        ## if in xxxx.xxxx.xxxx
        elif re.match('(:?[0-9A-Fa-f]{4}[-.:]){2}[0-9A-Fa-f]{4}',mac):
            self.bytes = [subel.lower() for el in re.split('[-.:]',mac) for subel in [el[i:i+2] for i in range(0,len(el),2)]]
        ## if in xxxxxxxxxxxx
        elif re.match('[0-9A-Fa-f]{12}',mac):
            self.bytes = [mac[i:i+2] for i in range(0,len(mac),2)]
        ## default action is to raise exception
        ## and not create object
        else:
            raise ValueError("Ethernet MAC not found")
        self.mac = self.form_a = '.'.join([self.bytes[i] + self.bytes[i+1] for i in range(0,len(self.bytes),2)])
        self.form_b = ':'.join(self.bytes)
        self._is_global()
        self._is_group()
#
    def __repr__(self):
        return self.form_a
#
    def bitswap_mac(self):
        '''
        swaps bit order for eachbyte of a mac
        bytes themselvs remain in same order
        0x01 -> 0x80
        0x02 -> 0x40
        0xc1 -> 0x83
        etc...
        '''
        reverse_bytes = []
        for b in self.bytes:
            ## bin string forward
            bin1 = format(int(b,16),'08b')
            ## bin string reversed
            bin2 = bin1[-1::-1]
            reverse_bytes.append(format(int(bin2,2),'02x'))
        return '.'.join([reverse_bytes[i] + reverse_bytes[i+1] for i in range(0,len(reverse_bytes),2)])
#
    def _is_group(self):
        '''
        checks the group/individual bit (least sig bit of first byte)
        1 = group (multicast)
        0 = individual (unicast)
        '''
        if int(self.bytes[0], 16) & 1:
            self.isGroup = True
            self.isMulticast = True
        else:
            self.isGroup=False
            self.isMulticast=False
#
    def _is_global(self):
        '''
        checks the global/local bit (next to least sig bit of first byte)
        1 = locally admin
        0 = globally unique
        '''
        if int(self.bytes[0], 16) & 2:
            self.isGlobal=False
        else:
            self.isGlobal=True


class IPv4NetworkArray(list):
    '''
    holds a list of networks
    '''
    import ipaddress
    def __init__(self, *args, **kwargs):
        '''
        '''
        super().__init__(*args, **kwargs)
        self.netlist=[]
        try:
            for n in self:
                self.netlist.append(self.ipaddress.IPv4Network(n))
        except ValueError:
            raise
        self.sort(key = lambda x: self.ipaddress.IPv4Network(x))
        self.netlist.sort()
    def __contains__(self,ipadd):
        '''
        func to check list of nets at once
        '''
        try:
            ipadd = self.ipaddress.IPv4Address(ipadd)
            for n in self.netlist:
                if ipadd in n:
                    return True
        except self.ipaddress.AddressValueError:
            try:
                ipnet = self.ipaddress.IPv4Network(ipadd)
                if ipnet in self.netlist:
                    return True
            except:
                raise ValueError("Not a IP address or IP network or format incorrect")
        return False
    def find_all_nets_for_ip(self, ipadd):
        '''
        returns list of networks a given IP is found in
        '''
        returnlist = []
        try:
            ipadd = self.ipaddress.IPv4Address(ipadd)
        except ValueError:
            raise
        for n in self.netlist:
            if ipadd in n:
                returnlist.append(str(n))
        return IPv4NetworkArray(returnlist)
        
        
############ functions ###############

def taboff():
        '''
        function to turn readline autocomplete tabs off
        useful for pasting in text that contains tabs
        '''
        import readline
        readline.parse_and_bind('set disable-completion on')
        return

def tabon():
        '''
        function to turn readline autocomplete tabs on
        useful for reversing taboff() function
        '''
        import readline
        readline.parse_and_bind('set disable-completion off')
        return

############ ipaddress functions ###################

def findholes(ipaddresslist, terse=True):
    '''
    returns list of ipaddresses NOT in the list between the lowest IP and the highest IP
    verbose mode returns the list of ipaddresses with empty strings taking the place of 
    missing IP addresses
    note: this list can be very long if including multiple subnets, by accident or otherwise
    '''
    from ipaddress import ip_address
    ipaddresslist.sort(key=lambda x: ipaddress.ip_address(x))
    start_ip_as_int = int(ipaddress.ip_address(ipaddresslist[0]))
    end_ip_as_int = int(ip_address(ipaddresslist[-1]))
    if terse:
        return [ str(ip_address(ip_as_int)) for ip_as_int in range(start_ip_as_int, end_ip_as_int + 1) if str(ip_address(ip_as_int)) not in ipaddresslist ]
    else:
        return [ str(ip_address(ip_as_int)) if str(ip_address(ip_as_int)) in ipaddresslist else '' for ip_as_int in range(start_ip_as_int, end_ip_as_int + 1) ]


############### ignore below here ##########
