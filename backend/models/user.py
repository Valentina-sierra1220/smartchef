# models/usuario.py

from sqlalchemy import Column, Integer, String
from config.database import Base
import bcrypt

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, nullable=False, unique=True)
    contraseña_hash = Column(String, nullable=False)  # Guardamos el hash

    def set_contraseña(self, contraseña_plana):
        """Recibe una contraseña en texto plano y guarda su hash."""
        self.contraseña_hash = bcrypt.hashpw(
            contraseña_plana.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    def verificar_contraseña(self, contraseña_plana):
        """Verifica si la contraseña ingresada es correcta."""
        return bcrypt.checkpw(
            contraseña_plana.encode('utf-8'),
            self.contraseña_hash.encode('utf-8')
        )

    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre='{self.nombre}', correo='{self.correo}')>"
