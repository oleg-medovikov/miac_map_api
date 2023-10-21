from os import getenv
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv(dotenv_path=".conf")


@dataclass
class Settings:
    POSTGRESS_URL: str
    PRIVATE_KEY: str
    SSL_KEYFILE: str
    SSL_CERTFILE: str


settings = Settings(
    POSTGRESS_URL=getenv("POSTGRESS_URL", default=''),
    PRIVATE_KEY=getenv("PRIVATE_KEY", default=''),
    SSL_KEYFILE=getenv("SSL_KEYFILE", default=''),
    SSL_CERTFILE=getenv("SSL_CERTFILE", default=''),
)
