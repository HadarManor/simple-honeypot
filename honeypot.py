#!/usr/bin/env python3  

import sys
import socket
import threading
import smtplib
from datetime import datetime

WELCOME_MSG = b"Ubuntu 20.04.1 LTS\r\nServer login: "
PORT = 23
HOST = ''
LISTEN_AMNT = 5
MAX_DATA = 1024
CLRF_CHARS = b'\r\n'


SERVER = "localhost" # Enter your SMTP Server
FROM = "honeypot@alert.com"
TO = "your@mail.com"


class Honeypot():
    """
    Honeypot class
    """
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((HOST, PORT))

    def handle_attacker(self, conn, addr):
        alert_msg = 'Honeypot has been accessed by ' + addr[0]
        self.alert_access(alert_msg)
        conn.sendall(WELCOME_MSG)
        while True:
            data = conn.recv(MAX_DATA)
            if data == CLRF_CHARS:
                self.sock.close()
                sys.exit()

    def start_hp(self):
        try:
            self.sock.listen(LISTEN_AMNT)
            while True:
                conn, addr = self.sock.accept()
                att_thread = threading.Thread(target = self.handle_attacker, args = (conn, addr))
                att_thread.start()
        except Exception as e:
            print(e)
            self.sock.close()
            sys.exit()

    def alert_access(self, alert_msg):
        now = datetime.now()
        subject = "honeypot alert " + now.strftime("%d/%m/%Y %H:%M:%S")
        message = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (FROM, TO, subject, alert_msg)
        print(message)
        server = smtplib.SMTP(SERVER)
        server.sendmail(FROM, TO, message)
        server.quit()
        print('Alerted by sending mail.')
    
def main():
    hp = Honeypot()
    hp.start_hp()

if __name__ == '__main__':
    main()
