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

    DATABASE_URL = os.getenv("DATABASE_URL")

