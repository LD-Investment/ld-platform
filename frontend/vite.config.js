import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(({ command, mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  return {
    define: {
      __APP_ENV__: env.APP_ENV
    },
    root: "./ld_platform_web/src",
    publicDir: "../public",
    build: {
      // Relative to the root
      outDir: "../build"
    },
    plugins: [
      react({
        // Use React plugin in all *.jsx and *.tsx files
        include: ["**/*.{js,jsx}", "**/**/*.{js,jsx}"]
      })
    ],
    server: {
      host: "0.0.0.0",
      port: 9000,
      strictPort: true,
      hmr: {
        clientPort: 8080,
        port: 8080
      }
    }
  };
});
