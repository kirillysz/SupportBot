from os import getenv
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

TOKEN = getenv("TOKEN")
HOST = getenv("HOST")
ADMIN_IDS = getenv("ADMINS_IDS")