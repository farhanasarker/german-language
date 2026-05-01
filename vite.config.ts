/// <reference types="vitest" />
import { defineConfig } from "vite";
import preact from "@preact/preset-vite";

export default defineConfig({
  plugins: [preact()],
  base: "/german-language/",
  build: {
    outDir: "dist",
    minify: true,
  },
  test: {
    include: ["src/__tests__/**/*.test.ts"],
  },
});
