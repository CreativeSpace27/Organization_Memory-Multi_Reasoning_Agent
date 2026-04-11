import os
from dotenv import load_dotenv

load_dotenv()

SERP_API_KEY = os.getenv("SERP_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

STACK_API_BASE = "https://api.stackexchange.com/2.3/search/advanced"
GITHUB_API_BASE = "https://api.github.com/search/issues"

TRUSTED_DOMAINS = [
    "developer.mozilla.org",
    "aws.amazon.com",
    "cloud.google.com",
    "learn.microsoft.com",
    "postgresql.org",
    "mongodb.com",
    "kubernetes.io"
]

REDIS_URL = "redis://localhost:6379"