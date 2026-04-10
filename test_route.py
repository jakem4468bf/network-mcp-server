from netmiko import ConnectHandler
import os

device = {
    "device_type": "arista_eos",
    "host": "localhost",
    "port": 2201,
    "username": "admin",
    "password": "admin",
    "secret": "admin",
}

conn = ConnectHandler(**device)
conn.enable()

print("Adding static route...")
output = conn.send_config_set(["ip route 192.168.10.0/24 10.0.1.2"])
print(output)

print("\nSaving config...")
conn.send_command("write memory")

print("\nVerifying route...")
verify = conn.send_command("show ip route static")
print(verify)

conn.disconnect()