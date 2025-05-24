export class Imagen {
  constructor(
    public url: string,
    public id_user: BigInt
  ) {}

  static fromJson(json: any): Imagen {
    return new Imagen(json.url, json.id_user);
  }
}
