<script lang="ts">
  type Receta = {
    id?: string;
    titulo: string;
    autor: string;
    imagen?: string;
    descripcion?: string;
    ingredientes?: string[];
    pasos?: string[];
  };

  export let historial: Receta[] = [];
  export let abrirCrearModal: () => void;
  export let abrirModal: (receta: Receta) => void;
</script>

<aside class="sidebar">
  <div class="logo-container">
    <img src="/logo.jpg" alt="SmartChef Logo" class="logo" />
  </div>

  <button class="add-button" on:click={abrirCrearModal}>+ Crear receta</button>
  <h2>Recetas guardadas</h2>

  <div class="sidebar-scroll">
    {#if historial.length === 0}
      <p style="font-size: 13px; opacity: 0.7;">No hay recetas guardadas aún.</p>
    {:else}
      {#each historial as receta (receta.id)}
  {#if receta.titulo}
    <button title={receta.titulo} on:click={() => abrirModal(receta)}>
      {receta.titulo}
    </button>
  {/if}
{/each}

    {/if}
  </div>
</aside>

<style>
  .sidebar {
    width: 260px;
    background-color: #1e293b;
    color: white;
    padding: 24px;
    display: flex;
    flex-direction: column;
    box-shadow: 2px 0 6px rgba(0, 0, 0, 0.05);
  }

  .logo-container {
    display: flex;
    justify-content: center;
    margin-bottom: 24px;
  }

  .logo {
    width: 64px;
    height: 64px;
    object-fit: contain;
    filter: brightness(0) invert(1);
  }

  .add-button {
    background-color: white;
    color: #1e293b;
    font-weight: 500;
    font-size: 14px;
    padding: 8px 12px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    margin-bottom: 12px;
    transition: background 0.2s ease;
  }

  .add-button:hover {
    background-color: rgba(255, 255, 255, 0.9);
  }

  h2 {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 12px;
  }

  .sidebar-scroll {
    flex: 1;
    overflow-y: auto;
    padding-right: 4px;
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.4) transparent;
  }

  .sidebar-scroll::-webkit-scrollbar {
    width: 6px;
  }

  .sidebar-scroll::-webkit-scrollbar-thumb {
    background-color: rgba(255, 255, 255, 0.4);
    border-radius: 10px;
  }

  .sidebar-scroll button {
    width: 100%;
    padding: 10px 14px;
    margin-bottom: 6px;
    background-color: rgba(255, 255, 255, 0.08);
    border: none;
    border-radius: 8px;
    color: white;
    font-size: 14px;
    text-align: left;
    cursor: pointer;
    transition: background 0.2s ease;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .sidebar-scroll button:hover {
    background-color: #334155;
  }
</style>
