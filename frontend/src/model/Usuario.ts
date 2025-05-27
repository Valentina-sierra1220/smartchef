import { Receta } from './Receta';

export class Usuario {
  constructor(
    public id : BigInt,
    public nombre: string,
    public correo: string,
   
    public recetas: Receta[] = []
  ) {}

  static fromJson(json: any): Usuario {
    return new Usuario(
      json.id,
      json.nombre,
      json.correo,      
      json.recetas?.map((r: any) => Receta.fromJson(r)) || []
    );
  }
}
