from f2b_parser import parse


def mainloop(logfile: str) -> None:
    try:
        with open(logfile) as f:
            for line in f:
                parsed_data = parse(line)
                print(parsed_data)
                    
    except KeyboardInterrupt as msg:
        print('Ctrl+C Pressed. Shutdown')
        exit(0)


def main() -> None:
    logfile = '/Users/padiynn/Projects/biblab/telegram/fail2ban-notify/fail2ban.log'
    mainloop(logfile)


if __name__ == '__main__':
    main()
