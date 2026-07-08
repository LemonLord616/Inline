#!/bin/bash

## I use this to export our ai token, this token is then used by opencode app

KEY_FILE="$HOME/.keys/skald.api"

if [ ! -f "$KEY_FILE" ]; then
    echo "Error: Key file not found at $KEY_FILE" >&2
    return 1 2>/dev/null || exit 1
fi

SKALD_API_KEY=$(cat "$KEY_FILE" | tr -d '\n\r' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

if [ -z "$SKALD_API_KEY" ]; then
    echo "Error: Key file is empty" >&2
    return 1 2>/dev/null || exit 1
fi

export SKALD_API_KEY


echo "Skald API key loaded successfully"
