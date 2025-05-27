<script lang="ts">
	import type { Receta } from '$model/Receta';
    import { construirUrlImagen } from '$lib/url';

	export let historial: Receta[] = []; // Mis recetas
	export let recetasGuardadas: Receta[] = [];
	export let abrirCrearModal: () => void;
	export let abrirModal: (receta: Receta) => void;
</script>

<aside class="sidebar">
	<div class="logo-container">
		<img src="/logo.jpg" alt="SmartChef Logo" class="logo" />
	</div>

	<button class="add-button" on:click={abrirCrearModal}>+ Crear receta</button>

	<!-- 🔹 Sección: Mis recetas -->
	<h2>Mis recetas</h2>
	<div class="sidebar-scroll">
		{#if historial.length === 0}
			<p style="font-size: 13px; opacity: 0.7;">No has creado recetas aún.</p>
		{:else}
			{#each historial as receta (receta.id)}
				{#if receta.nombre}
					<button class="receta-item" on:click={() => abrirModal(receta)} title={receta.nombre}>
						{#if receta.imagenes.length > 0}
							<img src={construirUrlImagen(receta.imagenes[0]?.url)} alt="Imagen" class="miniatura" />
						{/if}
						<span>{receta.nombre}</span>
					</button>
				{/if}
			{/each}
		{/if}
	</div>

	<!-- 🔹 Sección: Recetas guardadas -->
	<h2 style="margin-top: 24px;">Recetas guardadas</h2>
	<div class="sidebar-scroll">
		{#if recetasGuardadas.length === 0}
			<p style="font-size: 13px; opacity: 0.7;">No hay recetas guardadas aún.</p>
		{:else}
			{#each recetasGuardadas as receta (receta.id)}
				{#if receta.nombre}
					<button class="receta-item" on:click={() => abrirModal(receta)} title={receta.nombre}>
						{#if receta.imagenes.length > 0}
							<img src={construirUrlImagen(receta.imagenes[0]?.url)} alt="Imagen" class="miniatura" />
						{/if}
						<span>{receta.nombre}</span>
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
		font-size: 16px;
		font-weight: 600;
		margin-bottom: 8px;
		margin-top: 16px;
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

    .receta-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.receta-item .miniatura {
  width: 24px;
  height: 24px;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid white;
}
</style>
