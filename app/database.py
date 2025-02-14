from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Since you're connecting via Unix socket without password
SQLALCHEMY_DATABASE_URL = "postgresql:///store_db"

# Or more explicitly:
SQLALCHEMY_DATABASE_URL = "postgresql://kentarovadney@localhost/store_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 