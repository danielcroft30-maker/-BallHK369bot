# Number Base Converter Bot

A Telegram bot that converts numbers between different bases (2-36).

## Features

- Convert numbers between any bases from 2 to 36
- User-friendly inline keyboard interface
- Supports binary, octal, decimal, hexadecimal, and more
- Simple command format: `<number> <from_base> <to_base>`

## Deployment on Railway

1. Push this repository to GitHub
2. Go to Railway.app → New Project → Deploy from GitHub
3. Add environment variable: `TELEGRAM_TOKEN` with your BotFather token
4. Railway automatically detects the `Procfile` and runs the bot as a worker

## Local Development

1. Create virtual environment: `python -m venv .venv`
2. Activate: `source .venv/bin/activate` (Windows: `.venv\Scripts\activate`)
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and add your token
5. Run: `python main.py`

## Bot Commands

- `/start` - Show welcome menu with inline buttons
- `/help` - Display usage instructions
- Or simply send: `<number> <from_base> <to_base>`

## Example

- `1010 2 10` → Converts binary 1010 to decimal (10)
- `FF 16 2` → Converts hex FF to binary (11111111)
- `42 10 16` → Converts decimal 42 to hex (2A)
