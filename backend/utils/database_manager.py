# utils/database_manager.py

from config.database import Base,engine
from models.user import Usuario
from models.receta import Receta
from models.imagen_receta import ImagenReceta
from models.receta_guardada import RecetaGuardada


 

def create_tables():
    """Crea todas las tablas de la base de datos."""
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente")
