import random, re, psuedo
import argparse, subprocess, atexit, urllib.request, sys
from typing import List


_prefix = ['0', '2', '4', '6', '8', 'A', 'C', 'E']
_blacklist = set()
_access = False

'''
@desc: Format MAC address to adhere to protocol
'''
def _format(address: List[str]) -> None:
  for i in range(len(address)):
    address[i] = address[i].upper()
    if(len(address[i]) != 2 and address[i] != ':'):
      address[i] = '0' + address[i]

'''
@desc: Generate a new MAC address
'''
def _mask() -> None:
  mac = [random.choice(_prefix) + random.choice(_prefix)]
  for i in range(5):
    mac.append(hex(psuedo.lcg(10, 255))[2:])
  
  _format(mac)
  return mac

'''
@desc: Retrieve current MAC address
'''
def _get(iface: str) -> str:
  out = subprocess.check_output(f'ifconfig {iface}', shell=True).decode()
  match = re.search('ether (.+)', out).group()
  f = open('previous-address.txt', 'w')
  f.write(match)
  f.close()
  return match

'''
@desc: Set MAC address
'''
def _change(iface: str, mask: str) -> None:
  subprocess.check_output(f'ifconfig {iface} down', shell=True)
  subprocess.check_output(f'ifconfig {iface} hw ether {mask}', shell=True)
  subprocess.check_output(f'ifconfig {iface} up', shell=True)

'''
@desc: Update blacklist set
'''
def _update() -> None:
  with open('blacklist.txt', 'rb') as f:
    f.seek(-2, 2)
    while(f.read(1) != b'\n'):
      f.seek(-2, 1)
    patch = f.readline().decode()

  _blacklist.add(patch)

'''
@desc: Reset MAC address
'''
def _terminate(iface: str) -> None:
  f = open('previous-address.txt', 'r')
  original = f.read()
  f.close()

  _change(iface, original)

  urllib.urlopen('https://google.com')
  print(f'[+] Resetting MAC address: {original}')

'''
@desc: Execute MAC address changer
'''
if(__name__ == '__main__'):
  parser = argparse.ArgumentParser(description=
                                  'Temporarily Change Your MAC Address')
  parser.add_argument('interface', help='Network Interface')
  parser.add_argument('-r', '--random', action='store_true', 
                                        help='Generate A New MAC Address')
  args = parser.parse_args(sys.argv)
  iface = args.interface

  if(args.random):
    connect = _mask()
    prev = _get(iface)
    _change(iface, connect)

    while(True):
      try:
        urllib.urlopen('https://google.com')
      except:
        f = open('blacklist.txt', 'a')

        if(not _access):
          f.write(connect)
          _access = not _access
        else:
          f.write('\n' + connect)
        
        f.close()
        _update()
        connect = _mask()
      else:
        break

    print(f'[-] Previous MAC address: {prev}')
    print(f'[+] Current MAC address: {connect}')
    
    atexit.register(_terminate, iface = iface)