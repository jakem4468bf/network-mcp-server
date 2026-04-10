from netmiko import ConnectHandler

device = {
    "device_type": "arista_eos",
    "host": "localhost",
    "port": 2201,
    "username": "admin",
    "password": "admin",
}

print("Testing connection...")
with ConnectHandler(**device) as conn:
    output = conn.send_command("show version")
    print(output)
    
print("\n\nTesting interfaces...")
with ConnectHandler(**device) as conn:
    output = conn.send_command("show ip interface brief")
    print(output)