export async function subirMultiplesImagenes(files: File[]): Promise<string[]> {
  const formData = new FormData();
  for (const file of files) {
    formData.append('imagenes', file);
  }

  const response = await fetch('http://127.0.0.1:5000/upload', {
    method: 'POST',
    body: formData
  });

  const data = await response.json();
  return data.urls || [];
}
