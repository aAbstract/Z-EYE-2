from dataclasses import dataclass
from datetime import datetime

@dataclass
class log():
    ''' log data model '''
    
    date: datetime
    level: str
    mod_id: str # module id
    description: str # log content

logs: list[log] = []

def _print_log(log_obj: log):
    print(f"[{log_obj.date.strftime('%Y-%m-%d %H:%M:%S')}] [{log_obj.level}] [{log_obj.mod_id}] | {log_obj.description}")

def add_log(mod_id: str, level: str, desc: str):
    ''' this fucntion addes info level log to the log buffer '''
    temp_log_obj = log(
        datetime.now(),
        level,
        mod_id,
        desc
    )
    _print_log(temp_log_obj)
    logs.append(temp_log_obj)
