<script lang="ts">
  type Receta = {
    titulo: string;
    autor: string;
    imagen?: string;
  };

  let historial = Array.from({ length: 40 }, (_, i) => `Receta número muy larga para probar el scroll y truncamiento ${i + 1}`);
  let recetas: Receta[] = [
    { titulo: 'Receta de ejemplo', autor: 'Chef Smart', imagen: '/imagen-default.png' }
  ];

  let recetaSeleccionada: Receta | null = null;

  function abrirModal(receta: Receta) {
    recetaSeleccionada = receta;
  }

  function cerrarModal() {
    recetaSeleccionada = null;
  }
</script>

<style>
  .layout {
    display: flex;
    height: 100vh;
    font-family: 'Segoe UI', sans-serif;
    background-color: #f8fafc;
    color: #0f172a;
  }

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

  .sidebar h2 {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 12px;
  }

  .sidebar-scroll {
    flex: 1;
    overflow-y: auto;
    padding-right: 4px;
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

  .main {
    flex: 1;
    display: flex;
    flex-direction: column;
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

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 20px;
    flex: 1;
    overflow-y: auto;
    padding-right: 8px;
  }

  .card {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    text-align: center;
    min-height: 280px;
  }

  .card img {
    width: 100%;
    height: 160px;
    object-fit: contain;
    padding: 12px;
    background-color: #f1f5f9;
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

  .ver-mas-btn {
    margin: 16px auto;
    padding: 6px 12px;
    background-color: #3b82f6;
    color: white;
    font-size: 14px;
    font-weight: 500;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.2s ease;
    width: max-content;
    display: block;
  }

  .ver-mas-btn:hover {
    background-color: #2563eb;
  }

  .search-bar {
    margin-top: 36px;
    position: relative;
  }

  .search-bar input {
    width: 100%;
    padding: 16px 56px 16px 20px;
    border: 2px solid #3b82f6;
    border-radius: 999px;
    font-size: 16px;
    font-weight: 500;
    background-color: #ffffff;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    transition: box-shadow 0.2s, border 0.2s;
  }

  .search-bar input:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
    border-color: #2563eb;
  }

  .search-icon {
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 20px;
    color: #2563eb;
    opacity: 0.85;
  }

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
    width: 320px;
    max-height: 80vh;
    overflow-y: auto;
    text-align: center;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  }

  .btn-cerrar {
    margin-top: 16px;
    background-color: #3b82f6;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
  }

  .btn-cerrar:hover {
    background-color: #2563eb;
  }
</style>

<div class="layout">
  <aside class="sidebar">
    <div class="logo-container">
      <img src="/logo.jpg" alt="SmartChef Logo" class="logo" />
    </div>
    <button class="add-button">+ Añadir receta</button>
    <h2>Recetas guardadas</h2>
    <div class="sidebar-scroll">
      {#each historial as item}
        <button title={item}>{item}</button>
      {/each}
    </div>
  </aside>

  <main class="main">
    <div class="main-header">
      <h1>Explora tus recetas</h1>
    </div>

    <div class="grid">
      {#each recetas as receta}
        <div class="card">
          <img src={receta.imagen || '/imagen-default.png'} alt="Imagen de receta" />
          <div class="card-content">
            <div class="receta-titulo">{receta.titulo}</div>
            <div class="receta-autor">por {receta.autor}</div>
          </div>
          <button class="ver-mas-btn" on:click={() => abrirModal(receta)}>Ver más</button>
        </div>
      {/each}
    </div>

    <div class="search-bar">
      <input type="text" placeholder="Buscar recetas..." />
      <span class="search-icon">🔍</span>
    </div>
  </main>
</div>

{#if recetaSeleccionada}
  <div class="modal-overlay" on:click={cerrarModal}>
    <div class="modal" on:click|stopPropagation>

      <header class="modal-header">
        <h2 class="modal-titulo">{recetaSeleccionada.titulo}</h2>
        <p class="autor">por {recetaSeleccionada.autor}</p>
      </header>

      <div class="modal-body">
        <img src={recetaSeleccionada.imagen || '/imagen-default.png'} alt="Imagen de receta" class="modal-img" />

        <div style="margin: 12px 0;">
          <label for="imagen-input" style="cursor: pointer; font-size: 14px; color: #2563eb;">
            📷 Cambiar imagen
          </label>
          <input id="imagen-input" type="file" accept="image/*" style="display: none;" on:change={(e) => {
            const file = e.target.files[0];
            if (file) {
              const reader = new FileReader();
              reader.onload = () => {
                recetaSeleccionada.imagen = reader.result;
                const index = recetas.findIndex(r => r.titulo === recetaSeleccionada?.titulo && r.autor === recetaSeleccionada?.autor);
                if (index !== -1) recetas[index].imagen = reader.result;
              };
              reader.readAsDataURL(file);
            }
          }} />
        </div>

        <p class="descripcion">
          Esta es una deliciosa receta que puedes preparar en casa.<br />
          Perfecta para cualquier ocasión y fácil de seguir.
        </p>

        <section class="seccion">
          <h3>🧂 Ingredientes</h3>
          <ul class="lista">
            <li>1 taza de ejemplo</li>
            <li>2 cucharadas de prueba</li>
            <li>Sal al gusto</li>
          </ul>
        </section>

        <section class="seccion">
          <h3>👨‍🍳 Paso a paso</h3>
          <ol class="lista">
            <li>Mezclar los ingredientes.</li>
            <li>Cocinar a fuego medio por 20 minutos.</li>
            <li>Servir y disfrutar.</li>
          </ol>
        </section>
      </div>

      <footer class="modal-footer">
        <button class="btn-cerrar" on:click={cerrarModal}>Cerrar</button>
      </footer>

    </div>
  </div>
{/if}
