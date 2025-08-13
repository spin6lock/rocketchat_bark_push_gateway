# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Rocket.Chat to Bark Push Gateway that acts as a middleware between Rocket.Chat push notifications and the Bark notification service (and ntfy). It's based on the immanuelfodor/rocketchat-push-gateway project but modified to work with Bark on non-standard ports, addressing issues with apprise.

## Architecture

The application consists of three main Python modules:

- **push.py**: Flask web server that exposes the `/push/<service>/send` endpoint, mimicking the RocketChat push gateway API
- **notify.py**: Core notification logic that handles both Bark and ntfy push services with "do not disturb" time period support
- **config.py**: Configuration file containing tokens, host URLs, port settings, and do-not-disturb schedules

## Configuration

- Copy `config.py.example` to `config.py` and update with your settings
- `tokens` dict maps RocketChat push tokens to Bark device IDs
- `dont_disturb_hours` configures quiet hours per token
- `host` is the Bark server URL
- `ntfy_host` is the ntfy server URL

## Development Commands

### Running the Application
```bash
# Run directly with Python
python3 push.py

# Run with Docker
docker build -t rocketchat-push-gateway .
docker run -p 5050:5050 rocketchat-push-gateway
```

### Testing
```bash
# Test ntfy functionality directly
python3 notify.py
```

### Dependencies
```bash
pip install -r requirements.txt
```

## Key Components

### Push Gateway (push.py:11-41)
The main Flask route `/push/<service>/send` accepts POST requests with RocketChat notification payloads and forwards them to the notification system.

### Notification Handler (notify.py:18-44)
The `notify()` function processes notifications with time-sensitive/passive level handling based on configured do-not-disturb periods, then sends to both Bark and ntfy services.

### Dual Push Support (notify.py:9-16, notify.py:40-44)
The system pushes to both Bark (for iOS) and ntfy services simultaneously for redundancy.

## Current Git Status

The repository is on branch `json_notify` with modifications to `notify.py` - appears to be implementing JSON-based ntfy requests with click functionality for RocketChat integration.