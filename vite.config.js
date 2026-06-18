import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import { resolve } from "path";
import fs from "fs";

const htmlFiles = {};

fs.readdirSync(__dirname)
  .filter((file) => file.endsWith(".html"))
  .forEach((file) => {
    const name = file.replace(".html", "");
    htmlFiles[name] = resolve(__dirname, file);
  });

export default defineConfig({
    plugins: [
    tailwindcss(),
  ],
  build: {
    rollupOptions: {
      input: htmlFiles,
    },
  },
});