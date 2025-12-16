from sqlalchemy import create_engine, text

engine = create_engine(
    "mysql+pymysql://root:123456@127.0.0.1:3306",
    isolation_level="AUTOCOMMIT",
    echo=True
)

with engine.connect() as conn:
    conn.execute(text("CREATE DATABASE chat_history_db"))
