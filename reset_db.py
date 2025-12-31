"""
Script to reset database schema
"""
from app.agent.db_models import Base, engine

print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)

print("Creating all tables...")
Base.metadata.create_all(bind=engine)

print("Database reset complete!")
