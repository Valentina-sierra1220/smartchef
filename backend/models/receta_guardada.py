# models/receta_guardada.py

from sqlalchemy import Column, Integer, ForeignKey
from config.database import Base

class RecetaGuardada(Base):
    __tablename__ = "recetas_guardadas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    id_receta = Column(Integer, ForeignKey("recetas.id"), nullable=False)

    def __repr__(self):
        return f"<RecetaGuardada(usuario={self.id_usuario}, receta={self.id_receta})>"
