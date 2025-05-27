<script lang="ts">
  import type { Receta } from '$model/Receta';

  export let recetas: Receta[] = [];
  export let abrirModal: (receta: Receta) => void;
</script>

{#if recetas.length === 0}
  <div class="flex-1 flex items-center justify-center text-gray-500 text-center text-lg">
    Aún no hay recetas compartidas.<br />¡Comienza a compartir tus recetas!
  </div>
{:else}
  <div class="grid">
    {#each recetas as receta}
      <div class="card">
        <img src={receta.imagen || '/imagen-default.png'} alt="imagen por defecto" />
        <div class="card-content">
          <div class="receta-titulo">{receta.nombre}</div>
          <div class="receta-autor">por {receta.creador}</div>
          <button
            class="mt-4 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors text-sm font-semibold"
            on:click={() => abrirModal(receta)}
          >
            Ver más
          </button>
        </div>
      </div>
    {/each}
  </div>
{/if}

<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 20px;
    flex: 1;
    overflow-y: auto;
    padding-right: 8px;
  }

  .card {
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    text-align: center;
    min-height: 280px;
    cursor: pointer;
  }

  .card img {
    width: 100%;
    height: 160px;
    object-fit: contain;
    padding: 12px;
    background-color: #f1f5f9;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    display: block;
  }

  .card-content {
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    background-color: #fff;
    flex: 1;
    justify-content: center;
  }

  .receta-titulo {
    font-weight: 600;
    font-size: 16px;
  }

  .receta-autor {
    font-size: 14px;
    color: #6b7280;
  }
</style>
