import os

# Check if we have the necessary api keys
MISSING_KEY_ERROR_MESSAGES = {
    "NEWS_API_KEY": (
        "Missing `NEWS_API_KEY` environment variable. "
        "This application requires an api key for newsapi.org"
    ),
    "COHERE_API_KEY": (
        "Missing `COHERE_API_KEY` environment variable. "
        "This application requires a developer api key from Cohere."
    ),
}

for key, msg in MISSING_KEY_ERROR_MESSAGES.items():
    try:
        _ = os.environ[key]
    except KeyError:
        raise ValueError(msg)
