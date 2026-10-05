#!/usr/bin/env python3
"""Snapshot the live Flaim MCP tool definitions and server instructions.

Calls the public MCP endpoint without authentication (initialize, then
tools/list) and writes:

  tools/tools.json        tools sorted by name, pretty-printed
  tools/instructions.md   the server instructions returned by initialize

The server stamps the current date into some descriptions. Those dates are
replaced with a fixed placeholder so the snapshot only changes when the
wording does.

Refuses to write if the instructions are empty, a tool is incomplete, or the
tool count goes down. Set ALLOW_TOOL_REMOVAL=true when a removal is real.

Usage: python3 scripts/snapshot_tools.py [output-dir]   (default: tools)
"""

import datetime
import json
import os
import re
import sys
import tempfile
import urllib.request

ENDPOINT = os.environ.get("FLAIM_MCP_URL", "https://api.flaim.app/mcp")
PROTOCOL_VERSION = "2025-06-18"
DATE_PLACEHOLDER = "YYYY-MM-DD"
USER_AGENT = "flaim-fantasy-snapshot/1.0 (+https://github.com/jdguggs10/flaim-fantasy)"


def post(payload, session_id=None):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "MCP-Protocol-Version": PROTOCOL_VERSION,
        "User-Agent": USER_AGENT,
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        body = response.read().decode("utf-8")
        content_type = response.headers.get("Content-Type", "")
        new_session = response.headers.get("Mcp-Session-Id")
    return body, content_type, new_session


def parse_messages(body, content_type):
    """Return the JSON-RPC messages in a plain JSON or SSE-framed body."""
    if "text/event-stream" not in content_type:
        if not body.strip():
            return []
        parsed = json.loads(body)
        return parsed if isinstance(parsed, list) else [parsed]

    messages = []
    data_lines = []
    for line in body.splitlines() + [""]:
        if line.startswith("data:"):
            data_lines.append(line[5:].lstrip(" "))
        elif line == "":
            if data_lines:
                messages.append(json.loads("\n".join(data_lines)))
                data_lines = []
    return messages


def rpc(method, params, request_id, session_id=None):
    payload = {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params}
    body, content_type, new_session = post(payload, session_id)
    for message in parse_messages(body, content_type):
        if message.get("id") == request_id:
            if "error" in message:
                raise RuntimeError(f"{method} failed: {message['error']}")
            return message["result"], new_session or session_id
    raise RuntimeError(f"{method}: no response with id {request_id}")


def stabilize_dates(text):
    """Replace server-injected current dates with a placeholder."""
    text = re.sub(
        r"(Current date is )\d{4}-\d{2}-\d{2}", r"\g<1>" + DATE_PLACEHOLDER, text
    )
    # Belt and braces: any other copy of today's date (allowing for time
    # zones) is also treated as injected.
    today = datetime.datetime.now(datetime.timezone.utc).date()
    for offset in (-1, 0, 1):
        day = (today + datetime.timedelta(days=offset)).isoformat()
        text = text.replace(day, DATE_PLACEHOLDER)
    return text


def stabilize(value):
    if isinstance(value, str):
        return stabilize_dates(value)
    if isinstance(value, list):
        return [stabilize(item) for item in value]
    if isinstance(value, dict):
        return {key: stabilize(item) for key, item in value.items()}
    return value


def check_snapshot(tools, instructions, out_dir):
    """Refuse to write a snapshot that looks broken."""
    problems = []
    if not instructions.strip():
        problems.append("initialize returned no server instructions")
    if not tools:
        problems.append("tools/list returned no tools")
    for index, tool in enumerate(tools):
        for field in ("name", "description", "inputSchema"):
            if not tool.get(field):
                problems.append(f"tool #{index} ({tool.get('name', '?')}) has no {field}")

    existing_path = os.path.join(out_dir, "tools.json")
    if os.path.exists(existing_path):
        with open(existing_path, encoding="utf-8") as handle:
            previous = len(json.load(handle))
        allow_removal = os.environ.get("ALLOW_TOOL_REMOVAL", "").lower() == "true"
        if len(tools) < previous and not allow_removal:
            problems.append(
                f"tool count dropped from {previous} to {len(tools)}; if a tool was "
                "really removed, rerun with ALLOW_TOOL_REMOVAL=true (the "
                "allow_tool_removal input on a manual run)"
            )

    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        raise SystemExit("Snapshot not written.")


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "tools"

    init_result, session_id = rpc(
        "initialize",
        {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": "flaim-fantasy-snapshot", "version": "1.0.0"},
        },
        1,
    )
    # Courtesy notification per the MCP lifecycle; the response body is unused.
    post({"jsonrpc": "2.0", "method": "notifications/initialized"}, session_id)

    tools = []
    cursor = None
    request_id = 2
    while True:
        params = {"cursor": cursor} if cursor else {}
        result, session_id = rpc("tools/list", params, request_id, session_id)
        tools.extend(result.get("tools", []))
        cursor = result.get("nextCursor")
        request_id += 1
        if not cursor:
            break

    tools = stabilize(sorted(tools, key=lambda tool: tool.get("name", "")))
    instructions = stabilize_dates(init_result.get("instructions") or "").rstrip("\n")
    check_snapshot(tools, instructions, out_dir)

    # Write both files to a temp dir first, then move them into place, so a
    # failure part way never leaves a half-written snapshot.
    os.makedirs(out_dir, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=out_dir, prefix=".snapshot-") as staging:
        staged_tools = os.path.join(staging, "tools.json")
        staged_instructions = os.path.join(staging, "instructions.md")
        with open(staged_tools, "w", encoding="utf-8") as handle:
            json.dump(tools, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        with open(staged_instructions, "w", encoding="utf-8") as handle:
            handle.write(
                "<!-- Generated daily from the live Flaim MCP server's initialize response. "
                "Do not edit; suggest wording changes with an issue. -->\n\n"
            )
            handle.write(instructions + "\n")
        os.replace(staged_tools, os.path.join(out_dir, "tools.json"))
        os.replace(staged_instructions, os.path.join(out_dir, "instructions.md"))

    print(f"Wrote {len(tools)} tools and {len(instructions)} characters of instructions to {out_dir}/")


if __name__ == "__main__":
    main()
