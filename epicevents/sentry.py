import sentry_sdk
import os
from dotenv import load_dotenv

load_dotenv()

DSN = os.getenv("DSN")

sentry_sdk.init(dsn=DSN)
