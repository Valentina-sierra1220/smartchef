// src/lib/api.ts

export const API_BASE_URL = 'http://127.0.0.1:5000';

/**
 * Registro de usuario
 */
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
export async function loginUser(correo: string, contraseña: string): Promise<string> {
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
    return data.mensaje || 'Inicio de sesión exitoso';
  } catch (err) {
    if (err instanceof Error) {
      throw new Error(`No se pudo iniciar sesión: ${err.message}`);
    } else {
      throw new Error('Ocurrió un error desconocido al iniciar sesión');
    }
  }
}
