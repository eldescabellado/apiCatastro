from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://postgres:Catastro.2025-@168.197.48.48:5671/sigep_catastro_web'

engine = create_engine(DATABASE_URL)