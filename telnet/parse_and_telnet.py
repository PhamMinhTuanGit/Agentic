import telnetlib
import time
from telnet.connect import connect_zebos_multihop
def parse_config(config_text: str) -> list[str]:
    """Parse configuration text into individual commands"""
    # Extract content between triple backticks if present
    if '```' in config_text:
        parts = config_text.split('```')
        if len(parts) >= 3:
            config_text = parts[1]
    
    lines = config_text.strip().split('\n')
    commands = []
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            commands.append(line)
    
    return commands


# Example usage
if __name__ == "__main__":
    config = """configure terminal
interface xe48
 no shutdown
exit
router ospf 100
 network 192.168.1.0/24 area 0
 ip ospf cost 10
exit"""
    print(parse_config(config))
    connect_zebos_multihop(parse_config(config))