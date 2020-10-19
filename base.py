from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine_example = 'mysql+pymysql://root:BIGDATA@127.0.0.1/hash'
engine_hash = create_engine(engine_example)

# API Base
Base = declarative_base()
# Staging Base
Hash_Base = declarative_base(metadata=MetaData(schema='hash'))

# Session
SessionHash = sessionmaker(bind=engine_hash)


# Function to reset the Staging Database
def reset_db(base, engine):
    base.metadata.drop_all(engine)
    base.metadata.create_all(engine)
    print("Tables for Hashing Database created")