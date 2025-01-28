from dataclasses import dataclass
from pathlib import Path
import yaml
from typing import Optional

@dataclass
class OsuConfig:
    """
    Configuration class for osu! OAuth credentials.
    
    Attributes:
        client_id (str): The OAuth client ID obtained from osu! website
        client_secret (str): The OAuth client secret obtained from osu! website
    """
    client_id: str
    client_secret: str

@dataclass
class IrcConfig:
    """
    Configuration class for IRC connection settings.
    
    Attributes:
        token (str): IRC token used for authentication with osu! IRC server
        nickname (str): The username to use in IRC chat
        server (str): IRC server address, defaults to 'irc.ppy.sh'
        port (int): IRC server port number, defaults to 6667
    """
    token: str
    nickname: str
    server: str = "irc.ppy.sh"
    port: int = 6667

@dataclass
class DatabaseConfig:
    """
    Configuration class for database connection settings.
    
    Attributes:
        url (str): Database connection URL string (supports SQLite and MySQL formats)
    """
    url: str
    
@dataclass
class Config:
    """
    Main configuration class that combines all config components.
    
    Attributes:
        osu (OsuConfig): osu! OAuth configuration settings
        irc (IrcConfig): IRC connection configuration settings
        database (DatabaseConfig): Database connection configuration settings
    """
    osu: OsuConfig
    irc: IrcConfig
    database: DatabaseConfig

def load_config(path: Path) -> Config:
    """
    Loads configuration from a YAML file or creates a template if it doesn't exist.
    
    Args:
        path (Path): Path to the configuration file
        
    Returns:
        Config: Parsed configuration object containing all settings
        
    Raises:
        SystemExit: If the config file doesn't exist and a template is created
        yaml.YAMLError: If the YAML file is malformed
        
    Notes:
        - If the config file doesn't exist, creates a template file and exits
        - Creates parent directories if they don't exist
        - Template includes examples and instructions for filling out values
    """
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