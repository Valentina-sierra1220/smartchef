<script lang="ts">
	import ModalVerReceta from './modals/ModalVerReceta.svelte';
	import ModalCrearReceta from './modals/ModalCrearReceta.svelte';
	import BarraLateral from './components/BarraLateral.svelte';
	import CuadriculaRecetas from './components/CuadriculaRecetas.svelte';
	import BarraBusqueda from './components/BarraBusqueda.svelte';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	import { Receta } from '$model/Receta';
	import { Imagen } from '$model/Imagen';
	import { Usuario } from '$model/Usuario';

	import { obtenerMisRecetas } from '$lib/api';
	import { editarReceta } from '$lib/api';

	let historial: Receta[] = [];
	let recetasCompartidas: Receta[] = [];
	let showModal = false;
	let showCrearModal = false;
	let recetaSeleccionada: Receta | null = null;
	let modoEdicion = false;
	let usuario: Usuario | null = null;

	const abrirModal = (r: Receta) => {
		recetaSeleccionada = r;
		showModal = true;
	};

	function abrirEditarReceta(receta: Receta) {
		recetaSeleccionada = receta;
		modoEdicion = true;
		showModal = false;
		showCrearModal = true;
	}
	const cerrarModal = () => (showModal = false);
	const abrirCrearModal = () => (showCrearModal = true);
	const cerrarCrearModal = () => {
		showCrearModal = false;
		modoEdicion = false;
		recetaSeleccionada = null;
	};

	const cerrarSesion = () => {
		localStorage.removeItem('usuario');
		goto('/login');
	};

	// ✅ Cargar usuario y recetas personales
	onMount(async () => {
		try {
			const json = localStorage.getItem('usuario');
			usuario = json ? Usuario.fromJson(JSON.parse(json)) : null;

			if (usuario) {
				historial = await obtenerMisRecetas(Number(usuario.id));
			}
		} catch (err) {
			console.error('❌ Error al cargar recetas personales:', err);
		}
	});

	function guardarRecetaDesdeModal(receta: Receta) {
		// Agrega la receta al historial
		historial = [receta, ...historial];

		// Si es pública, también al feed compartido
		if (receta.publica) {
			recetasCompartidas = [receta, ...recetasCompartidas];
		}

		cerrarCrearModal();
		modoEdicion = false;
	}

	function compartirReceta(r: Receta) {
		if (!recetasCompartidas.some((x) => x.id === r.id)) {
			recetasCompartidas = [r, ...recetasCompartidas];
		}
	}

	function actualizarRecetaEditada(editada: Receta) {
		historial = historial.map((r) => (r.id === editada.id ? editada : r));
		recetasCompartidas = editada.publica
			? [editada, ...recetasCompartidas.filter((r) => r.id !== editada.id)]
			: recetasCompartidas.filter((r) => r.id !== editada.id);
		recetaSeleccionada = editada;
	}

	async function manejarEdicionReceta(receta: Receta) {
		try {
			// Actualiza en backend
			await editarReceta(receta);

			// Reemplaza en historial
			historial = historial.map((r) => (r.id === receta.id ? receta : r));
			recetaSeleccionada = receta;

			// Actualiza en el feed compartido
			if (receta.publica && !recetasCompartidas.some((r) => r.id === receta.id)) {
				recetasCompartidas = [receta, ...recetasCompartidas];
			} else if (!receta.publica) {
				recetasCompartidas = recetasCompartidas.filter((r) => r.id !== receta.id);
			}

			cerrarCrearModal();
			modoEdicion = false;
		} catch (err) {
			console.error('❌ Error al editar receta:', err);
			alert('Ocurrió un error al actualizar la receta');
		}
	}
</script>

<div class="layout">
	<div class="absolute right-6 top-4 z-50">
		<button on:click={cerrarSesion} class="text-sm font-semibold text-red-600 hover:underline"
			>Cerrar sesión</button
		>
	</div>

	<BarraLateral {historial} {abrirCrearModal} {abrirModal} />

	<main class="main">
		<div class="main-header">
			<h1>
				Explora tus recetas{#if usuario}, {usuario.nombre}{/if}
			</h1>
		</div>

		<div class="contenido-recetas">
			{#if recetasCompartidas.length === 0}
				<div class="flex h-full w-full items-center justify-center">
					<div class="text-center text-lg leading-relaxed text-gray-500">
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
		usuario={usuario!}
		on:compartir={(e) => {
			compartirReceta(e.detail);
			cerrarModal();
		}}
		on:editado={(e) => actualizarRecetaEditada(e.detail)}
		on:editar={(e) => abrirEditarReceta(e.detail)}
	/>
{/if}

{#if showCrearModal}
	<ModalCrearReceta
		show={showCrearModal}
		editar={modoEdicion}
		recetaAEditar={modoEdicion ? recetaSeleccionada : null}
		onClose={cerrarCrearModal}
		onGuardar={guardarRecetaDesdeModal}
		onEditar={manejarEdicionReceta}
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
