---

title: "Operaton MCP Server"
sidebar_position: 30
description: "Install the Operaton MCP server to connect AI assistants to the Operaton REST API"

---
# Install the Operaton MCP Server

The [Operaton MCP server](https://github.com/operaton/operaton-mcp) is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that exposes the Operaton REST API to AI assistants such as Claude. It is published on npm as [`@operaton/mcp`](https://www.npmjs.com/package/@operaton/mcp).

See the [User Guide](../user-guide/mcp-server/index.md) for an overview, the [configuration reference](../user-guide/mcp-server/configuration.md) and the available tools.

## Prerequisites

- [Node.js](https://nodejs.org) 22 or later
- A running Operaton instance with the [REST API](../reference/rest/index.md) reachable from the machine running the MCP server, for example `http://localhost:8080/engine-rest`

## Installation

The MCP server does not need to be installed separately. MCP clients start it on demand with `npx`:

```shell
npx -y @operaton/mcp
```

Alternatively, install it globally. This provides the `operaton-mcp` command:

```shell
npm install -g @operaton/mcp
```

## Register the Server in an MCP Client

MCP clients start the server as a local process and pass the configuration as environment variables. The following example registers the server in Claude Desktop. Edit the configuration file:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "operaton": {
      "command": "npx",
      "args": ["-y", "@operaton/mcp"],
      "env": {
        "OPERATON_BASE_URL": "http://localhost:8080/engine-rest",
        "OPERATON_USERNAME": "demo",
        "OPERATON_PASSWORD": "demo"
      }
    }
  }
}
```

Restart Claude Desktop afterwards. Other MCP clients use the same `command`, `args` and `env` settings in their own configuration format.

The [Configuration](../user-guide/mcp-server/configuration.md) page in the User Guide describes the setup in detail: all environment variables, OIDC authentication, configuration files and access control guards.

On startup, the server checks that the Operaton REST API is reachable and exits with an error if it is not.

:::note[Credentials]
The example uses the `demo` user of the Operaton distributions. For anything other than a local test installation, use a dedicated user with the minimum required permissions and restrict the server with [access control guards](../user-guide/mcp-server/configuration.md#access-control-guards).
:::

## Next Steps

- [Configure](../user-guide/mcp-server/configuration.md) authentication, multiple engines and access control guards.
- Browse the [available tools and example prompts](../user-guide/mcp-server/capabilities.md).
