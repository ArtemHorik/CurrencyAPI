import os
import pathlib

from dotenv import load_dotenv

# Loading env variables
path = pathlib.Path(__file__).parent.parent
dotenv_path = path.joinpath('.env')
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)


class Config:
    API_KEY = os.getenv("API_KEY")

    # DATABASE_URL = f'postgresql+asyncpg://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}' \
    #                f'@{os.getenv("POSTGRES_HOST", "localhost")}' \
    #                f':{os.getenv("POSTGRES_PORT", 5432)}/{os.getenv("POSTGRES_DB")}'
    # DATABASE_URL = 'postgresql+asyncpg://postgres:1337@localhost/horik'
    DATABASE_URL = os.getenv("DATABASE_URL")

