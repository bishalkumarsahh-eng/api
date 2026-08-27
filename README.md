# ElevenYTS-Compatible Music API

Heroku-ready compatibility API designed around the uploaded ElevenYTS music bot.

## Compatible endpoint
The bot calls:

`GET /download?url=<video_id_or_url>&type=audio|video&api_key=<key>`

The endpoint is intentionally designed as a provider gateway. Configure an authorized media/catalog provider to supply playable content.

## Environment variables
- API_KEY
- ADMIN_KEY
- ALLOWED_ORIGINS=*
- RATE_LIMIT_PER_MINUTE=60
- MAX_PROVIDER_URL_AGE_SECONDS=900

## Bot configuration
Set:
- ARTISTBOTS_API_URL=https://YOUR-APP.herokuapp.com
- ARTISTBOTS_KEY=<API_KEY>
- ENABLE_API=True

## Important
The default provider is a safe placeholder and will return 501 until an authorized provider is configured. This project does not include DRM circumvention or unauthorized downloading.
