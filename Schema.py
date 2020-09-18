import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class http(Base):
    __tablename__ = 'http'
    id = Column(Integer, primary_key=True)
    proxy = Column(String(21), nullable=False, unique=True)
    added = Column(String(19), nullable=False)
    lastChecked = Column(String(19), nullable=False)

class socks4(Base):
    __tablename__ = 'socks4'
    id = Column(Integer, primary_key=True)
    proxy = Column(String(21), nullable=False, unique=True)
    added = Column(String(19), nullable=False)
    lastChecked = Column(String(19), nullable=False)

class socks5(Base):
    __tablename__ = 'socks5'
    id = Column(Integer, primary_key=True)
    proxy = Column(String(21), nullable=False, unique=True)
    added = Column(String(19), nullable=False)
    lastChecked = Column(String(19), nullable=False)

engine = create_engine('sqlite:///proxies.db')
Base.metadata.create_all(engine)