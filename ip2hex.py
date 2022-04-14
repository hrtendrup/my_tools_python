#!/usr/bin/env python3

def ip2hex(iporhex):
    '''
    '''
    import ipaddress
    try:
      try:
        return hex(int(ipaddress.ip_address(iporhex)))
      except:
        return str(ipaddress.ip_address(int(iporhex,16)))
    except:
        raise ValueError("Wrong format")

hex2ip = ip2hex

if __name__ == "__main__":
    import sys
    try:
        arg = sys.argv[1]
    except IndexError:
        print("Error: Missing IP or HEX value")
    else:
        print(ip2hex(arg))