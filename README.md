# XPO Kortrijk Ticket Bot

Telegram Bot that generates valid parking tickets for XPO Kortrijk P2.

## Motivation

Laziness

## Installation

### Add your Telegram API Token, base and end to a .env file

- Current base: 540513002
- Current end: 515

### Build Docker image from source

```bash
docker build -t xpo_kortrijk_ticket_bot_container .
```

### Run Docker image

```bash
docker run --env-file=<.your env file> -dit xpo_kortrijk_ticket_bot_container
```

## Usage

```bash
python bot.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
