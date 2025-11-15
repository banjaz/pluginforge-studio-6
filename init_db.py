"""
Database initialization script for production deployment
Run this after first deployment to create tables and admin user
"""
from app import app, db, User
from werkzeug.security import generate_password_hash
import sys

def init_database():
    """Initialize database with tables and default admin user"""
    with app.app_context():
        try:
            # Create all tables
            print("📦 Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Create admin user if doesn't exist
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                print("👤 Creating admin user...")
                admin = User(
                    username='admin',
                    email='admin@pluginforge.com',
                    password_hash=generate_password_hash('admin123')
                )
                db.session.add(admin)
                db.session.commit()
                print("✅ Admin user created successfully")
                print("📝 Login credentials: admin / admin123")
                print("⚠️  IMPORTANT: Change the admin password after first login!")
            else:
                print("ℹ️  Admin user already exists")
            
            # Verify database connection
            user_count = User.query.count()
            print(f"📊 Total users in database: {user_count}")
            
            print("\n✅ Database initialization completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing database: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)
