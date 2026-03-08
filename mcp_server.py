#!/usr/bin/env python3
"""MCP server exposing Claude Code Starter Kit commands and agents as tools.

Commands are exposed as ``command_<name>`` tools.
Agents are exposed as ``agent_<name>`` tools.
Each tool accepts an optional ``arguments`` string (file paths, flags, etc.)
and returns the corresponding prompt with ``$ARGUMENTS`` substituted.
"""

import asyncio
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# ---------------------------------------------------------------------------
# Locate bundled data (works both in the repo and when pip-installed)
# ---------------------------------------------------------------------------
_HERE = Path(__file__).parent
_COMMANDS_DIR = _HERE / ".claude" / "commands"
_AGENTS_DIR = _HERE / ".claude" / "agents"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Return (metadata_dict, body) parsed from YAML-style frontmatter."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta: dict[str, str] = {}
    for line in parts[1].strip().splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip()] = val.strip().strip('"')
    return meta, parts[2].strip()


def _load_tools() -> dict[str, dict[str, str]]:
    """Load all command and agent markdown files into a name→info mapping."""
    tools: dict[str, dict[str, str]] = {}

    if _COMMANDS_DIR.exists():
        for path in sorted(_COMMANDS_DIR.glob("*.md")):
            meta, body = _parse_frontmatter(path.read_text())
            raw_name = meta.get("name", path.stem)
            tool_name = f"command_{raw_name.replace('-', '_')}"
            tools[tool_name] = {
                "description": meta.get(
                    "description", f"Claude Code command: {raw_name}"
                ),
                "prompt": body,
            }

    if _AGENTS_DIR.exists():
        for path in sorted(_AGENTS_DIR.glob("*.md")):
            meta, body = _parse_frontmatter(path.read_text())
            raw_name = meta.get("name", path.stem)
            tool_name = f"agent_{raw_name.replace('-', '_')}"
            tools[tool_name] = {
                "description": meta.get(
                    "description", f"Claude Code agent: {raw_name}"
                ),
                "prompt": body,
            }

    return tools


_TOOLS = _load_tools()

# ---------------------------------------------------------------------------
# MCP server
# ---------------------------------------------------------------------------

server = Server("claude-code-starter-kit-mcp")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name=name,
            description=info["description"],
            inputSchema={
                "type": "object",
                "properties": {
                    "arguments": {
                        "type": "string",
                        "description": (
                            "Optional arguments for the tool "
                            "(e.g. a file path or flags like --changed, --dry-run)."
                        ),
                    }
                },
            },
        )
        for name, info in _TOOLS.items()
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name not in _TOOLS:
        raise ValueError(f"Unknown tool: {name!r}")

    prompt = _TOOLS[name]["prompt"]
    args = (arguments or {}).get("arguments", "").strip()

    if args:
        result = prompt.replace("$ARGUMENTS", args)
    else:
        result = prompt.replace("$ARGUMENTS", "").strip()

    return [TextContent(type="text", text=result)]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

async def _run() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def main() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    main()
