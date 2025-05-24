import { Receta } from './Receta';

export class Usuario {
  constructor(
    public nombre: string,
    public correo: string,
    public contrasena: string,
    public recetas: Receta[] = []
  ) {}

  static fromJson(json: any): Usuario {
    return new Usuario(
      json.nombre,
      json.correo,
      json.contrasena,
      json.recetas?.map((r: any) => Receta.fromJson(r)) || []
    );
  }
}
