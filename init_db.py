#!/usr/bin/env python3
"""
Initialize database - create tables
"""
import sys
import os

# Add app to path
sys.path.insert(0, '/app')

# Set Docker flag
os.environ.setdefault('RUNNING_IN_DOCKER', 'true')

from app.agent.db_models import init_db

if __name__ == '__main__':
    try:
        print("=" * 60)
        print("Database Initialization")
        print("=" * 60)
        init_db()
        print("=" * 60)
        print("✓ Database initialization complete!")
        print("=" * 60)
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        sys.exit(1)
