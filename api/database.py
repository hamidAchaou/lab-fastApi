# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# ssl_args = {
#     "ssl": {
#         "ca": "./ca.pem"
#     }
# }

# SQLALCHEMY_DATABASE_URL = (
#     "mysql+pymysql://avnadmin:AVNS_N-y3TCrpPKoracijYxp@mysql-d48dd82-achaou-7575.l.aivencloud.com:14434/defaultdb"
# )

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=ssl_args)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection parameters
DB_CONFIG = {
    "db": "defaultdb",
    "host": "mysql-d48dd82-achaou-7575.l.aivencloud.com",
    "password": "AVNS_N-y3TCrpPKoracijYxp",
    "port": 14434,
    "user": "avnadmin",
}

# Create SQLAlchemy engine
DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['db']}"

# Add SSL configuration
ssl_args = {
    "ssl": {
        "ssl_mode": "REQUIRED"
    }
}

engine = create_engine(DATABASE_URL, connect_args=ssl_args)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()