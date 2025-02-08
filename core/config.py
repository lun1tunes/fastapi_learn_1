from pathlib import Path
from pydantic_settings import BaseSettings

# На случай, если каждый раз таблица создается заного
BASE_DIR = Path(__file__).parent.parent


class Setting(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    # db_url: str = f"sqlite+aiosqlite:///./db.sqlite3"
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    # db_echo: bool = False
    db_echo: bool = True


settings = Setting()
