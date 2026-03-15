from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Sử dụng SQLite cho MVP
SQLALCHEMY_DATABASE_URL = "sqlite:///./thuvien.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Hàm dependency để tạo session database cho mỗi request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()