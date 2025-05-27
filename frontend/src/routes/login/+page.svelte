<script lang="ts">
	import { registerUser, loginUser } from '$lib/api';

	let modo = 'login';
	let nombre = '';
	let correo = '';
	let contraseña = '';
	let error = '';
	let mensaje = '';

	const handleSubmit = async () => {
		mensaje = '';
		error = '';

		try {
			if (modo === 'register') {
				const response = await registerUser(nombre, correo, contraseña);
				mensaje = response;
				modo = 'login';
			} else {
				const usuario = await loginUser(correo, contraseña);
				localStorage.setItem('usuario', JSON.stringify(usuario));
				mensaje = 'Inicio de sesión exitoso';
				window.location.href = '/home';
			}
		} catch (err) {
			if (err instanceof Error) {
				error = err.message;
			} else {
				error = 'Ocurrió un error inesperado';
			}
		}
	};
</script>

<div class="flex min-h-screen items-center justify-center bg-gray-100 px-4">
	<div class="w-full max-w-md rounded-2xl bg-white p-8 shadow-lg">
		<h1 class="mb-2 text-center text-3xl font-bold text-gray-800">
			{modo === 'login' ? 'Iniciar sesión' : 'Crear cuenta'}
		</h1>
		<p class="mb-6 text-center text-sm text-gray-500">
			{modo === 'login' ? 'Accede a tu mundo de recetas' : 'Crea una cuenta para comenzar'}
		</p>

		<!-- Selector de modo -->
		<div class="mb-6 flex justify-center">
			<button
				on:click={() => (modo = 'login')}
				class={`rounded-l-md px-4 py-2 text-sm font-semibold transition ${
					modo === 'login' ? 'bg-blue-800 text-white' : 'bg-gray-200 text-gray-700'
				}`}
			>
				Iniciar sesión
			</button>
			<button
				on:click={() => (modo = 'register')}
				class={`rounded-r-md px-4 py-2 text-sm font-semibold transition ${
					modo === 'register' ? 'bg-blue-800 text-white' : 'bg-gray-200 text-gray-700'
				}`}
			>
				Registrarse
			</button>
		</div>

		<!-- Mensajes -->
		{#if error}
			<div class="mb-4 rounded border border-red-300 bg-red-100 px-4 py-2 text-sm text-red-700">
				{error}
			</div>
		{/if}

		{#if mensaje}
			<div
				class="mb-4 rounded border border-green-300 bg-green-100 px-4 py-2 text-sm text-green-700"
			>
				{mensaje}
			</div>
		{/if}

		<!-- Formulario -->
		<form on:submit|preventDefault={handleSubmit} class="space-y-4">
			{#if modo === 'register'}
				<div>
					<label for="nombre" class="mb-1 block text-sm font-medium text-gray-700"
						>Nombre completo</label
					>
					<input id="nombre" type="text" bind:value={nombre} required class="input" />
				</div>
			{/if}

			<div>
				<label for="correo" class="mb-1 block text-sm font-medium text-gray-700"
					>Correo electrónico</label
				>
				<input id="correo" type="email" bind:value={correo} required class="input" />
			</div>

			<div>
				<label for="contraseña" class="mb-1 block text-sm font-medium text-gray-700"
					>Contraseña</label
				>
				<input id="contraseña" type="password" bind:value={contraseña} required class="input" />
			</div>

			<button
				type="submit"
				class="mt-2 w-full rounded-lg bg-blue-800 py-2 font-semibold text-white transition hover:bg-blue-700"
			>
				{modo === 'login' ? 'Entrar' : 'Registrarse'}
			</button>
		</form>
	</div>
</div>
