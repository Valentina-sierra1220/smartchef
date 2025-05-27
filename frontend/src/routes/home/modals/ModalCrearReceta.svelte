<script lang="ts">
	import { crearReceta, guardarUrlsImagenes } from '$lib/api';
	import { subirMultiplesImagenes } from '$lib/imageUtils';
	import { Receta } from '$model/Receta';
	import { Imagen } from '$model/Imagen';
	import { Usuario } from '$model/Usuario';
	import { construirUrlImagen } from '$lib/url';

	export let show = false;
	export let onClose: () => void;
	export let editar: boolean = false;
	export let recetaAEditar: Receta | null = null;
	export let onGuardar: (receta: Receta) => void;
	export let onEditar: (receta: Receta) => void;

	let titulo = '';
	let descripcion = '';
	let instrucciones = '';
	let tiempo = '';
	let porciones = 1;
	let publica = false;

	let imagenes: string[] = [];
	let archivosSeleccionados: File[] = [];
	let currentIndex = 0;
	let cargando = false;

	$: if (editar && recetaAEditar) {
		titulo = recetaAEditar.nombre;
		descripcion = recetaAEditar.descripcion;
		instrucciones = recetaAEditar.instrucciones;
		tiempo = recetaAEditar.tiempo;
		porciones = recetaAEditar.porciones;
		publica = recetaAEditar.publica;
		imagenes = recetaAEditar.imagenes?.map((i) => i.url) || [];
	}
    $: if (!editar && show) {
	titulo = '';
	descripcion = '';
	instrucciones = '';
	tiempo = '';
	porciones = 1;
	publica = false;
	imagenes = [];
	currentIndex = 0;
	archivosSeleccionados = [];
}

	async function handleFileChange(event: Event) {
		const files = (event.target as HTMLInputElement)?.files;
		if (!files || files.length === 0) return;
		archivosSeleccionados = Array.from(files);
	}

	async function guardarReceta() {
		cargando = true;
		try {
			const urls = await subirMultiplesImagenes(archivosSeleccionados);
			imagenes = [...imagenes, ...urls];

			const usuarioJson = localStorage.getItem('usuario');
			const usuario = usuarioJson ? Usuario.fromJson(JSON.parse(usuarioJson)) : null;
			if (!usuario) throw new Error('No se encontró el usuario activo');

			const imagenesFinales = imagenes.map((url) => new Imagen(url, usuario.id));

			if (editar && recetaAEditar) {
				const recetaEditada = new Receta(
					recetaAEditar.id, // mantener ID original
					titulo,
					descripcion,
					instrucciones,
					tiempo,
					porciones,
					publica,
					String(usuario.id),
					imagenesFinales
				);

				onEditar(recetaEditada); // ✅ usa la prop como callback
			} else {
				const nuevaReceta = new Receta(
					'',
					titulo,
					descripcion,
					instrucciones,
					tiempo,
					porciones,
					publica,
					String(usuario.id),
					imagenesFinales
				);

				const recetaCreada = await crearReceta(nuevaReceta);

				if (urls.length > 0) {
					await guardarUrlsImagenes(Number(recetaCreada.id), urls);
				}

				onGuardar(recetaCreada); // ✅ usa la prop como callback
			}

			onClose();
		} catch (err) {
			console.error('❌ Error al guardar:', err);
			alert('Ocurrió un error al guardar la receta');
		} finally {
			cargando = false;
		}
	}
</script>

