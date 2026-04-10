from mcp.server.fastmcp import FastMCP
from netmiko import ConnectHandler
import os
import re

mcp = FastMCP("network-tools")

def get_connection():
    """Helper function to create device connection"""
    device = {
        "device_type": "arista_eos",
        "host": os.getenv("DEVICE_HOST", "localhost"),
        "port": int(os.getenv("DEVICE_PORT", "2201")),
        "username": os.getenv("DEVICE_USERNAME", "admin"),
        "password": os.getenv("DEVICE_PASSWORD", "admin"),
        "secret": os.getenv("DEVICE_PASSWORD", "admin"),  # Enable password
        "session_log": "netmiko_session.log",  # Debug logging
    }
    conn = ConnectHandler(**device)
    conn.enable()  # Enter privileged mode
    return conn

@mcp.tool()
async def get_device_info() -> str:
    """Get basic device information including hostname, version, and uptime"""
    with get_connection() as conn:
        output = conn.send_command("show version")
    return output

@mcp.tool()
async def get_interfaces() -> str:
    """List all interfaces with their status, speed, and descriptions"""
    with get_connection() as conn:
        output = conn.send_command("show interfaces status")
    return output

@mcp.tool()
async def get_routes() -> str:
    """Show the routing table with all routes"""
    with get_connection() as conn:
        output = conn.send_command("show ip route")
    return output

@mcp.tool()
async def get_running_config() -> str:
    """Retrieve the current running configuration"""
    with get_connection() as conn:
        output = conn.send_command("show running-config")
    return output


@mcp.tool()
async def configure_interface(
    interface: str,
    ip_address: str,
    subnet_mask: str,
    description: str = ""
) -> str:
    """Configure an IP address on a network interface.
    
    Args:
        interface: Interface name (e.g., Ethernet1, Management0)
        ip_address: IP address to assign (e.g., 10.0.1.1)
        subnet_mask: Subnet mask (e.g., 255.255.255.0)
        description: Optional interface description
    """
    # INPUT VALIDATION
    if not re.match(r"^[A-Za-z]+[\d/\.]+$", interface):
        return "Error: Invalid interface name format"
    
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip_address):
        return "Error: Invalid IP address format"
    
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", subnet_mask):
        return "Error: Invalid subnet mask format"
    
    # Calculate CIDR from subnet mask
    cidr = sum([bin(int(x)).count('1') for x in subnet_mask.split('.')])
    
    commands = [
        f"interface {interface}",
        f"no switchport",
        f"ip address {ip_address}/{cidr}",
    ]
    
    if description:
        commands.insert(2, f"description {description}")
    
    commands.append("no shutdown")
    
    try:
        conn = get_connection()
        output = conn.send_config_set(commands)
        conn.send_command("write memory")
        verify = conn.send_command(f"show running-config interface {interface}")
        conn.disconnect()
        
        return f"Configuration applied!\n\nCommands:\n{chr(10).join(commands)}\n\nVerification:\n{verify}"
    
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def add_static_route(
    destination: str,
    subnet_mask: str,
    next_hop: str
) -> str:
    """Add a static route to the routing table.
    
    Args:
        destination: Destination network (e.g., 192.168.10.0)
        subnet_mask: Subnet mask (e.g., 255.255.255.0)
        next_hop: Next hop IP address (e.g., 10.0.1.2)
    """
    # INPUT VALIDATION
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", destination):
        return "Error: Invalid destination network format"
    
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", subnet_mask):
        return "Error: Invalid subnet mask format"
    
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", next_hop):
        return "Error: Invalid next hop IP format"
    
    # Calculate CIDR from subnet mask
    cidr = sum([bin(int(x)).count('1') for x in subnet_mask.split('.')])
    
    commands = [
        f"ip route {destination}/{cidr} {next_hop}"
    ]
    
    try:
        conn = get_connection()
        
        # First check if IP routing is enabled
        ip_routing_check = conn.send_command("show running-config | include ip routing")
        if "ip routing" not in ip_routing_check:
            conn.disconnect()
            return "Error: IP routing is not enabled. Please enable it first with 'ip routing' command."
        
        output = conn.send_config_set(commands)
        conn.send_command("write memory")
        
        # Verify the route was added
        verify = conn.send_command(f"show ip route {destination}")
        all_static = conn.send_command("show ip route static")
        
        conn.disconnect()
        
        return f"Static route configuration output:\n{output}\n\nRoute verification:\n{verify}\n\nAll static routes:\n{all_static}"
    
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()