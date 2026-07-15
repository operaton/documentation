# Operaton Documentation

This repository contains the public documentation website for [Operaton](https://operaton.org/), built with [Docusaurus](https://docusaurus.io/).

## Requirements

- Node.js 18 or newer
- npm

## Install

```bash
npm ci
```

## Local Development

```bash
npm run start
```

This starts a local development server. Most content and styling changes are reflected without restarting the server.

## Build

```bash
npm run build
```

The static site is generated in the `build` directory.

## Typecheck

```bash
npm run typecheck
```

Run the typecheck and production build before opening a pull request.

## Local Search (Typesense) Setup

The production site queries a Typesense server directly from the browser
(`typesenseServerConfig` in `docusaurus.config.ts`), over **HTTPS** on port
`8108`. To develop or test the search integration locally — including
reproducing HTTPS/CORS issues like
[#161](https://github.com/operaton/documentation/issues/161) — run a local
Typesense instance with TLS enabled via Docker Compose.

### 1. Generate a local TLS certificate

```bash
./docker/typesense/generate-certs.sh
```

This creates a self-signed certificate/key in `docker/typesense/certs/`
(git-ignored). Typesense terminates TLS itself using this certificate,
the same way the production server must be configured.

### 2. Configure an API key

```bash
echo "TYPESENSE_API_KEY=some-local-dev-key" > docker/typesense/.env
```

### 3. Start Typesense

```bash
cd docker/typesense
docker compose up -d
```

Verify it's serving HTTPS correctly:

```bash
curl -sk https://localhost:8108/health
# {"ok":true}
```

### 4. Point Docusaurus at the local server

Create a `.env` file in the repository root (git-ignored):

```bash
TYPESENSE_API_KEY=some-local-dev-key
TYPESENSE_HOST=localhost
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=https
```

`docusaurus.config.ts` reads `TYPESENSE_HOST`/`TYPESENSE_PORT`/`TYPESENSE_PROTOCOL`
from the environment, defaulting to the production values
(`docs.operaton.org`, `8108`, `https`) when unset.

### 5. Populate the index and run the site

Index some content into the `docusaurus` collection (for example with the
same [`docsearch.config.json`](./docsearch.config.json) and the
[`typesense-scraper`](https://github.com/celsiusnarhwal/typesense-scraper)
tooling used in CI, pointed at your local dev server), then start Docusaurus
as usual:

```bash
npm run start
```

Since the certificate is self-signed, browsers will show a security warning
for `https://localhost:8108` the first time — open that URL directly once and
accept the exception, or add the certificate to your system/browser trust
store, before using the search box.

### Background: issue #161

Search on the production site failed because the Typesense server at
`docs.operaton.org:8108` only accepted plain HTTP, while the browser (per
`docusaurus.config.ts`) connects over HTTPS — the TLS handshake fails before
any CORS headers can be returned, which browsers surface as a CORS error.
This local setup demonstrates the fix: Typesense must terminate TLS on port
8108 (via `--ssl-certificate`/`--ssl-certificate-key`, as configured in
`docker/typesense/docker-compose.yml`), which is what needs to be replicated
on the production server.
