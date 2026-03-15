#!/usr/bin/env bash
set -euo pipefail

CERTBOT_DOMAIN="klinik-dps.de"
CERTBOT_EMAIL="admin@example.com"

if [[ -f "/etc/letsencrypt/live/${CERTBOT_DOMAIN}/fullchain.pem" ]]; then
  exit 0
fi

podman run --rm --name kdps-certbot-bootstrap \
  -p 80:80 \
  -v /etc/letsencrypt:/etc/letsencrypt:Z \
  -v /var/lib/letsencrypt:/var/lib/letsencrypt:Z \
  docker.io/certbot/certbot:latest \
  certonly \
  --non-interactive \
  --agree-tos \
  --standalone \
  --email "${CERTBOT_EMAIL}" \
  -d "${CERTBOT_DOMAIN}"
