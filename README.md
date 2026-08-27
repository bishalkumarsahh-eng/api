# ElevenYTS Universal Provider API v4

This API is compatible with the uploaded ElevenYTS bot:

GET /download?url=<id>&type=audio|video&api_key=<key>

Unlike the previous placeholder version, this version can proxy an **authorized upstream media provider** that returns the actual media bytes.

## Required Heroku Config Vars
API_KEY=your-secret
UPSTREAM_DOWNLOAD_URL=https://your-authorized-provider.example/download
UPSTREAM_API_KEY=provider-secret (only if required)

The upstream provider is fixed by environment configuration; clients cannot choose arbitrary URLs.

## Upstream request
The API forwards:
- url=<identifier>
- type=audio|video

and, if configured, adds:
- X-API-Key: UPSTREAM_API_KEY

The upstream must return HTTP 200 with playable media bytes.

## Status
GET /status shows whether the upstream provider is configured.

## Important
This project is a provider gateway. It does not bypass DRM, authentication challenges, or obtain media from sources you are not authorized to access.
