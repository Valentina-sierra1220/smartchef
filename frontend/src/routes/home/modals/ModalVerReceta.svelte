<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import type { Receta } from '$model/Receta';
	import { construirUrlImagen } from '$lib/url';
	import { Usuario } from '$model/Usuario';

	export let show = false;
	export let receta: Receta;
	export let onClose: () => void;
	export let usuario: Usuario;

	const dispatch = createEventDispatcher();

	const compartirReceta = () => dispatch('compartir', receta);
	const editar = () => dispatch('editar', receta);
	const esPropia = receta.id_usuario.toString() === usuario.id.toString();
	const esPublica = receta.publica;
</script>

{#if show}
	<div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
		<div class="relative w-full max-w-md overflow-hidden rounded-2xl bg-white shadow-xl">
			<!-- Header con título centrado y botón cerrar alineado -->
			<div class="relative flex items-center justify-center border-b p-4">
				<h2 class="w-full text-center text-lg font-semibold">{receta.nombre}</h2>
				<button
					on:click={onClose}
					class="absolute right-4 top-4 text-xl text-gray-500 hover:text-gray-800">×</button
				>
			</div>

			<!-- 🔹 Imagen -->
			{#if receta.imagenes.length > 0}
				<img
					src={construirUrlImagen(receta.imagenes[0].url)}
					alt="Receta"
					class="h-48 w-full object-cover"
				/>
			{:else}
				<div class="flex h-48 w-full items-center justify-center bg-gray-100 text-gray-400">
					📷 Sin imagen
				</div>
			{/if}

			<div class="p-6">
				<!-- 🔹 Info alineada izquierda -->
				<div class="mb-4 flex gap-4 text-sm text-gray-600">
					<span>⏱️ {receta.tiempo}</span>
					<span>🍽️ {receta.porciones} porciones</span>
					<span>{receta.publica ? '🌐 Pública' : '🔒 Privada'}</span>
				</div>

				<!-- 🔹 Descripción -->
				<h3 class="mb-1 text-sm font-semibold">Descripción</h3>
				<p class="mb-4 text-sm text-gray-700">{receta.descripcion}</p>

				<!-- 🔹 Instrucciones -->
				<h3 class="mb-1 text-sm font-semibold">Instrucciones</h3>
				<ol class="ml-5 list-decimal space-y-1 text-sm text-gray-700">
					{#each receta.instrucciones.split('\n').filter((p) => p.trim()) as paso}
						<li>{paso}</li>
					{/each}
				</ol>

				<!-- 🔹 Botones -->
				<div class="mt-6 flex flex-col gap-3">
					{#if esPropia}
						<div class="mt-6 flex gap-2">
							{#if receta.publica}
								<button
									on:click={print}
									class="flex-1 rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white hover:bg-red-700"
									>🔒 Privada</button
								>
							{:else}
								<button
									on:click={compartirReceta}
									class="flex-1 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-700"
									>🌐 Pública</button
								>
							{/if}

							<button
  on:click={() => dispatch('editar', receta)}
  class="flex-1 border border-gray-300 py-2 rounded-lg text-sm hover:bg-gray-100">
  ✏️ Editar
</button>

							
						</div>
					{:else}
						<!-- 📥 Botón de guardar centrado -->
						<div class="mt-6 flex justify-center">
							<button
								on:click={() => dispatch('guardar', receta)}
								class="w-full max-w-[300px] rounded-lg bg-green-600 px-4 py-2 text-sm font-semibold text-white hover:bg-green-700"
								>📥 Guardar receta</button
							>
						</div>
					{/if}
				</div>
			</div>
		</div>
	</div>
{/if}
