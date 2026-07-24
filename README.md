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
(`typesenseServerConfig` in `docusaurus.config.ts`), over plain **HTTP** on
port `8108`. The search API key embedded in the built site is a public,
search-only key (it's shipped in client-side JS, same as any DocSearch-style
integration), so there's no secret to protect and no TLS requirement.
To develop or test the search integration locally, run a local Typesense
instance via Docker Compose.

### 1. Configure an API key

```bash
echo "TYPESENSE_API_KEY=some-local-dev-key" > docker/typesense/.env
```

### 2. Start Typesense

```bash
cd docker/typesense
docker compose up -d
```

Verify it's up:

```bash
curl -s http://localhost:8108/health
# {"ok":true}
```

### 3. Point Docusaurus at the local server

Create a `.env` file in the repository root (git-ignored):

```bash
TYPESENSE_API_KEY=some-local-dev-key
TYPESENSE_HOST=localhost
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
```

`docusaurus.config.ts` reads `TYPESENSE_HOST`/`TYPESENSE_PORT`/`TYPESENSE_PROTOCOL`
from the environment, defaulting to the production values
(`docs.operaton.org`, `8108`, `http`) when unset.

### 4. Populate the index and run the site

Index some content into the `docusaurus` collection (for example with the
same [`docsearch.config.json`](./docsearch.config.json) and the
[`typesense-scraper`](https://github.com/celsiusnarhwal/typesense-scraper)
tooling used in CI, pointed at your local dev server), then start Docusaurus
as usual:

```bash
npm run start
```

### Optional: testing over HTTPS

To test the search integration over HTTPS instead (e.g. if the production
server's TLS setup ever changes), generate a self-signed certificate and
layer on the TLS override:

```bash
./docker/typesense/generate-certs.sh
docker compose -f docker-compose.yml -f docker-compose.tls.yml up -d
```

Since the certificate is self-signed, browsers will show a security warning
for `https://localhost:8108` the first time — open that URL directly once and
accept the exception, or add the certificate to your system/browser trust
store.

### Background: issue #161

Search on the production site failed because `docusaurus.config.ts` was
configured to connect over HTTPS while the Typesense server at
`docs.operaton.org:8108` only ever served plain HTTP — the TLS handshake
fails before any CORS headers can be returned, which browsers surface as a
CORS error. Confirmed via direct query against the production server (over
HTTP, using the public search key from the deployed site) that the
`docusaurus` collection is indexed correctly (15k+ documents, real search
results) — only the protocol mismatch was broken. The fix is to keep
`docusaurus.config.ts` and the scraper step in
`.github/workflows/deploy.yml` on `protocol: http`, matching the server.
