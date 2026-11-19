---

title: "Configuration"
sidebar_position: 10

---
# Configuration

The Operaton MCP server is configured through environment variables, which the MCP client passes to the server process. Use one of the following modes:

- **Basic Auth** through environment variables
- **OIDC** (OAuth2 client credentials) through environment variables
- **Configuration file** through `OPERATON_CONFIG`, for example to keep several engines in one file

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPERATON_CONFIG` | No | – | Path to a JSON configuration file. If set, all other `OPERATON_*` variables except `OPERATON_SKIP_HEALTH_CHECK` and the guard variables are ignored. |
| `OPERATON_BASE_URL` | Yes¹ ² | – | URL of the Operaton REST API, e.g. `http://localhost:8080/engine-rest` |
| `OPERATON_USERNAME` | Yes¹ | – | Basic Auth username |
| `OPERATON_PASSWORD` | Yes¹ | – | Basic Auth password |
| `OPERATON_CLIENT_ID` | Yes² | – | OAuth2 client ID |
| `OPERATON_CLIENT_SECRET` | Yes² | – | OAuth2 client secret |
| `OPERATON_TOKEN_URL` | Yes² | – | Token endpoint of the identity provider |
| `OPERATON_ENGINE` | No | `default` | Name of the process engine addressed in REST API paths |
| `OPERATON_SKIP_HEALTH_CHECK` | No | `false` | Set to `true` to skip the connectivity check on startup |
| `OPERATON_GUARD` | No | `unrestricted` | Overall guard mode, see [Access Control Guards](#access-control-guards) |
| `OPERATON_DENY_RESOURCES` | No | – | Resource domains to deny, see [Access Control Guards](#access-control-guards) |
| `OPERATON_DENY_OPS` | No | – | Operation classes to deny, see [Access Control Guards](#access-control-guards) |

¹ Required for Basic Auth without a configuration file.
² Required for OIDC without a configuration file.

Without a configuration file, Basic Auth and OIDC variables are mutually exclusive. If both `OPERATON_USERNAME` and `OPERATON_CLIENT_ID` are set, the server does not start.

## Basic Auth

Use Basic Auth for local or internal Operaton installations that authenticate REST API calls with username and password:

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

## OIDC

Use OIDC for Operaton installations secured by an OAuth2 identity provider such as Keycloak. The server fetches access tokens with the client credentials grant, caches them and refreshes them 30 seconds before they expire.

```json
{
  "mcpServers": {
    "operaton": {
      "command": "npx",
      "args": ["-y", "@operaton/mcp"],
      "env": {
        "OPERATON_BASE_URL": "https://operaton.example.com/engine-rest",
        "OPERATON_CLIENT_ID": "mcp-client",
        "OPERATON_CLIENT_SECRET": "your-client-secret",
        "OPERATON_TOKEN_URL": "https://keycloak.example.com/realms/myapp/protocol/openid-connect/token"
      }
    }
  }
}
```

## Configuration File

A JSON configuration file describes one or more engines, each with its own URL and authentication:

```json
{
  "engines": {
    "dev": {
      "url": "http://localhost:8080/engine-rest",
      "authentication": {
        "type": "basic",
        "username": "demo",
        "password": "demo"
      }
    },
    "quality-stage": {
      "url": "https://operaton-qa.example.com/engine-rest",
      "default": true,
      "authentication": {
        "type": "oidc",
        "clientId": "mcp-client",
        "clientSecret": "your-secret",
        "tokenUrl": "https://keycloak.example.com/realms/qa/protocol/openid-connect/token"
      }
    }
  }
}
```

Reference the file with `OPERATON_CONFIG`:

```json
{
  "mcpServers": {
    "operaton": {
      "command": "npx",
      "args": ["-y", "@operaton/mcp"],
      "env": {
        "OPERATON_CONFIG": "/Users/yourname/operaton-config.json"
      }
    }
  }
}
```

### Default Engine

All tool calls go to the default engine. The other engines in the file are not used. To work with a different engine, mark it as default and restart the MCP client. Alternatively, register the server several times in the MCP client, each with its own configuration file or environment variables.

The default engine is determined as follows:

- If the file contains a single engine, it is the default engine.
- If the file contains several engines, exactly one of them must have `"default": true`.

If several engines are configured and none or more than one is marked as default, the server does not start.

## Access Control Guards

Guards restrict which operations the assistant may perform. They are enforced in the MCP server, so blocked calls never reach Operaton.

Guards act on two levels:

1. Forbidden tools are removed from the tool list. The assistant does not see them and cannot propose to use them.
2. If a forbidden tool is called anyway, the server rejects the call. The MCP client receives an error that names the blocked operation and the rule that triggered, and the server logs a warning.

Guards complement the [authorization](../process-engine/authorization-service.md) settings of the engine; they do not replace them.

### Guard Mode

`OPERATON_GUARD` sets the overall mode:

| Value | Effect |
|---|---|
| `unrestricted` (default) | All operations are permitted. |
| `read-only` | Only read operations are permitted. |
| `safe` | Read operations and reversible changes are permitted. Irreversible operations (delete, deploy, execute migration) are blocked. |

:::tip
Use `OPERATON_GUARD=safe` for production systems. The assistant can still start process instances, complete tasks and manage jobs, but it cannot delete definitions or execute migrations.
:::

### Deny Resource Domains

`OPERATON_DENY_RESOURCES` takes a comma-separated list of resource domains. Both read and write operations in these domains are blocked.

Valid domains: `process-definitions`, `deployments`, `instances`, `tasks`, `jobs`, `incidents`, `users-groups`, `decisions`, `migrations`, `infrastructure`

```json
"env": {
  "OPERATON_DENY_RESOURCES": "users-groups,decisions"
}
```

### Deny Operation Classes

`OPERATON_DENY_OPS` takes a comma-separated list of operation classes, which are blocked in all domains.

Valid classes: `read`, `create`, `update`, `delete`, `suspend-resume`, `deploy`, `migrate-execute`, `migrate-control`

```json
"env": {
  "OPERATON_DENY_OPS": "delete,deploy"
}
```

### Combining Guards

All three variables can be set together. The most restrictive matching rule wins. The rules are evaluated in the order `OPERATON_GUARD`, `OPERATON_DENY_RESOURCES`, `OPERATON_DENY_OPS`.

## Security Recommendations

:::warning
Never commit credentials or configuration files containing secrets to version control.
:::

- Prefer environment variables or a secrets manager over credentials in configuration files.
- If a configuration file contains credentials, exclude it from version control and restrict its file permissions, e.g. `chmod 600 ~/operaton-config.json`.
- Use a dedicated Operaton user or OIDC client with the minimum required permissions.
- Set `OPERATON_SKIP_HEALTH_CHECK=true` only in development and test environments. The startup check detects connectivity problems early.

## Troubleshooting

| Error message | Cause | Fix |
|---|---|---|
| `No configuration found. Provide one of: ...` | None of `OPERATON_CONFIG`, `OPERATON_USERNAME` or `OPERATON_CLIENT_ID` is set | Set the variables for your authentication mode. |
| `Missing required environment variables: OPERATON_BASE_URL` | `OPERATON_BASE_URL` is missing | Set `OPERATON_BASE_URL`. |
| `Ambiguous authentication config: ...` | Both Basic Auth and OIDC variables are set | Use one authentication mode only, or use a configuration file. |
| `Config file not found: ...` | `OPERATON_CONFIG` points to a file that does not exist | Check the path. |
| `Failed to parse config file: ...` | The configuration file is not valid JSON | Fix the JSON syntax. |
| `Multiple engines configured but none marked as default` | No engine has `"default": true` | Mark exactly one engine as default. |
| `Multiple engines marked as default` | More than one engine has `"default": true` | Keep `"default": true` on one engine only. |
| `OIDC token fetch failed: HTTP 401 from ...` | Wrong client ID or secret | Check the OIDC credentials with your identity provider. |
| `Cannot reach Operaton at ...` | The startup connectivity check failed | Check `OPERATON_BASE_URL` and that Operaton is reachable. |
