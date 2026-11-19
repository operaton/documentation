#!/usr/bin/env bash
# Generates a self-signed TLS certificate for the local Typesense dev server.
# Typesense terminates TLS itself (--ssl-certificate / --ssl-certificate-key),
# mirroring how the production server should be configured for port 8108.
set -euo pipefail

CERT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/certs"
mkdir -p "$CERT_DIR"

openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout "$CERT_DIR/key.pem" \
  -out "$CERT_DIR/cert.pem" \
  -days 825 \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

echo "Certificate written to $CERT_DIR/cert.pem"
echo "Key written to $CERT_DIR/key.pem"
echo
echo "Trust this certificate in your browser/OS keychain, or curl with --insecure, to avoid TLS warnings."
