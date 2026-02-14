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

2) Create a local env file:

```
cp .env.example .env
```

3) Build and run:

```
docker compose up --build
```

4) Open the attacker UI:

```
http://attacker.local/
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
- Defaults use `COOKIE_SAMESITE=None` and `COOKIE_SECURE=false` for local HTTP testing.
- Some browsers enforce `SameSite=None` + `Secure`. If cookies are blocked, try a different browser or adjust cookie settings.

## Phase 1 Endpoints

- `GET http://api.local/login` sets a dummy session cookie (`sid`)
- `GET http://api.local/me` returns sensitive JSON only if `sid` is present

## Project Structure

- `docker-compose.yml` orchestrates all services
- `nginx/nginx.conf` routes hosts to services
- `services/api` is the victim API (FastAPI)
- `services/attacker` serves the exploit UI
- `services/trusted_http` is a placeholder trusted origin

