from setuptools import setup, find_packages

setup(
    name="mcp-tasks-organizer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "mcp>=1.2.0",
        "markdown>=3.4.0",
    ],
    python_requires=">=3.10",
    author="Claude",
    description="An MCP server that converts Cursor agent plans to markdown task lists",
) 