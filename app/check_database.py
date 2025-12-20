#!/usr/bin/env python3
"""
Script to check database connection and tables
"""
import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db.session import get_engine
from db.models import User, Offer
from db.base import Base
from sqlalchemy import inspect

def check_database():
    """Check database connection and tables"""
    print("Checking database connection...")
    try:
        engine = get_engine()
        if engine is None:
            print("❌ Database engine is not available. Cannot check database.")
            return False
        
        conn = engine.connect()
        print("✅ Database connection successful!")
        
        print("\nChecking tables...")
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Found tables: {tables}")
        
        required_tables = ['users', 'offers']
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            print(f"\n❌ Missing tables: {missing_tables}")
            print("Creating missing tables...")
            Base.metadata.create_all(bind=engine)
            print("✅ Tables created!")
        else:
            print("✅ All required tables exist!")
        
        # Show table structure
        print("\nTable structures:")
        for table_name in required_tables:
            if table_name in tables:
                columns = inspector.get_columns(table_name)
                print(f"\n{table_name}:")
                for col in columns:
                    print(f"  - {col['name']}: {col['type']}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = check_database()
    sys.exit(0 if success else 1)

