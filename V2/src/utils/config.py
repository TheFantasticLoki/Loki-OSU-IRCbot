from dataclasses import dataclass
from pathlib import Path
import yaml
from typing import Optional

@dataclass
class OsuConfig:
    client_id: str
    client_secret: str

@dataclass
class IrcConfig:
    token: str
    nickname: str
    server: str = "irc.ppy.sh"
    port: int = 6667

@dataclass
class DatabaseConfig:
    url: str
    
@dataclass
class Config:
    osu: OsuConfig
    irc: IrcConfig
    database: DatabaseConfig

def load_config(path: Path) -> Config:
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
        
    if not path.exists():
        template = """# OSU IRC Bot Configuration

osu:
    # Get these credentials from https://osu.ppy.sh/home/account/edit#oauth
    client_id: ''  
    client_secret: ''

irc:
    # Get IRC token from https://osu.ppy.sh/home/account/edit in Legacy API (Can't find the correct #tag to nav to it)
    # server password is your token
    token: ''
    # Your osu! username
    nickname: ''
    # Default osu! IRC server settings
    server: 'irc.ppy.sh'
    port: 6667

database:
    # Database connection URL
    # Examples:
    # SQLite: 'sqlite://data/bot.db'
    # MySQL: 'mysql://user:pass@localhost/dbname'
    url: ''
"""
        
        with open(path, 'w') as f:
            f.write(template)
            
        print(f"Created template config file at {path}. Please fill out the required values and run again.")
        exit(1)
        
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
        
    return Config(
        osu=OsuConfig(**data['osu']),
        irc=IrcConfig(**data['irc']),
        database=DatabaseConfig(**data['database'])
    )
