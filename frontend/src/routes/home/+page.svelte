<script lang="ts">
  import ModalVerReceta from './modals/ModalVerReceta.svelte';
  import ModalCrearReceta from './modals/ModalCrearReceta.svelte';
  import BarraLateral from './components/BarraLateral.svelte';
  import CuadriculaRecetas from './components/CuadriculaRecetas.svelte';
  import BarraBusqueda from './components/BarraBusqueda.svelte';

  type Receta = {
    id?: string;
    titulo: string;
    autor: string;
    imagen?: string;
    descripcion?: string;
    ingredientes?: string[];
    pasos?: string[];
    tiempo?: string;
    porciones?: number;
    publica?: boolean;
  };

  let historial: Receta[] = [];
  let recetasCompartidas: Receta[] = [];

  let showModal = false;
  let showCrearModal = false;

  let recetaSeleccionada: Receta | null = null;

  function abrirModal(receta: Receta) {
    recetaSeleccionada = { ...receta };
    showModal = true;
  }

  function cerrarModal() {
    showModal = false;
  }

  function abrirCrearModal() {
    showCrearModal = true;
  }

  function cerrarCrearModal() {
    showCrearModal = false;
  }

  function guardarRecetaDesdeModal(data: {
    titulo: string;
    descripcion: string;
    instrucciones: string;
    tiempo: string;
    porciones: number;
    publica: boolean;
  }) {
    const nuevaReceta: Receta = {
      ...data,
      id: crypto.randomUUID(),
      autor: 'usuario',
      pasos: data.instrucciones.split('\n').map(p => p.trim()).filter(Boolean),
      ingredientes: [], // opcional si decides usarlos luego
    };

    historial = [nuevaReceta, ...historial];

    if (nuevaReceta.publica) {
      recetasCompartidas = [nuevaReceta, ...recetasCompartidas];
    }
  }

  function compartirReceta(receta: Receta) {
    const yaExiste = recetasCompartidas.some((r) => r.id === receta.id);
    if (!yaExiste) {
      recetasCompartidas = [receta, ...recetasCompartidas];
    }
  }

  function actualizarRecetaEditada(editada: Receta) {
    recetasCompartidas = recetasCompartidas.map((r) =>
      r.id === editada.id ? { ...editada } : r
    );

    historial = historial.map((r) =>
      r.id === editada.id ? { ...editada } : r
    );

    recetaSeleccionada = { ...editada };
  }
</script>

<div class="layout">
  <BarraLateral
    {historial}
    {abrirCrearModal}
    {abrirModal}
  />

  <main class="main">
    <div class="main-header">
      <h1>Explora tus recetas</h1>
    </div>

    <div class="contenido-recetas">
      {#if recetasCompartidas.length === 0}
        <div class="flex h-full justify-center items-center w-full">
          <div class="text-center text-gray-500 text-lg leading-relaxed">
            <p>Aún no hay recetas compartidas.</p>
            <p>¡Comienza a compartir tus recetas!</p>
          </div>
        </div>
      {:else}
        <CuadriculaRecetas recetas={recetasCompartidas} {abrirModal} />
      {/if}
    </div>

    <BarraBusqueda />
  </main>
</div>

{#if recetaSeleccionada}
  <ModalVerReceta
    show={showModal}
    receta={recetaSeleccionada}
    onClose={cerrarModal}
    on:compartir={(e) => {
      compartirReceta(e.detail);
      cerrarModal();
    }}
    on:editado={(e) => actualizarRecetaEditada(e.detail)}
  />
{/if}

{#if showCrearModal}
  <ModalCrearReceta
    show={showCrearModal}
    onClose={cerrarCrearModal}
    onGuardar={guardarRecetaDesdeModal}
  />
{/if}

<style>
  .layout {
    display: flex;
    height: 100vh;
    font-family: 'Segoe UI', sans-serif;
    background-color: var(--bg);
    color: var(--text);
  }

  .main {
    display: flex;
    flex-direction: column;
    flex: 1;
    padding: 32px;
    overflow: hidden;
  }

  .main-header {
    margin-bottom: 28px;
  }

  .main-header h1 {
    font-size: 26px;
    font-weight: 600;
  }

  .contenido-recetas {
    flex: 1;
    overflow-y: auto;
    padding-right: 8px;
  }
</style>
