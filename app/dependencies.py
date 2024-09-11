from app.database import SessionLocal

# Dependency for the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
