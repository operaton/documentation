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

Search on the production site originally failed because `docusaurus.config.ts`
was configured to connect over HTTPS while the Typesense server at
`docs.operaton.org:8108` only ever served plain HTTP — the TLS handshake
fails before any CORS headers can be returned, which browsers surface as a
CORS error. The first fix switched the client config to `protocol: http` to
match the server.

That traded one broken state for another: `docs.operaton.org` is served over
HTTPS, and browsers block an HTTPS page from making a plain-HTTP XHR request
to anything ("mixed content"), regardless of whether the server would have
answered correctly. Search still failed in a real browser — silently, with no
network request even showing up in devtools, only a `Mixed Content` console
error and an `ERR_NETWORK` from the Typesense client. A visible symptom of
the same root cause: the "See all N results" footer in the search modal
stayed stuck on the literal `{count}` placeholder, because `nbHits` never
got populated. A direct `curl` against the production server (over HTTP,
using the public search key) had confirmed the `docusaurus` collection was
indexed correctly (15k+ documents) — that check bypasses the browser's
mixed-content policy, so it didn't catch this.

The actual fix: nginx on `docs.operaton.org` reverse-proxies `/typesense/` to
the local Typesense container (`proxy_pass http://127.0.0.1:8108/`), so the
browser talks to Typesense same-origin over HTTPS. `docusaurus.config.ts`
defaults to `protocol: https`, `port: 443`, `path: /typesense` accordingly.
Local dev keeps talking to the Docker Typesense instance directly — see
`.env` above, which sets `TYPESENSE_PROTOCOL=http`, `TYPESENSE_PORT=8108`,
and `TYPESENSE_PATH=` (empty, no proxy prefix) to override those defaults.
The CI scraper step in `.github/workflows/deploy.yml` is unaffected: it runs
on a GitHub Actions runner, not in a browser, so it keeps talking to
`docs.operaton.org:8108` directly over plain HTTP — mixed content is a
browser-only restriction.
