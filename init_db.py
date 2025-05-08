from app import db

if __name__ == "__main__":
    db.create_all()
    print("Database tables created successfully.")
