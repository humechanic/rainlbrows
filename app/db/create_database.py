"""
Script to create PostgreSQL database
Run this script to create the database before first bot startup
"""
import sys
import os

# Add app directory to path
app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, app_dir)

import subprocess
import env

# Database connection parameters from env.py
# Parse DATABASE_URL: postgresql+psycopg://user:password@host:port/database
db_url = env.DATABASE_URL

# Remove postgresql+psycopg:// or postgresql:// prefix
if "://" in db_url:
    db_url = db_url.split("://")[1]

# Parse connection string
if "@" in db_url:
    auth_part, host_db_part = db_url.split("@")
    if ":" in auth_part:
        db_user, db_password = auth_part.split(":")
    else:
        db_user = auth_part
        db_password = ""
    
    if "/" in host_db_part:
        host_port, db_name = host_db_part.split("/")
        if ":" in host_port:
            db_host, db_port = host_port.split(":")
        else:
            db_host = host_port
            db_port = "5432"
    else:
        db_host = host_db_part
        db_port = "5432"
        db_name = "rainlbrows"
else:
    print("Error: Invalid DATABASE_URL format")
    sys.exit(1)

print(f"Creating database '{db_name}' on {db_host}:{db_port}...")
print(f"User: {db_user}")

# Set PGPASSWORD environment variable for password
if db_password:
    os.environ['PGPASSWORD'] = db_password

try:
    # First, try to create user if it doesn't exist (for postgres user)
    if db_user == "postgres":
        try:
            # Try to connect as current system user to create postgres user
            create_user_cmd = [
                "psql",
                "-h", db_host,
                "-p", db_port,
                "-d", "postgres",
                "-tc", "SELECT 1 FROM pg_roles WHERE rolname = 'postgres'"
            ]
            result = subprocess.run(create_user_cmd, capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip() != "1":
                # User doesn't exist, create it
                print(f"Creating user '{db_user}'...")
                create_user_cmd = [
                    "psql",
                    "-h", db_host,
                    "-p", db_port,
                    "-d", "postgres",
                    "-c", f"CREATE USER {db_user} WITH SUPERUSER PASSWORD '{db_password}';"
                ]
                subprocess.run(create_user_cmd, check=True)
                print(f"User '{db_user}' created.")
        except subprocess.CalledProcessError:
            # If we can't create user, try to continue anyway
            print(f"Warning: Could not create user '{db_user}'. Trying to continue...")
    
    # Connect to PostgreSQL server (using 'postgres' database to create new database)
    # First, check if database exists
    check_db_cmd = [
        "psql",
        "-h", db_host,
        "-p", db_port,
        "-U", db_user,
        "-d", "postgres",  # Connect to default postgres database
        "-tc", f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"
    ]
    
    result = subprocess.run(check_db_cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error connecting to PostgreSQL: {result.stderr}")
        print("\nTrying to create database...")
    else:
        if result.stdout.strip() == "1":
            print(f"Database '{db_name}' already exists!")
            response = input("Do you want to recreate it? (yes/no): ")
            if response.lower() != "yes":
                print("Database creation cancelled.")
                sys.exit(0)
            # Drop existing database
            drop_cmd = [
                "psql",
                "-h", db_host,
                "-p", db_port,
                "-U", db_user,
                "-d", "postgres",
                "-c", f"DROP DATABASE IF EXISTS {db_name};"
            ]
            subprocess.run(drop_cmd, check=True)
            print(f"Database '{db_name}' dropped.")
    
    # Create database
    create_cmd = [
        "psql",
        "-h", db_host,
        "-p", db_port,
        "-U", db_user,
        "-d", "postgres",
        "-c", f"CREATE DATABASE {db_name};"
    ]
    
    result = subprocess.run(create_cmd, check=True)
    print(f"✅ Database '{db_name}' created successfully!")
    print(f"\nNext steps:")
    print(f"1. Tables will be created automatically when you run the bot")
    print(f"2. Or run: cd app && python -c 'from db.init_db import init_db; init_db()'")
    
except subprocess.CalledProcessError as e:
    print(f"❌ Error creating database: {e}")
    print(f"\nTroubleshooting:")
    print(f"1. Make sure PostgreSQL is running: brew services start postgresql@14")
    print(f"2. Check connection settings in app/env.py")
    print(f"3. Try creating database manually:")
    print(f"   psql -U {db_user} -d postgres -c \"CREATE DATABASE {db_name};\"")
    sys.exit(1)
except FileNotFoundError:
    print("❌ Error: psql command not found")
    print("Make sure PostgreSQL is installed:")
    print("  brew install postgresql@14")
    sys.exit(1)
finally:
    # Clear password from environment
    if 'PGPASSWORD' in os.environ:
        del os.environ['PGPASSWORD']

