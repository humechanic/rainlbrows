"""
Environment variables configuration module.

Loads variables from .env file in project root or from system environment.
Environment variables take precedence over .env file values.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Get project root directory (parent of 'app' directory)
project_root = Path(__file__).parent.parent

# Load .env file from project root if it exists
env_file = project_root / '.env'
if env_file.exists():
    load_dotenv(dotenv_path=env_file, override=False)
else:
    # Also try loading from current directory (for backward compatibility)
    load_dotenv(override=False)

# Telegram Bot Token
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')

# Payment Provider Token
PAYMENT_PROVIDER_TOKEN = os.getenv('PAYMENT_PROVIDER_TOKEN', '')

# Database URL
# Format: postgresql+psycopg://user:password@host:port/database
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql+psycopg://postgres:postgres@localhost:5432/rainlbrows'
)

# BePaid Payment Links
BEPAID_PAYMENT_URL_WITHOUT_PROMO = os.getenv(
    'BEPAID_PAYMENT_URL_WITHOUT_PROMO',
    'https://api.bepaid.by/products/prd_cee1ddcb25a5526f/pay'
)
BEPAID_PAYMENT_URL_WITH_PROMO = os.getenv(
    'BEPAID_PAYMENT_URL_WITH_PROMO',
    'https://api.bepaid.by/products/prd_e96afb3851f78d9d/pay'
)

# Validate required variables
if not TELEGRAM_TOKEN:
    raise ValueError(
        "TELEGRAM_TOKEN is not set. Please set it in .env file or environment variables."
    )

if not PAYMENT_PROVIDER_TOKEN:
    raise ValueError(
        "PAYMENT_PROVIDER_TOKEN is not set. Please set it in .env file or environment variables."
    )


