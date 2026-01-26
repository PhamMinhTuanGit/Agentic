from netmiko import ConnectHandler, redispatch
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
MID_DEVICE_TYPE = os.getenv('MID_DEVICE_TYPE', 'linux')
MID_DEVICE_IP = os.getenv('MID_DEVICE_IP', '')
MID_DEVICE_USERNAME = os.getenv('MID_DEVICE_USERNAME', '')
MID_DEVICE_PASSWORD = os.getenv('MID_DEVICE_PASSWORD', '')
END_DEVICE_IP = os.getenv('END_DEVICE_IP', '')
END_DEVICE_USERNAME = os.getenv('END_DEVICE_USERNAME', '')
END_DEVICE_PASSWORD = os.getenv('END_DEVICE_PASSWORD', '')

# Thông tin Hop A (Thường là một máy chủ Linux hoặc Gateway)
ssh_jump_host = {
    'device_type': MID_DEVICE_TYPE,
    'host': MID_DEVICE_IP,
    'username': MID_DEVICE_USERNAME,
    'password': MID_DEVICE_PASSWORD,
}

# Thông tin Thiết bị B (ZebOS Router)
telnet_target = {
    'ip': END_DEVICE_IP,
    'user': END_DEVICE_USERNAME,
    'pass': END_DEVICE_PASSWORD,
    'terminal_prompt': r'[>#]' # Dấu nhắc lệnh đặc trưng của ZebOS
}

def connect_zebos_multihop(commands=None):
    try:
        # 1. Kết nối SSH đến Hop A
        print(f"--- Đang kết nối SSH tới Jump Host: {ssh_jump_host['host']} ---")
        connection = ConnectHandler(**ssh_jump_host)

        # 2. Thực hiện lệnh Telnet từ Hop A sang B
        print(f"--- Đang Telnet từ A sang ZebOS B ({telnet_target['ip']}) ---")
        connection.write_channel(f"telnet {telnet_target['ip']}\n")
        time.sleep(2)
        
        # Xử lý đăng nhập ZebOS
        # Lưu ý: ZebOS có thể hỏi 'login:' hoặc 'Username:'
        try:
            output = connection.read_until_pattern(pattern=r"login:|Username:", read_timeout=5)
            print(f"[DEBUG] Login prompt: {output}")
        except:
            output = connection.read_channel()
            print(f"[DEBUG] Prompt (no pattern): {output}")
        
        connection.write_channel(telnet_target['user'] + "\n")
        time.sleep(1)
        
        try:
            output = connection.read_until_pattern(pattern=r"Password:", read_timeout=5)
            print(f"[DEBUG] Password prompt: {output}")
        except:
            output = connection.read_channel()
            print(f"[DEBUG] Output after user: {output}")
        
        connection.write_channel(telnet_target['pass'] + "\n")
        time.sleep(2)
        
        # Read initial output
        output = connection.read_channel()
        print(f"[DEBUG] After login: {output}")
        
        print("--- Đã vào đến Shell của ZebOS ---")

        # 4. Gửi lệnh kiểm tra (ZebOS dùng lệnh tương tự Cisco)
        commands_full = [
            "imish",
            "enable"
        ]
        commands_full.extend(commands if commands else [])
        for cmd in commands_full:
            print(f"\n✓ Đang thực thi: {cmd}")
            try:
                # Use write_channel + read_channel instead of send_command
                connection.write_channel(cmd + "\n")
                time.sleep(1)
                output = connection.read_channel()
                print(output)
            except Exception as e:
                print(f"  Lỗi lệnh: {e}")
        
        # 5. Thoát
        connection.write_channel("exit\n")
        connection.disconnect()
        print("\n--- Kết thúc phiên làm việc ---")

    except Exception as e:
        print(f"❌ Lỗi hệ thống: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    connect_zebos_multihop()