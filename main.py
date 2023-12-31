#!/usr/bin/env python3
from log_parser import parse
import requests
import time
import os
from config import TOKEN, CHAT_ID, THREAD_ID


LOGNAME = '/var/log/fail2ban.log'


def send_to_telegram_topic(action: str, ip: str, dt: str) -> None:
    message = f'[ALERT] {dt} {action} {ip}'
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&message_thread_id={THREAD_ID}&text={message}'
    requests.get(url)


def send_to_telegram_chat(action: str, ip: str, dt: str) -> None:
    message = f'[ALERT] {dt} {action} {ip}'
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}'
    requests.get(url)


def tail(file):
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
                send_to_telegram_topic(parsed_data['action'], parsed_data['ip'], parsed_data['dt'])


def main() -> None:
    logfile = open(LOGNAME, 'r')
    mainloop(logfile)


if __name__ == '__main__':
    main()
