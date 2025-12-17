# Rainlbrows Telegram Bot

Telegram bot for beauty master sales intensive with payment integration and reminder system.

## Features

- User registration and offer management
- Payment integration with promocodes
- Automatic reminder system for expiring offers
- PostgreSQL database for data persistence

## Requirements

- Python 3.8+
- PostgreSQL database
- Telegram Bot Token
- Payment Provider Token (for payments)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd rainlbrows
```

2. Create and activate virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment:
   Edit `app/env.py` and set:

- `TELEGRAM_TOKEN` - Your Telegram bot token
- `PAYMENT_PROVIDER_TOKEN` - Your payment provider token
- `DATABASE_URL` - PostgreSQL connection string (format: `postgresql+psycopg://user:password@host:port/database` for psycopg3, or `postgresql://user:password@host:port/database` for auto-detection)

Example:

```python
DATABASE_URL = 'postgresql://postgres:password@localhost:5432/rainlbrows'
```

4. Set up PostgreSQL database:

```bash
# Create database
createdb rainlbrows

# Or using psql:
psql -U postgres
CREATE DATABASE rainlbrows;
```

5. Activate virtual environment (if not already activated):

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

6. Initialize database tables:
   The database tables will be created automatically on first bot startup.

## Running the Bot

### Main Bot Application

**Important**: Make sure virtual environment is activated before running:

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Run the main bot:

```bash
cd app
python main.py
```

### Scheduler (Reminder System)

The scheduler sends reminder messages to users about expiring offers. Run it periodically (e.g., every 6 hours or daily at 10:00 AM).

#### Option 1: Manual execution

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
cd app
python run_scheduler.py
```

#### Option 2: Using cron (Linux/Mac)

Add to crontab (`crontab -e`):

```bash
# Run every 6 hours
0 */6 * * * /path/to/python /path/to/app/run_scheduler.py

# Or run daily at 10:00 AM
0 10 * * * /path/to/python /path/to/app/run_scheduler.py
```

#### Option 3: Using systemd timer (Linux)

Create a systemd service and timer for automated execution.

## Database Schema

### Users Table

- `id` - Primary key
- `telegram_id` - Unique Telegram user ID
- `nickname` - Telegram username
- `first_name` - User's first name
- `last_name` - User's last name
- `is_premium_tg_user` - Telegram Premium status
- `created_at` - Registration timestamp

### Offers Table

- `id` - Primary key
- `user_id` - Foreign key to users table
- `offer_expiration_date` - When the offer expires
- `last_reminder_sent` - Timestamp of last reminder
- `is_active` - Whether offer is still active
- `reminder_type` - Type of last reminder ('last_call' or None)
- `created_at` - Offer creation timestamp

## Reminder System

The scheduler checks for two types of reminders:

1. **Last Call Reminder**: Sent 24-48 hours before offer expiration
2. **Regular Reminder**: Sent every 48 hours (if offer expires in more than 48 hours)

## Project Structure

```
app/
├── db/                 # Database models and session
│   ├── base.py         # SQLAlchemy Base
│   ├── session.py      # Database session
│   ├── models.py       # User and Offer models
│   ├── repository.py   # Database operations
│   └── init_db.py      # Database initialization
├── modules/            # Bot modules
│   ├── init/          # Start command
│   ├── payment/       # Payment handling
│   ├── main_menu/     # Main menu
│   └── ...
├── scheduler/         # Reminder scheduler
│   └── reminders.py  # Reminder processing
├── main.py           # Main bot application
└── run_scheduler.py  # Scheduler entry point
```

## Development

### Database Migrations

For production, consider using Alembic for database migrations:

```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Troubleshooting

### Database Connection Issues

- Verify PostgreSQL is running
- Check `DATABASE_URL` format
- Ensure database exists and user has permissions

### Scheduler Not Sending Messages

- Check scheduler logs
- Verify bot token is correct
- Ensure database is accessible
- Check that offers exist and are active

## License

[Your License Here]
