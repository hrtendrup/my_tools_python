#!/usr/bin/env python3

def ip2hex(ip):
    '''
    '''
    import ipaddress
    try:
      try:
        return hex(int(ipaddress.ip_address(ip)))
      except:
        return str(ipaddress.ip_address(int(ip,16)))
    except:
        raise ValueError("Wrong format")

hex2ip = ip2hex

if __name__ == "__main__":
    import sys
    arg = sys.argv[1]
    print(ip2hex(arg))