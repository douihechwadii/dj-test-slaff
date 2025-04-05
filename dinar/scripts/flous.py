import re
from functools import lru_cache

@lru_cache(maxsize=None)
def parse_log_entry(log_entry):
    log_dict = {}
    
    pattern = r'(\w+)="([^"]*)"|(\w+)=([^\s]+)'
    
    for match in re.finditer(pattern, log_entry):
        key = match.group(1) or match.group(3)
        value = match.group(2) or match.group(4)
        
        # Convert numeric values where applicable
        if value.isdigit():
            value = int(value)
        elif value.replace('.', '', 1).isdigit():  # Check for float values
            value = float(value)

        log_dict[key] = value

    return log_dict


def convert_logs_to_json(input_file):
    logs = []

    with open(input_file, "r") as file:
        for line in file:
            log_dict = parse_log_entry(line.strip())  # Ensure parse_log_entry exists
            logs.append(log_dict)

    return logs  # Return list of logs instead of writing to a file
