from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float, func, type_coerce, TypeDecorator
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, backref
import hashlib
import os
from sqlalchemy.types import LargeBinary
from base import Hash_Base

class Hashing(TypeDecorator):
    """Safely coerce Python bytestrings to Unicode
    before passing off to the database."""

    impl = LargeBinary

    def __init__(self, password):
        super(Hashing, self).__init__()
        self.password = password

    def process_hash_passw(self, value):
        if isinstance(value, str):
            salt = os.urandom(5)
            value = hashlib.pbkdf2_hmac('sha256', self.password.encode('utf-8'), salt, 100000)
            # bindvalue = type_coerce(value, String)
        return value # func.pgp_sym_encrypt(bindvalue, self.passphrase)
    
    # def column_expression(self, col):
    #     return func.pgp_sym_decrypt(col, self.password)


# salt = 5
# salt_b = os.urandom(salt)
# password = 'test'
# key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt_b, 100000)
# type(key)
# key.decode('utf-8')

class NamePassw(Hash_Base):
    __tablename__ = "Name_Passw"

    Name = Column(String(255))
    Password = Column(String(255), primary_key=True)
    Hashed_Passw = Column(Hashing(Password)
    Load_datetime = Column(DateTime, server_default=func.now())


# class Passw(object):
#     @declared_attr
#     def passw_b(self):
#         passw = Column("Password", String(255),
#                           ForeignKey('basic_match.Match_id',
#                                      ondelete="cascade", onupdate="cascade"))
#         return match_id

# class PasswHash(Base):
#     __tablename__ = Passw_Hash

#     Password_Hashed = Column(String(255), primary_key=True)