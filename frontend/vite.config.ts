import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // Keep the demo runnable when another local project already owns 5173.
    strictPort: false,
  },
});
