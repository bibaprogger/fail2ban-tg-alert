from dataclasses import InitVar, asdict, dataclass, field
import datetime 
from typing import Dict, Optional
import re

REGEX = r'(?P<dt>[0-9]{,4}-[0-9]{,2}-[0-9]{,2} [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}) ' \
        + r'fail2ban\.(?P<source>(observer|filter|actions)\s+) ' \
        + r'\[(?P<id>[0-9]+)\]: (?P<severity>(WARNING|NOTICE|INFO)\s+) ' \
        + r'\[(?P<service>.*)\] (?P<action>(Ban|Unban)) (?P<ip>(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b))'


PATTERN_FAIL2BAN = re.compile(REGEX)


ParseResultType = Dict[str, str]


@dataclass
class ParseResult:
        dt: str
        source: str
        id: str
        severity: str
        service: str
        action: str
        ip: str
        #dt_dt: datetime = field(init=False)

        #def __post_init__(self) -> None:
        #        self.dt_dt = datetime.datetime.strptime(self.dt, '%Y-%m-%d %H:%M:%S,%f')


        def to_dict(self) -> ParseResultType:
                return asdict(self)



def parse(line: str) -> Optional[ParseResultType]:
        match_  = re.search(PATTERN_FAIL2BAN, line)

        if match_ is not None:
                result = match_.groupdict()
                return ParseResult(**result).to_dict()
        else: 
                return None
        