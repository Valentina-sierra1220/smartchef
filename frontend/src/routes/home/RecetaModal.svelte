<script lang="ts">
  export let receta: { titulo: string; autor: string; imagen?: string } | null;
  export let onClose: () => void;
</script>

{#if receta}
  <div class="modal-overlay" on:click={onClose}>
    <div class="modal" on:click|stopPropagation>
      <h2>{receta.titulo}</h2>
      <p>por {receta.autor}</p>
      <img src={receta.imagen || '/imagen-default.png'} alt="Imagen de receta" />
      <button on:click={onClose}>Cerrar</button>
    </div>
  </div>
{/if}

<style>
  .modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 100;
  }

  .modal {
    background: white;
    padding: 16px;
    border-radius: 12px;
    width: 300px;
    text-align: center;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  }

  .modal img {
    width: 100%;
    border-radius: 8px;
    margin: 12px 0;
  }

  .modal button {
    background-color: #ef4444;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
  }

  .modal button:hover {
    background-color: #dc2626;
  }
</style>
