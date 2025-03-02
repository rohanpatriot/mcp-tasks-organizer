"""
Tasks Organizer MCP Server entry point.
Run with: python -m tasks_organizer
"""

from .server import mcp

if __name__ == "__main__":
    print("Starting Tasks Organizer MCP Server...")
    mcp.run(transport='stdio') 