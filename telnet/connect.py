import telnetlib
import time

HOST = "172.20.20.155"
PORT = 23

USERNAME = "root"      # ← sửa nếu khác
PASSWORD = "TTTD@1234%"   # ← sửa nếu khác

tn = telnetlib.Telnet(HOST, PORT, timeout=10)

# Chờ prompt login
tn.read_until(b"login: ")
tn.write(USERNAME.encode("ascii") + b"\n")

# Chờ prompt password
tn.read_until(b"Password: ")
tn.write(PASSWORD.encode("ascii") + b"\n")

# Đợi CLI sẵn sàng
time.sleep(1)

# ===== GỬI LỆNH CLI =====
tn.write(b"help\n")
tn.write(b"show status\n")

time.sleep(2)

# Đọc output
output = tn.read_very_eager().decode("ascii", errors="ignore")
print(output)

# Thoát
tn.write(b"exit\n")
tn.close()
