"""
Database migration script to add subscription fields to User model
Run this script to update the database schema
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app import app
from models import db

def migrate_database():
    """Add subscription fields to existing users table"""
    with app.app_context():
        try:
            # Check if columns already exist
            from sqlalchemy import inspect, text
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('users')]
            
            if 'subscription_plan' not in columns:
                print("📝 Adding subscription fields to users table...")
                
                # Add new columns with ALTER TABLE
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE users ADD COLUMN subscription_plan VARCHAR(20) DEFAULT 'basic'"))
                    conn.execute(text("ALTER TABLE users ADD COLUMN subscription_status VARCHAR(20) DEFAULT 'active'"))
                    conn.execute(text("ALTER TABLE users ADD COLUMN subscription_start DATETIME"))
                    conn.execute(text("ALTER TABLE users ADD COLUMN subscription_end DATETIME"))
                    conn.commit()
                
                print("✅ Migration completed successfully!")
                print("   - Added subscription_plan column")
                print("   - Added subscription_status column")
                print("   - Added subscription_start column")
                print("   - Added subscription_end column")
            else:
                print("✅ Subscription fields already exist in database")
                
        except Exception as e:
            print(f"❌ Migration error: {e}")
            print("\nℹ️  If using SQLite and columns already exist, you can ignore this error.")
            print("   The new fields will be created automatically when creating new tables.")

if __name__ == '__main__':
    migrate_database()
