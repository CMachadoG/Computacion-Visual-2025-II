import { defineConfig } from 'vite';

export default defineConfig({
  // ESTO ES LO CRUCIAL: Le dice a Vite que el código fuente está en la carpeta 'src'.
  root: './src', 
  
  // Esto es opcional, pero ayuda a asegurar que el servidor abra la página correcta.
  server: {
    open: '/index.html',
  }
});