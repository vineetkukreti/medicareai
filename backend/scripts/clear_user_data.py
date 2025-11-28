"""
Script to clear all user data from the database.
Removes all entries from users and contact_messages tables.
Admin authentication is handled separately via hardcoded credentials.
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database URL
DATABASE_URL = "sqlite:///./kisanai.db"

def clear_database():
    """Clear all user and contact message data"""
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Count records before deletion
        users_count = session.execute(text("SELECT COUNT(*) FROM users")).scalar()
        contacts_count = session.execute(text("SELECT COUNT(*) FROM contact_messages")).scalar()

        print(f"Found {users_count} users and {contacts_count} contact messages")

        # Delete all contact messages
        session.execute(text("DELETE FROM contact_messages"))
        print(f"✓ Deleted all {contacts_count} contact messages")

        # Delete all users
        session.execute(text("DELETE FROM users"))
        print(f"✓ Deleted all {users_count} users")

        # Reset auto-increment counters
        session.execute(text("DELETE FROM sqlite_sequence WHERE name='users'"))
        session.execute(text("DELETE FROM sqlite_sequence WHERE name='contact_messages'"))
        print("✓ Reset auto-increment counters")

        # Commit the changes
        session.commit()
        print("\n✅ Database cleared successfully!")
        print("Note: Admin access remains available via hardcoded credentials (admin@gmail.com)")

    except Exception as e:
        session.rollback()
        print(f"❌ Error clearing database: {e}")
    finally:
        session.close()
        engine.dispose()

if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE CLEANUP SCRIPT")
    print("=" * 60)
    print("\nThis will delete ALL user data and contact messages.")
    print("Admin access is preserved (hardcoded credentials).\n")

    confirmation = input("Type 'YES' to proceed: ")

    if confirmation == "YES":
        clear_database()
    else:
        print("❌ Operation cancelled")
