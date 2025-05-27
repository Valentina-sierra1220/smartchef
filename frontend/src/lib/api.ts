// src/lib/api.ts
import { Usuario } from '$model/Usuario';
import { Receta } from '$model/Receta';
import { Imagen } from '$model/Imagen';
export const API_BASE_URL = 'http://127.0.0.1:5000';




export async function registerUser(nombre: string, correo: string, contraseña: string): Promise<string> {
  try {
    const response = await fetch(`${API_BASE_URL}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ nombre, correo, contraseña })
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(error || 'Error en el registro');
    }

    return await response.text();
  } catch (err) {
    if (err instanceof Error) {
      throw new Error(`No se pudo registrar: ${err.message}`);
    } else {
      throw new Error('Ocurrió un error desconocido al registrarse');
    }
  }
}

/**
 * Inicio de sesión
 */
export async function loginUser(correo: string, contraseña: string): Promise<Usuario> {
  try {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ correo, contraseña })
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(error || 'Error al iniciar sesión');
    }

    const data = await response.json();

    // Convierte la respuesta en una instancia del modelo Usuario
    return Usuario.fromJson({
      id: data.id_usuario,
      nombre: data.nombre,
      correo: data.correo,
      recetas: [] // puedes llenarlo luego si quieres cargar las recetas del usuario
    });
  } catch (err) {
    if (err instanceof Error) {
      throw new Error(`No se pudo iniciar sesión: ${err.message}`);
    } else {
      throw new Error('Ocurrió un error desconocido al iniciar sesión');
    }
  }
}


/**
 * Receta
 */

export async function crearReceta(receta: Receta): Promise<Receta> {
  try {
    // Obtener el usuario activo desde localStorage
    const storedUser = localStorage.getItem('usuario');
    const usuario = storedUser ? Usuario.fromJson(JSON.parse(storedUser)) : null;

    if (!usuario) {
      throw new Error('No hay un usuario autenticado');
    }

    // Preparamos el body para el backend (solo campos planos)
    const body = {
      nombre: receta.nombre,
      descripcion: receta.descripcion,
      instrucciones: receta.instrucciones,
      tiempo: receta.tiempo,
      porciones: receta.porciones,
      publica: receta.publica,
      id_usuario: usuario.id.toString(), 
      imagen: receta.imagenes[0]?.url || '',
      imagenes: receta.imagenes.map(img => img.url)
    };

    const response = await fetch(`${API_BASE_URL}/recetas`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(error || 'Error al crear la receta');
    }

    const data = await response.json();

    // Reconstruir objeto Receta completo (ya con id del backend)
    return new Receta(
      data.id_receta.toString(),
      body.nombre,
      body.descripcion,
      body.instrucciones,
      body.tiempo,
      body.porciones,
      body.publica,
      body.id_usuario,
      body.imagenes.map(url => new Imagen(url, BigInt(data.id_receta)))
    );
  } catch (err) {
    throw new Error(
      err instanceof Error
        ? `No se pudo crear la receta: ${err.message}`
        : 'Ocurrió un error desconocido al crear la receta'
    );
  }
}



export async function guardarUrlsImagenes(id_receta: number, urls: string[]): Promise<void> {
  try {
    const response = await fetch(`${API_BASE_URL}/imagenes-receta`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id_receta, urls })
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(error || 'Error al guardar las URLs de las imágenes');
    }
  } catch (err) {
    throw new Error(
      err instanceof Error
        ? `No se pudieron guardar las URLs: ${err.message}`
        : 'Ocurrió un error desconocido al guardar las URLs'
    );
  }
}

export async function obtenerMisRecetas(id_usuario: number): Promise<Receta[]> {
  const response = await fetch(`${API_BASE_URL}/mis-recetas?id_usuario=${id_usuario}`);

  if (!response.ok) {
    const error = await response.text();
    throw new Error(error || 'Error al obtener recetas personales');
  }

  const data = await response.json();

  return data.map((r: any) =>
    new Receta(
      r.id.toString(),
      r.nombre,
      r.descripcion,
      r.instrucciones,
      r.tiempo,
      r.porciones,
      r.publica,
      r.id_usuario.toString(),
      r.imagenes.map((url: string) => new Imagen(url, BigInt(r.id)))
    )
  );
}


export async function editarReceta(receta: Receta): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/recetas/${receta.id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      nombre: receta.nombre,
      descripcion: receta.descripcion,
      instrucciones: receta.instrucciones,
      tiempo: receta.tiempo,
      porciones: receta.porciones,
      publica: receta.publica
    })
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(error || 'Error al actualizar la receta');
  }
}