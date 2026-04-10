# mcp-work-tools

MCP server aggregating tools for EC work services — GitLab, Confluence (phase 2), and others.

Built as a permanent replacement for `@modelcontextprotocol/server-gitlab` (npm), which had fragile `node_modules` patches. This server lives in a versioned repository, has only the tools actually needed (principle of least privilege), and is easy to extend with new services.

## Services

| Service | Status | Tools |
|---------|--------|-------|
| GitLab (`sdlc.webcloud.ec.europa.eu`) | Phase 1 — active | `gitlab_get_issue`, `gitlab_create_issue_note`, `gitlab_create_merge_request`, `gitlab_list_merge_requests` |
| Confluence | Phase 2 — planned | — |

## Setup

```bash
git clone git@github.com:infowhere-be/mcp-work-tools.git ~/desenvolvimento/private/mcp-work-tools
cd ~/desenvolvimento/private/mcp-work-tools

python3 -m venv .venv
.venv/bin/pip install "mcp[cli]>=1.0.0" "httpx>=0.27.0"
```

Add to `~/.infowhere-secrets.env`:

```bash
export GITLAB_API_KEY="glpat-..."
```

## Claude Code Integration

Add to `.mcp.json` in the project:

```json
{
  "mcpServers": {
    "gitlab": {
      "command": "/home/tavalea/desenvolvimento/private/mcp-work-tools/.venv/bin/python3",
      "args": ["/home/tavalea/desenvolvimento/private/mcp-work-tools/server.py"],
      "env": {
        "GITLAB_API_URL": "https://sdlc.webcloud.ec.europa.eu/api/v4",
        "GITLAB_PERSONAL_ACCESS_TOKEN": "${GITLAB_API_KEY}"
      }
    }
  }
}
```

`${GITLAB_API_KEY}` is substituted at runtime from the shell environment (sourced from `~/.infowhere-secrets.env`).

## Project Structure

```
mcp-work-tools/
├── server.py          # Entry point — registers all tools
├── tools/
│   ├── gitlab.py      # GitLab tools
│   └── confluence.py  # Confluence tools (phase 2)
└── pyproject.toml
```

## Adding a New Service

1. Create `tools/<service>.py` with a `register(mcp)` function
2. Add required env vars to `~/.infowhere-secrets.env`
3. Add env vars to `.mcp.json`
4. Call `<service>.register(mcp)` in `server.py`

## Notes

- `verify=False` on all HTTPS calls — the EC GitLab instance uses an internal certificate not trusted by the system CA bundle
- Tools are intentionally minimal: no file writes to GitLab, no repository creation/deletion
