import { Imagen } from './Imagen';

export class Receta {
  constructor(
    public id: string,
    public nombre: string,
    public descripcion: string = '',
    public instrucciones: string = '',
    public tiempo: string = '',
    public porciones: number = 1,
    public publica: boolean = false,
    public id_usuario: string = '',
    public imagenes: Imagen[] = []
  ) {}

  static fromJson(json: any): Receta {
    return new Receta(
      json.id,
      json.nombre,
      json.descripcion || '',
      json.instrucciones || '',
      json.tiempo || '',
      json.porciones ?? 1,
      json.publica ?? false,
      json.id_usuario || '',
      Array.isArray(json.imagenes)
        ? json.imagenes.map((img: any) => Imagen.fromJson(img))
        : []
    );
  }
}
