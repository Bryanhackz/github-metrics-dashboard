# GitHub Metrics Dashboard

## Problem
Developers and open-source maintainers need a fast, secure way to monitor repository health without exposing API tokens to the client, dealing with CORS, or hitting rate limits.

## Solution
A zero-dependency Python WSGI backend acting as a secure proxy to the GitHub API. It implements a SQLite-based caching layer to respect rate limits, and a pure Vanilla JS/CSS frontend that renders visual analytics using native CSS transitions.

## Stack
- Backend: Python 3.11+ (`wsgiref`, `urllib`, `sqlite3`)
- Frontend: Vanilla HTML5, CSS3, ES Modules
- No external dependencies, no Docker, no build steps.

## Setup
```bash
python server.py
```
Open `http://localhost:8000`.

## Architectural decisions
- **Proxy Architecture:** The frontend never communicates directly with GitHub. All requests go through the backend, which handles User-Agent headers, preventing CORS issues and protecting rate limits.
- **SQLite Cache over Redis:** To maintain the zero-dependency philosophy, SQLite acts as a persistent cache with a 15-minute TTL. This avoids requiring a separate Redis server while still protecting the external API.
- **CSS-based Charts:** Instead of importing a heavy charting library from a CDN (which may be blocked in enterprise environments), the dashboard uses native CSS transitions to render proportional bars.
- **Proxy Awareness:** The backend uses `urllib`, which natively respects the system's `HTTP_PROXY` and `HTTPS_PROXY` environment variables, making it robust in restricted corporate networks.

- ## Security Posture (CSP)
The application is served via a WSGI backend that enforces a strict Content Security Policy. The exact headers are defined in `security/headers.py`:
- `script-src 'self'` (No inline JavaScript; ES modules are loaded externally)
- `style-src 'self' 'unsafe-inline'` (Permits dynamic CSS for dashboard bar animations)
- `connect-src 'self'` (Restricts fetch requests to the local backend proxy)
- `frame-ancestors 'none'` (Prevents clickjacking)
