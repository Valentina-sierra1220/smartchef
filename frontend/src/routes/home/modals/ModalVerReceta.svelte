<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  type Receta = {
    id?: string;
    titulo: string;
    autor: string;
    imagen?: string;
    descripcion?: string;
    ingredientes?: string[];
    pasos?: string[];
  };

  export let show = false;
  export let receta: Receta;
  export let onClose: () => void;

  const dispatch = createEventDispatcher();

  let imagenPreview = '';
  let imagenTemp = '';
  let editando = false;
  let yaCompartida = false;

  let titulo = '';
  let autor = '';
  let descripcion = '';
  let ingredientes = '';
  let pasos = '';
  let mensaje = '';

  $: if (show && receta && !editando) {
    titulo = receta.titulo;
    autor = receta.autor;
    descripcion = receta.descripcion || '';
    ingredientes = (receta.ingredientes ?? []).join(', ');
    pasos = (receta.pasos ?? []).join('\n');
    imagenTemp = receta.imagen || '';
    imagenPreview = receta.imagen || '';
    mensaje = '';
  }

  function handleFileChange(event: Event) {
    const file = (event.target as HTMLInputElement)?.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        imagenTemp = reader.result as string;
        imagenPreview = imagenTemp;
      };
      reader.readAsDataURL(file);
    }
  }

  function compartirReceta() {
    if (yaCompartida) {
      mensaje = '⚠️ Ya se compartió esta receta.';
      return;
    }

    dispatch('compartir', {
      ...receta,
      imagen: imagenTemp
    });

    yaCompartida = true;
    mensaje = '✅ Receta compartida.';
  }

  function habilitarEdicion() {
    editando = true;
  }

  function guardarCambios() {
    const editada = {
      ...receta,
      titulo: titulo.trim(),
      autor: autor.trim(),
      descripcion: descripcion.trim(),
      ingredientes: ingredientes.split(',').map(i => i.trim()).filter(Boolean),
      pasos: pasos.split('\n').map(p => p.trim()).filter(Boolean),
      imagen: imagenTemp
    };
    dispatch('editado', editada);
    mensaje = '✅ Cambios guardados.';
    editando = false;
  }
</script>

{#if show}
  <div class="fixed inset-0 bg-black/50 flex justify-center items-center z-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-md relative shadow-xl overflow-y-auto max-h-[90vh]">
      <button on:click={onClose} class="absolute top-3 right-3 text-gray-400 hover:text-gray-800 text-xl">×</button>

      <div class="w-full flex flex-col items-center mb-4">
        {#if imagenPreview}
          <img src={imagenPreview} alt="Imagen de receta" class="rounded-md max-h-[300px] w-auto object-contain" />
        {:else}
          <div class="w-full h-[200px] bg-gray-100 flex items-center justify-center text-gray-400 rounded-md">
            📷 No se ha cargado imagen
          </div>
        {/if}

        <input
          type="file"
          accept="image/*"
          on:change={handleFileChange}
          class="mt-4 text-sm text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
      </div>

      {#if editando}
        <input bind:value={titulo} class="w-full p-2 border rounded mb-2 text-sm" placeholder="Título" />
        <input bind:value={autor} class="w-full p-2 border rounded mb-2 text-sm" placeholder="Autor" />
        <textarea bind:value={descripcion} class="w-full p-2 border rounded mb-2 text-sm" placeholder="Descripción"></textarea>
        <textarea bind:value={ingredientes} class="w-full p-2 border rounded mb-2 text-sm" placeholder="Ingredientes (separados por comas)"></textarea>
        <textarea bind:value={pasos} class="w-full p-2 border rounded mb-4 text-sm" placeholder="Pasos (cada uno en una línea)"></textarea>

        <button on:click={guardarCambios} class="w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 text-sm font-semibold">
          Guardar cambios
        </button>
      {:else}
        <h2 class="text-lg font-semibold mb-2">{receta.titulo}</h2>
        <p class="text-sm text-gray-600 mb-4">{receta.descripcion}</p>

        <div class="mb-6">
          <h3 class="font-medium">🥣 Ingredientes</h3>
          <ul class="list-disc ml-5 text-sm mb-4">
            {#each receta.ingredientes ?? [] as i}<li>{i}</li>{/each}
          </ul>

          <h3 class="font-medium">👨‍🍳 Pasos</h3>
          <ol class="list-decimal ml-5 text-sm">
            {#each receta.pasos ?? [] as paso}<li>{paso}</li>{/each}
          </ol>
        </div>

        {#if mensaje}
          <p class="text-sm text-green-600 mb-2">{mensaje}</p>
        {/if}

        <div class="flex flex-col gap-2">
          <button
            on:click={compartirReceta}
            disabled={yaCompartida}
            class="w-full py-2 px-4 rounded-lg text-sm font-semibold transition-colors
              {yaCompartida
                ? 'bg-gray-400 text-white cursor-not-allowed'
                : 'bg-indigo-600 text-white hover:bg-indigo-700'}"
          >
            {yaCompartida ? 'Ya se compartió' : 'Compartir'}
          </button>

          <button on:click={habilitarEdicion} class="w-full bg-teal-600 text-white py-2 px-4 rounded-lg hover:bg-teal-700 text-sm font-semibold">
            Editar
          </button>
        </div>
      {/if}

      <button on:click={onClose} class="w-full mt-4 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 text-sm font-semibold">
        Cerrar
      </button>
    </div>
  </div>
{/if}
