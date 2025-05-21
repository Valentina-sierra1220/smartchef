# config/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

# URL de la base de datos: SQLite (archivo local)
DATABASE_URL = "sqlite:///smartchef.db"

# Motor de conexión a SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # necesario para trabajar con Flask
    poolclass=StaticPool,                       # reutiliza la misma conexión
    echo=True                                   # muestra las consultas en la consola (solo para desarrollo)
)

# Sesiones: permiten leer y escribir en la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: clase base que usarán todos nuestros modelos (tablas)
Base = declarative_base()         
