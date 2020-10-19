from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float, func, type_coerce, TypeDecorator
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, backref
import hashlib
import os
from sqlalchemy.types import LargeBinary
from base import Hash_Base

# class Hashing(TypeDecorator):
#     impl = LargeBinary

#     def __init__(self, password):
#         super(Hashing, self).__init__()
#         self.password = password

#     def process_hash_passw(self, value):
#         if isinstance(value, str):
#             salt = os.urandom(5)
#             value = hashlib.pbkdf2_hmac('sha256', self.password.encode('utf-8'), salt, 100000)
#             # bindvalue = type_coerce(value, String)
#         return value # func.pgp_sym_encrypt(bindvalue, self.passphrase)
    
class NamePassw(Hash_Base):
    __tablename__ = "Name_Passw"

    Name = Column(String(255), nullable=False)
    Password = Column(String(255), primary_key=True) 
    Hashed_Passw = Column(String(255), nullable=False)
    Load_datetime = Column(DateTime, server_default=func.now())
