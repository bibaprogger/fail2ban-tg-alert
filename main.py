#!/usr/bin/env python3
from f2b_parser import parse
import requests
import time


def send_telegram_message(action: str, ip: str, dt: str) -> None:
    TOKEN = '5878794044:AAGQBZyT1NyN6JoFrt675EcHTMT-zrQlAZ4'
    CHAT_ID = '-879794776'
    message = f'[ALERT] {dt} {action} {ip}'
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}'
    requests.get(url)


def mainloop(logfile: str) -> None:
    try:
        with open(logfile, 'r') as f:
            f.seek(0, 2)
            while True:
                line = ''
                while len(line) == 0 or line[-1] != '\n':
                    tail = f.readline()
                    if tail == '':
                        time.sleep(0.1)
                        continue
                    line += tail
                parsed_data = parse(line)
                if parsed_data is not None:
                    send_telegram_message(parsed_data['action'], parsed_data['ip'], parsed_data['dt'])
    except KeyboardInterrupt as msg:
        print('Ctrl+C Pressed. Shutdown')
        exit(0)


def main() -> None:
    logfile = '/var/log/fail2ban.log'
    mainloop(logfile)


if __name__ == '__main__':
    main()
