
import { Imagen } from './Imagen';

export class Receta {
  constructor(
    public nombre: string,   
    public pasos: string[] = [],
    public imagenes: Imagen[] = [],
    public tipo: string = '',
    public creador: string = ''
  ) {}

  static fromJson(json: any): Receta {
    return new Receta(
      json.nombre,
      
      json.pasos || [],
      json.imagenes?.map((img: any) => Imagen.fromJson(img)) || [],
      json.tipo,
      json.creador
    );
  }
}
