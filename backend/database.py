"""Configuración de la base de datos con SQLAlchemy para el proyecto SmartChef."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# URL de la base de datos SQLite
DATABASE_URL = "sqlite:///smartchef.db"

# Crear el motor que se conecta a esa URL
engine = create_engine(DATABASE_URL, echo=True)

# Crear la sesión para acceder a la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para tus modelos (clases en POO)
Base = declarative_base()
