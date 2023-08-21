from app.db.config import Base
from sqlalchemy import Column, BigInteger, String


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(1024), unique=True)
    password = Column(String(1024))
