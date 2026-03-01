# Lvoff Sec Labs – CORS Playground (Phase 1)

This repo contains a minimal, local Docker Compose lab for experimenting with CORS misconfigurations.
Phase 1 implements a basic API with session cookies, a single CORS scenario, and an attacker UI.

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

## Lab 1 Behavior

Scenario: `lab1_reflect_basic_origin`

- Reflects any Origin
- Allows credentials
- Sets `Vary: Origin`
- Allows methods: `GET, POST, OPTIONS`
- Allows headers: `Content-Type, X-Requested-With, X-Api-Key`

## Notes / Defaults

- Cookies are controlled via environment variables in `.env`.
- Defaults use `COOKIE_SAMESITE=None` and `COOKIE_SECURE=true` for HTTPS testing.
- Browsers enforce `SameSite=None` + `Secure`. If cookies are blocked, verify you are using HTTPS and your local CA is trusted.
- Requests to `http://api.local` redirect to `https://api.local`.

## Phase 1 Endpoints

- `GET https://api.local/login` sets a dummy session cookie (`sid`)
- `GET https://api.local/me` returns sensitive JSON only if `sid` is present

## Project Structure

- `docker-compose.yml` orchestrates all services
- `nginx/nginx.conf` routes hosts to services
- `services/api` is the victim API (FastAPI)
- `services/attacker` serves the exploit UI
- `services/trusted_http` is a placeholder trusted origin
