from sqlalchemy import Column, String, DateTime, func
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

# Definimos la conexion con la base de datos, en este caso nos
# conectamos a una base creada en MySQL
engine_example = 'mysql+pymysql://root:BIGDATA@127.0.0.1/hash'
engine_hash = create_engine(engine_example)

# Definimos la Base y el schema al que está asociado
Hash_Base = declarative_base()


# Definimos la Tabla que almacenara el nombre, la contraseña, el hash de la contraseña
# y la fecha de insercción de los datos.
class NamePassw(Hash_Base):
    __tablename__ = "Name_Passw"

    Name = Column(String(255), nullable=False)
    Password = Column(String(255), primary_key=True)
    Hashed_Passw = Column(String(255), nullable=False)
    Load_datetime = Column(DateTime, server_default=func.now())
