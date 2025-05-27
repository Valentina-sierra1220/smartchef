export const BASE_BACKEND_URL = 'http://127.0.0.1:5000';

export function construirUrlImagen(urlParcial: string): string {
  if (!urlParcial) return ''; // manejo si está vacía
  return `${BASE_BACKEND_URL}${urlParcial}`;
}
