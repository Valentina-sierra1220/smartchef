<script lang="ts">
  let modo = 'login';
  let nombre = '';
  let correo = '';
  let contraseña = '';
  let error = '';
  let mensaje = '';

  const handleSubmit = async () => {
    error = '';
    mensaje = '';

    const url = modo === 'login'
      ? 'http://localhost:5000/login'
      : 'http://localhost:5000/register';

    const body = modo === 'login'
      ? { correo, contraseña }
      : { nombre, correo, contraseña };

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });

      const data = await response.json();

      if (response.ok) {
        mensaje = data.mensaje;
        if (modo === 'register') {
          modo = 'login';
          nombre = '';
        }
      } else {
        error = data.error || 'Error desconocido';
      }
    } catch (e) {
      error = 'No se pudo conectar con el servidor';
    }
  };
</script>

<div class="min-h-screen flex items-center justify-center bg-gray-100 px-4">
  <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-lg">
    <h1 class="text-3xl font-bold text-center text-gray-800 mb-2">
      {modo === 'login' ? 'Iniciar sesión' : 'Crear cuenta'}
    </h1>
    <p class="text-sm text-gray-500 text-center mb-6">
      {modo === 'login' ? 'Accede a tu mundo de recetas' : 'Crea una cuenta para comenzar'}
    </p>

    <!-- Selector de modo -->
    <div class="flex justify-center mb-6">
      <button
        on:click={() => (modo = 'login')}
        class={`px-4 py-2 rounded-l-md text-sm font-semibold transition ${
          modo === 'login'
            ? 'bg-blue-800 text-white'
            : 'bg-gray-200 text-gray-700'
        }`}>
        Iniciar sesión
      </button>
      <button
        on:click={() => (modo = 'register')}
        class={`px-4 py-2 rounded-r-md text-sm font-semibold transition ${
          modo === 'register'
            ? 'bg-blue-800 text-white'
            : 'bg-gray-200 text-gray-700'
        }`}>
        Registrarse
      </button>
    </div>

    <!-- Mensajes -->
    {#if error}
      <div class="bg-red-100 border border-red-300 text-red-700 px-4 py-2 rounded mb-4 text-sm">
        {error}
      </div>
    {/if}

    {#if mensaje}
      <div class="bg-green-100 border border-green-300 text-green-700 px-4 py-2 rounded mb-4 text-sm">
        {mensaje}
      </div>
    {/if}

    <!-- Formulario -->
    <form on:submit|preventDefault={handleSubmit} class="space-y-4">
      {#if modo === 'register'}
        <div>
          <label for="nombre" class="block text-sm font-medium text-gray-700 mb-1">Nombre completo</label>
          <input
            id="nombre"
            type="text"
            bind:value={nombre}
            required
            class="input"
          />
        </div>
      {/if}

      <div>
        <label for="correo" class="block text-sm font-medium text-gray-700 mb-1">Correo electrónico</label>
        <input
          id="correo"
          type="email"
          bind:value={correo}
          required
          class="input"
        />
      </div>

      <div>
        <label for="contraseña" class="block text-sm font-medium text-gray-700 mb-1">Contraseña</label>
        <input
          id="contraseña"
          type="password"
          bind:value={contraseña}
          required
          class="input"
        />
      </div>

      <button
        type="submit"
        class="w-full py-2 mt-2 text-white bg-blue-800 hover:bg-blue-700 font-semibold rounded-lg transition">
        {modo === 'login' ? 'Entrar' : 'Registrarse'}
      </button>
    </form>
  </div>
</div>

<style>
  .input {
    @apply w-full px-4 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500;
  }
</style>
