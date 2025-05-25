<script lang="ts">
  export let show = false;
  export let onClose: () => void;
  export let onGuardar: (receta: {
    titulo: string;
    descripcion: string;
    instrucciones: string;
    tiempo: string;
    porciones: number;
    publica: boolean;
    imagen?: string;
  }) => void;

  let titulo = '';
  let descripcion = '';
  let instrucciones = '';
  let tiempo = '';
  let porciones: number = 1;
  let publica = false;
  let imagenTemp: string | null = null;

  function handleFileChange(event: Event) {
    const file = (event.target as HTMLInputElement)?.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        imagenTemp = reader.result as string;
      };
      reader.readAsDataURL(file);
    }
  }

  function guardarReceta() {
    const nuevaReceta = {
      titulo,
      descripcion,
      instrucciones,
      tiempo,
      porciones,
      publica,
      imagen: imagenTemp || ''
    };
    onGuardar(nuevaReceta);
    onClose();
  }
</script>

{#if show}
  <div class="fixed inset-0 bg-black/50 flex justify-center items-center z-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-md relative shadow-xl overflow-y-auto max-h-[90vh]">
      <button on:click={onClose} class="absolute top-3 right-3 text-gray-400 hover:text-gray-800 text-xl">×</button>

      <h2 class="text-lg font-semibold mb-4 text-center">Nueva Receta</h2>

      <div class="space-y-4 text-sm">
        <div>
          <label for="titulo" class="font-medium block mb-1">Nombre</label>
          <input id="titulo" bind:value={titulo} type="text" class="w-full p-2 border rounded-md" />
        </div>

        <div>
          <label for="descripcion" class="font-medium block mb-1">Descripción</label>
          <textarea id="descripcion" bind:value={descripcion} class="w-full p-2 border rounded-md"></textarea>
        </div>

        <div>
          <label for="instrucciones" class="font-medium block mb-1">Instrucciones</label>
          <textarea id="instrucciones" bind:value={instrucciones} class="w-full p-2 border rounded-md"></textarea>
        </div>

        <div>
          <label for="tiempo" class="font-medium block mb-1">Tiempo</label>
          <input id="tiempo" bind:value={tiempo} type="text" class="w-full p-2 border rounded-md" />
        </div>

        <div>
          <label for="porciones" class="font-medium block mb-1">Porciones</label>
          <input id="porciones" bind:value={porciones} type="number" min="1" class="w-full p-2 border rounded-md" />
        </div>

        <div class="flex items-center gap-2">
          <input id="publica" type="checkbox" bind:checked={publica} class="rounded border-gray-300" />
          <label for="publica" class="text-sm">¿Publica?</label>
        </div>

        <div>
          <label for="imagen" class="font-medium block mb-1">Imagen</label>
          <input
            id="imagen"
            type="file"
            accept="image/*"
            on:change={handleFileChange}
            class="block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />

          {#if imagenTemp}
            <img src={imagenTemp} alt="Vista previa" class="w-full max-h-[200px] object-contain rounded-md border mt-2" />
          {/if}
        </div>
      </div>

      <div class="mt-6 flex flex-col gap-2">
        <button
          on:click={guardarReceta}
          class="w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 text-sm font-semibold"
        >
          Guardar
        </button>
        <button
          on:click={onClose}
          class="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 text-sm font-semibold"
        >
          Cerrar
        </button>
      </div>
    </div>
  </div>
{/if}
