---
name: ibkr-account-snapshot
description: Use when the user wants a read-only Interactive Brokers account snapshot (NAV, cash, positions, weights, or TWR). Do not use for placing, modifying, or cancelling orders.
---

# IBKR account snapshot

Produce a single **IbkrAccountSnapshot** from the official IBKR remote MCP. Do not invent numbers, tool names, or payloads.

```
IbkrAccountSnapshot = {
  asOf,
  accountId,
  nav,
  cash,
  currency,
  positions: [{ symbol, qty, marketValue, weight }],
  twrDaily: [{ date, twr }]
}
```

## Auth and scope

OAuth is **client-managed** (Agent Plugins 1.0.0 has no OAuth fields in `mcp.json`). Prefer **mcp.read**. Do not request **mcp.write**.

If authentication fails, is missing, or the user cannot complete OAuth: **stop**. Report that the snapshot cannot be built. Do not guess balances, retry with write scopes, or fall back to fabricated data.

## Discover tools at runtime

List the MCP server's tools before calling any. Do **not** assume a complete catalog.

Look for these known tools (names verified; field names below are verified):

- `get_account_summary` — keys include `net_liquidation`, `total_cash_value`, `currency`, `available_funds`, `buying_power`
- `get_account_positions` — keys include `symbol`, `position`, `market_value`, `market_price`, `avg_cost`, `currency`, `contract_id`, `sec_type`, `unrealized_pnl`

Other tool names, including any TWR / time-weighted-return tool, are **unknown**. If a listed tool's name and description clearly provide TWR (or the other snapshot fields), use it. If none matches, leave that snapshot field empty or omit it. Never invent a tool name or call payload.

## Map onto IbkrAccountSnapshot

Fill only from tool results. Leave a field absent or null when the source is missing.

| Snapshot field | Source |
| --- | --- |
| `asOf` | Timestamp of the successful read (ISO 8601). Do not backdate. |
| `accountId` | Account identifier returned by the tools, if present. |
| `nav` | `net_liquidation` from `get_account_summary`. |
| `cash` | `total_cash_value` from `get_account_summary`. |
| `currency` | `currency` from `get_account_summary`. |
| `positions[].symbol` | `symbol` |
| `positions[].qty` | `position` |
| `positions[].marketValue` | `market_value` |
| `positions[].weight` | Derive only: `marketValue / nav` when both exist and `nav` is non-zero. Otherwise omit `weight`. |
| `twrDaily` | Fill only if a discovered tool actually returns dated TWR. Do not invent a TWR tool or series. |

Do not populate extra trading fields into the snapshot unless the user asked. Extra keys from the tools (`available_funds`, `buying_power`, `market_price`, `avg_cost`, `unrealized_pnl`, `contract_id`, `sec_type`, position `currency`) may be cited in prose, but they are not required snapshot fields.

## Hard rules

- Never invent numbers, positions, dates, or account IDs.
- Never call write, order, trade-instruction, or other mutating tools.
- Never place, modify, or cancel orders.
- Never pass a `CLIENT_ID` or invent OAuth / API payloads.
- This plugin wraps the official remote streamable-http MCP; there is no local stdio OAuth proxy.
