# models/imagen_receta.py

from sqlalchemy import Column, Integer, String, ForeignKey
from config.database import Base

class ImagenReceta(Base):
    __tablename__ = "imagenes_receta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(500), nullable=False)

    id_receta = Column(Integer, ForeignKey("recetas.id"), nullable=False)

    def __repr__(self):
        return f"<ImagenReceta(id={self.id}, receta_id={self.id_receta})>"
