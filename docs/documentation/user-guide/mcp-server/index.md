---

title: "MCP Server"
sidebar_position: 170

---
# Operaton MCP Server

The [Operaton MCP server](https://github.com/operaton/operaton-mcp) connects AI assistants to the Operaton process engine. It implements the [Model Context Protocol (MCP)](https://modelcontextprotocol.io), an open protocol through which AI assistants such as Claude call external tools.

The server exposes more than 300 operations of the [Operaton REST API](../../reference/rest/index.md) as MCP tools. An assistant can use them to deploy processes and decisions, start and inspect process instances, work on user tasks, handle failed jobs and incidents, query history and migrate process instances between definition versions.

## How It Works

The MCP client (for example Claude Desktop) starts the MCP server as a local process and communicates with it over standard input and output. The MCP server translates each tool call into a request to the Operaton REST API and returns the response to the assistant.

```
AI assistant ── MCP ──▶ Operaton MCP server ── HTTP ──▶ Operaton REST API ──▶ Process engine
```

The MCP server does not store process data. All operations run with the permissions of the configured Operaton user or OIDC client, so the [authorization](../process-engine/authorization-service.md) settings of the engine apply.

## Features

- Coverage of the Operaton REST API for process definitions, deployments, process instances, tasks, jobs, incidents, users and groups, history, decisions and migration.
- Authentication with HTTP Basic or OAuth2 client credentials (OIDC).
- Access control guards that restrict which operations the assistant can see and call.
- No installation step required: MCP clients start the server with `npx`.

## Limitations

The current release does not provide:

- Autonomous monitoring, i.e. the assistant does not watch processes or raise alerts on its own.
- Generation of BPMN models from natural language.
- Prompt templates for guided scenarios.
- A user interface. The MCP server is used only through an MCP client.

## Further Reading

- [Install the Operaton MCP server](../../installation/mcp-server.md)
- [Configuration](configuration.md)
- [Capabilities and examples](capabilities.md)
