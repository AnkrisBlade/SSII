from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float, func, type_coerce, TypeDecorator
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

engine_example = 'mysql+pymysql://root:BIGDATA@127.0.0.1/hash'
engine_hash = create_engine(engine_example)

# API Base
Base = declarative_base()
# Staging Base
Hash_Base = declarative_base(metadata=MetaData(schema='hash'))


class NamePassw(Hash_Base):
    __tablename__ = "Name_Passw"

    Name = Column(String(255), nullable=False)
    Password = Column(String(255), primary_key=True)
    Hashed_Passw = Column(String(255), nullable=False)
    Load_datetime = Column(DateTime, server_default=func.now())
