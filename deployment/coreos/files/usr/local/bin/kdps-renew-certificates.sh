#!/usr/bin/env bash
set -euo pipefail

systemctl stop kdps-nginx.service

renew_exit_code=0

# we catch exit code here because we want to start nginx again even if the renewal fails
podman run --rm --name kdps-certbot-renew \
  -p 80:80 \
  -v /etc/letsencrypt:/etc/letsencrypt:Z \
  -v /var/lib/letsencrypt:/var/lib/letsencrypt:Z \
  docker.io/certbot/certbot:latest \
  renew \
  --standalone \
  --quiet || renew_exit_code=$?

systemctl start kdps-nginx.service

exit "${renew_exit_code}"
