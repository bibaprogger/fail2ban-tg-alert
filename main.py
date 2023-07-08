#!/usr/bin/env python3
from f2b_parser import parse
import requests
import time
import os


LOGNAME = '/var/log/fail2ban.log'


def send_telegram_message(action: str, ip: str, dt: str) -> None:
    TOKEN = 'your token'
    CHAT_ID = 'your chat id'
    message = f'[ALERT] {dt} {action} {ip}'
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}'
    requests.post(url)


def tail(file) -> None:
    file.seek(0,2)
    inode = os.fstat(file.fileno()).st_ino

    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)
            if os.stat(LOGNAME).st_ino != inode:
                file.close()
                file = open(LOGNAME, 'r')
                inode = os.fstat(file.fileno()).st_ino
            continue
        yield line


def mainloop(logfile) -> None:
    for line in tail(logfile):
        parsed_data = parse(line)
        if parsed_data is not None:
                send_telegram_message(parsed_data['action'], parsed_data['ip'], parsed_data['dt'])



def main() -> None:
    logfile = open(LOGNAME, 'r')
    mainloop(logfile)


if __name__ == '__main__':
    main()
