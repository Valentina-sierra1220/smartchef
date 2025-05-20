# models/receta.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
from config.database import Base

class Receta(Base):
    __tablename__ = "recetas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    instrucciones = Column(Text, nullable=False)
    tiempo = Column(Integer, nullable=True)
    porciones = Column(Integer, nullable=True)
    
    publica = Column(Boolean, default=False)         # ¿La receta es visible para todos?

    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    def __repr__(self):
        return f"<Receta(id={self.id}, nombre='{self.nombre}')>"
