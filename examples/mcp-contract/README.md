# Strict mock tool dispatcher, not a network MCP server

The intentionally tiny offline fixture checks role/tenant boundaries, strict input shapes, explicit write approval, replay-safe request keys and defensive response copies. No transport, auth provider, registry or third-party account is contacted.

Run: python -m unittest discover -s examples/mcp-contract -p "test_*.py" -v

**MCP compatibility NOT TESTED:** the fixture models tool boundary concepts, not MCP JSON-RPC methods, client/server transport, identity provider or token lifecycle. To certify a real MCP connector, use the current official protocol conformance suite and real supported clients in an authorized environment.
