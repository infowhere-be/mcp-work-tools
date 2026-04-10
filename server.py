#!/usr/bin/env python3
"""mcp-work-tools — MCP server aggregating EC work service tools.

Services:
  - gitlab: GitLab (sdlc.webcloud.ec.europa.eu) — issues, MRs
  - confluence: Confluence EC (fase 2)
"""
from mcp.server.fastmcp import FastMCP
from tools import gitlab

mcp = FastMCP("work-tools")
gitlab.register(mcp)
# confluence.register(mcp)  # fase 2

if __name__ == "__main__":
    mcp.run()
