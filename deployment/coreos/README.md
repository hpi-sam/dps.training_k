# Fedora CoreOS Deployment

If you do not want to set up a Fedora CoreOS, we recommend using this 
[Guide](../../docs/deployment-process.md) to set up the application using docker-compose.

## Overview of the CoreOS Setup

- Podman Quadlet units for all production containers
- journald retention limits so logs do not grow without bound
  - Podman's default container log driver is `journald`, so this also bounds container logs
- SSH hardening, e.g. allowing only public key auth 
- firewalld enabled with only `ssh`, `http`, and `https` exposed
- automatic container updates via `podman-auto-update.timer`
- automatic OS updates via Zincati with an explicit weekend reboot window
  - OS reboot window pinned to Sunday 04:00-06:00 `Europe/Berlin` time
- automatic Let's Encrypt bootstrap and renewal via `certbot` standalone in a container
  - certificate renewal timer pinned to Saturday 03:00 `Europe/Berlin` time

## Before Generating Ignition

Edit the placeholders in [config.bu](config.bu):

- the secrets in `/etc/kdps/.env.prod`
- the SSH public key for the `core` user

The CoreOS deployment hardcodes the production TLS domain to `klinik-dps.de`.
If you want to run on a different domain, replace all occurrences before generating an Ignition file.
The bootstrap certificate contact email is also hardcoded to `admin@example.com` in `kdps-bootstrap-cert.sh`.

As long as the GHCR images are private, the host needs persistent registry credentials on first boot.
This setup expects them in `deployment/coreos/secrets/ghcr-config.json`, which gets written to `/root/.docker/config.json`.

One easy way to create that file locally is:

```bash
mkdir -p deployment/coreos/secrets
echo "$GHCR_TOKEN" | podman login \
  --authfile deployment/coreos/secrets/ghcr-config.json \
  --username YOUR_GITHUB_USERNAME \
  --password-stdin \
  ghcr.io
```

Use a GitHub token with `read:packages`. Keep that file out of version control.

## Generate Ignition

Install `butane`, then run:

```bash
butane --pretty --strict deployment/coreos/config.bu > deployment/coreos/config.ign
```

To embed that Ignition config into a Fedora CoreOS ISO:

```bash
coreos-installer iso customize \
  --live-ignition deployment/coreos/config.ign \
  --output deployment/coreos/kdps-coreos.iso \
  <fedora-coreos.iso>
```

You can then boot your server from that ISO. Everything should start up automatically, but may need a few minutes. 
