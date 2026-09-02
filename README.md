# ibkr-mcp

Read-only Cursor / Agent Plugin wrapper around Interactive Brokers' **official remote MCP**.

This package does **not** run a local MCP server, stdio proxy, or OAuth client. It points Cursor at IBKR's streamable-http endpoint. OAuth is client-managed.

Official IBKR docs (paste the MCP URL into any MCP-capable client, including Cursor):
https://www.interactivebrokers.com/en/trading/ai-integrations.php

MCP URL: `https://api.ibkr.com/v1/api/mcp-public`

## What this is for

A **read-only desk consumer**: NAV, cash, positions, weights, optional TWR when a live tool exists. See `skills/ibkr-account-snapshot/SKILL.md`.

It is **not** for placing, modifying, or cancelling orders.

## Install (local, unpublished)

Grok Bot / cloud agents do **not** load `~/.cursor/plugins/local`. Cursor IDE does.

Clone https://github.com/TheRealM4rtin/ibkr-mcp, then:

```bash
mkdir -p ~/.cursor/plugins/local
cp -a ibkr-mcp ~/.cursor/plugins/local/ibkr-mcp
```

The install path must be a **real directory** (copied files), not a symlink whose target is outside `~/.cursor/plugins/local`.

Then enable the plugin in Cursor's plugin / Customize UI. This repository is not published and should not be added via `AddMcpServer` as a substitute for the plugin.

## MCP config

`mcp.json` declares a single streamable-http server:

- `type`: `streamable-http`
- `url`: `https://api.ibkr.com/v1/api/mcp-public`

Agent Plugins 1.0.0 has **no OAuth fields** in `mcp.json`. Optional `headers` must be literal, non-secret values. This plugin sends **no headers and no secrets**.

## OAuth (client-managed)

IBKR protects the MCP resource (RFC 9728):

- Resource: `https://api.ibkr.com/v1/api/mcp-public`
- Authorization servers: `https://api.ibkr.com/oauth2`
- Scopes supported: `mcp.read`, `mcp.write`
- Bearer method: header

Request **mcp.read only**. Do not request `mcp.write`.

Authorization server (from IBKR OAuth metadata):

- Issuer: `https://api.ibkr.com`
- Authorization: `https://api.ibkr.com/oauth2/authorize`
- Token: `https://api.ibkr.com/oauth2/api/v1/token`
- Registration: `https://api.ibkr.com/oauth2/register`
- Scopes include: `openid`, `profile`, `email`, `account-ids`, `mcp.read`, `mcp.write`
- `token_endpoint_auth_methods_supported` includes `none`
- PKCE: S256

Do not invent a `CLIENT_ID` or embed tokens in this plugin.

### Cursor redirect URIs

Cursor dynamic client registration (DCR) with a `cursor://` redirect URI is **rejected by IBKR**.

Documented allowed callbacks:

- `https://www.cursor.com/agents/mcp/oauth/callback`
- `http://localhost:8787/callback`
- `http://127.0.0.1:8787/callback`

Complete OAuth in the Cursor client using an allowed callback. This plugin cannot complete OAuth for you.

## Safety

- No secrets in the repo or in `mcp.json`
- No order placement
- Skill maps only verified `get_account_summary` / `get_account_positions` fields; other tool names (including TWR) are discovered at runtime
- If auth fails, stop; do not invent balances

## License

MIT. Copyright (c) 2026 Martin.
