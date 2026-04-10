from mcp.server.fastmcp import FastMCP
from netmiko import ConnectHandler
import os

mcp = FastMCP("network-tools")

def get_connection():
    """Helper function to create device connection"""
    device = {
        "device_type": "arista_eos",
        "host": os.getenv("DEVICE_HOST", "localhost"),
        "port": int(os.getenv("DEVICE_PORT", "2201")),
        "username": os.getenv("DEVICE_USERNAME", "admin"),
        "password": os.getenv("DEVICE_PASSWORD", "admin"),
    }
    return ConnectHandler(**device)

@mcp.tool()
async def get_device_info() -> str:
    """Get basic device information including hostname, version, and uptime"""
    with get_connection() as conn:
        output = conn.send_command("show version")
    return output

@mcp.tool()
async def get_interfaces() -> str:
    """List all interfaces with their IP addresses and status"""
    with get_connection() as conn:
        output = conn.send_command("show ip interface brief")
    return output

if __name__ == "__main__":
    mcp.run()