# Loki-OSU-IRC Bot V2

An advanced osu! IRC bot with multiplayer lobby management, PP calculation, and custom command capabilities.

## Core Features

- **Real-time PP Calculation**: Built-in PP calculator service for unranked maps
- **Multiplayer Lobby Management**: Automatic lobby tracking and management
- **Custom Commands System**: User-configurable command messages
- **Message Queue**: Rate-limited message handling to prevent spam
- **Database Integration**: Supports both SQLite and MySQL
- **Automatic Channel Management**: Remembers and rejoins channels after restart

## Command Categories

### Basic Commands
- `!stats [username]` - Show detailed osu! statistics for a user
- `!last/!r/!recent [username]` - Show latest play information
- `!socials`, `!collections`, `!skin`, `!about` - Customizable info commands

### Multiplayer Commands
- `!join <match_id>` - Join a multiplayer lobby
- `!start [countdown]` - Start match with optional countdown
- `!matchinfo` - Display detailed match statistics

### Configuration Commands
- `!addmsg <command> <index> <message>` - Add/update custom command messages
- `!delmsg <command> <index>` - Remove custom command messages

### Admin Commands
- `!listchannels` - List all active channels
- `!disablechannel <channel>` - Disable auto-rejoin for a channel

## Setup

1. Install dependencies:
```bash
setup.bat
