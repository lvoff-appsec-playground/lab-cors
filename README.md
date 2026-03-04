# Lvoff Sec Labs – CORS Playground

This repo contains a minimal, local Docker Compose lab for experimenting with CORS misconfigurations,
CSRF vs CORS behavior, and sensitive header exposure.

# WARNING
(!) This is intentionally vulnerable and must never be used in production.

## Quick Start

1) Add local hostnames:

```
127.0.0.1 api.local
127.0.0.1 attacker.local
127.0.0.1 trusted.local
```

2) Create local HTTPS certificates (mkcert). Install `mkcert` via your package manager first:

```
mkcert -install
mkcert -cert-file ./nginx/certs/local.pem -key-file ./nginx/certs/local-key.pem api.local attacker.local trusted.local localhost
```

3) Create a local env file:

```
cp .env.example .env
```

4) Build and run:

```
docker compose up --build
```

5) Open the attacker UI:

```
https://attacker.local/
```

## CORS Scenarios

Available scenarios (set via env or `/admin/config`):

- `lab1_reflect_basic_origin`: reflect any origin, allow credentials
- `lab2_trusted_null_origin`: allow `Origin: null` with credentials
- `allow_all`: worst-case configuration (reflect + null + credentials + broad headers)
- `hardened`: most restrictive (no origins allowed)

## Notes / Defaults

- Cookies are controlled via environment variables in `.env`.
- Defaults use `COOKIE_SAMESITE=None` and `COOKIE_SECURE=true` for HTTPS testing.
- Browsers enforce `SameSite=None` + `Secure`. If cookies are blocked, verify you are using HTTPS and your local CA is trusted.
- Requests to `http://api.local` redirect to `https://api.local`.
- `COOKIE_HTTPONLY` is configurable and can be changed at runtime via `/admin/config`.

## API Endpoints

- `GET https://api.local/login` sets a dummy session cookie (`sid`)
- `GET https://api.local/me` returns sensitive JSON only if `sid` is present
- `POST https://api.local/notes` JSON-only endpoint requiring a custom header (`X-Api-Key` or `X-Requested-With`)
- `POST https://api.local/transfer` form-friendly state change (simple request)
- `GET https://api.local/transfer-legacy` intentionally unsafe state change via GET
- `GET https://api.local/transfers` returns transfers for the current user and requires a custom header
  (e.g. `X-Client-Version: 1` and/or `X-Api-Key`)
- `GET https://api.local/account-meta` returns sensitive info in custom response headers
- `GET https://api.local/admin/transfers` lists all transfers (requires `sid=admin`)
- `GET https://api.local/admin/config` admin UI for runtime config
- `POST https://api.local/admin/config` updates runtime config (requires `sid=admin`)

## Attacker UI

Open `https://attacker.local/` to trigger:
- Cross-origin `fetch` to `/me`
- Preflighted `/notes` and `/transfers` requests using custom headers
- Sensitive header exfiltration from `/account-meta`
- CSRF-style form POST to `/transfer`
- Legacy GET state change via `/transfer-legacy` using both `fetch` and image load

## Data Storage

Transfers are stored in SQLite under the API service. Seed data is created on first run.

## Project Structure

- `docker-compose.yml` orchestrates all services
- `nginx/nginx.conf` routes hosts to services
- `services/api` is the victim API (FastAPI)
- `services/attacker` serves the exploit UI
- `services/trusted_http` is a placeholder trusted origin