{#if show}
	<div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4">
		<div
			class="relative max-h-[92vh] w-full max-w-2xl overflow-y-auto rounded-2xl bg-white p-8 shadow-xl dark:bg-zinc-900"
		>
			<button
				on:click={onClose}
				class="absolute right-4 top-4 text-2xl font-bold text-zinc-400 hover:text-zinc-200"
				aria-label="Cerrar">×</button
			>

			<h2 class="mb-8 text-center text-2xl font-bold text-zinc-800 dark:text-zinc-100">
				{editar ? 'Editar receta' : 'Crear nueva receta'}
			</h2>

			<div class="space-y-6 text-sm text-zinc-800 dark:text-zinc-100">
				<div>
					<label for="titulo" class="mb-1 block font-medium text-zinc-700 dark:text-zinc-200"
						>Título</label
					>
					<input
						id="titulo"
						bind:value={titulo}
						class="w-full rounded-lg border border-zinc-300 bg-white px-4 py-2 text-zinc-900 transition focus:outline-none focus:ring-2 focus:ring-zinc-400 dark:border-zinc-600 dark:bg-zinc-800 dark:text-zinc-100"
					/>
				</div>

				<div>
					<label for="descripcion" class="mb-1 block font-medium text-zinc-700 dark:text-zinc-200"
						>Descripción</label
					>
					<textarea
						id="descripcion"
						bind:value={descripcion}
						rows="2"
						class="w-full resize-none rounded-lg border border-zinc-300 bg-white px-4 py-2 text-zinc-900 transition focus:outline-none focus:ring-2 focus:ring-zinc-400 dark:border-zinc-600 dark:bg-zinc-800 dark:text-zinc-100"
					></textarea>
				</div>

				<div>
					<label for="instrucciones" class="mb-1 block font-medium text-zinc-700 dark:text-zinc-200"
						>Instrucciones</label
					>
					<textarea
						id="instrucciones"
						bind:value={instrucciones}
						rows="4"
						class="w-full resize-none rounded-lg border border-zinc-300 bg-white px-4 py-2 text-zinc-900 transition focus:outline-none focus:ring-2 focus:ring-zinc-400 dark:border-zinc-600 dark:bg-zinc-800 dark:text-zinc-100"
					></textarea>
				</div>

				<div class="flex flex-col gap-4 sm:flex-row">
					<div class="flex-1">
						<label for="tiempo" class="mb-1 block font-medium text-zinc-700 dark:text-zinc-200"
							>Tiempo</label
						>
						<input
							id="tiempo"
							bind:value={tiempo}
							class="w-full rounded-lg border border-zinc-300 bg-white px-4 py-2 text-zinc-900 transition focus:outline-none focus:ring-2 focus:ring-zinc-400 dark:border-zinc-600 dark:bg-zinc-800 dark:text-zinc-100"
						/>
					</div>

					<div class="flex-1">
						<label for="porciones" class="mb-1 block font-medium text-zinc-700 dark:text-zinc-200"
							>Porciones</label
						>
						<input
							id="porciones"
							type="number"
							bind:value={porciones}
							min="1"
							class="w-full rounded-lg border border-zinc-300 bg-white px-4 py-2 text-zinc-900 transition focus:outline-none focus:ring-2 focus:ring-zinc-400 dark:border-zinc-600 dark:bg-zinc-800 dark:text-zinc-100"
						/>
					</div>
				</div>

				<div class="flex items-center gap-2">
					<input
						type="checkbox"
						id="publica"
						bind:checked={publica}
						class="accent-zinc-700 dark:accent-zinc-500"
					/>
					<label for="publica" class="font-medium text-zinc-700 dark:text-zinc-200"
						>¿Hacer pública la receta?</label
					>
				</div>

				<div>
					<label for="imagenes" class="mb-1 block font-medium text-zinc-700 dark:text-zinc-200"
						>Imágenes</label
					>
					<input
						id="imagenes"
						type="file"
						accept="image/*"
						multiple
						on:change={handleFileChange}
						class="text-zinc-700 file:rounded-lg file:border-0 file:bg-zinc-100 file:px-4 file:py-2 file:font-medium file:text-zinc-800"
					/>
				</div>

				{#if cargando}
					<p class="text-center text-zinc-500">Subiendo imágenes...</p>
				{/if}

				{#if imagenes.length > 0}
					<div class="relative">
						<img
							src={construirUrlImagen(imagenes[currentIndex])}
							alt="Imagen subida"
							class="h-[250px] w-full rounded-lg border object-contain"
						/>

						{#if imagenes.length > 1}
							<button
								on:click={() =>
									(currentIndex = (currentIndex - 1 + imagenes.length) % imagenes.length)}
								class="absolute left-3 top-1/2 -translate-y-1/2 rounded-full bg-white p-2 text-black shadow hover:bg-zinc-100 dark:bg-zinc-700 dark:text-white dark:hover:bg-zinc-600"
								>◀</button
							>

							<button
								on:click={() => (currentIndex = (currentIndex + 1) % imagenes.length)}
								class="absolute right-3 top-1/2 -translate-y-1/2 rounded-full bg-white p-2 text-black shadow hover:bg-zinc-100 dark:bg-zinc-700 dark:text-white dark:hover:bg-zinc-600"
								>▶</button
							>

							<div class="mt-2 text-center text-sm text-zinc-500 dark:text-zinc-400">
								Imagen {currentIndex + 1} de {imagenes.length}
							</div>
						{/if}
					</div>
				{/if}
			</div>

			<div class="mt-10 flex justify-end gap-3">
				<button
					on:click={onClose}
					class="rounded-lg bg-zinc-200 px-5 py-2 font-semibold text-zinc-800 transition hover:bg-zinc-300 dark:bg-zinc-700 dark:text-white dark:hover:bg-zinc-600"
				>
					Cancelar
				</button>
				<button
					on:click={guardarReceta}
					class="rounded-lg bg-zinc-700 px-5 py-2 font-semibold text-white transition hover:bg-zinc-800"
				>
					{editar ? 'Guardar cambios' : 'Guardar receta'}
				</button>
			</div>
		</div>
	</div>
{/if}
