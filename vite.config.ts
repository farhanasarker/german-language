/// <reference types="vitest" />
import { defineConfig } from "vite";
import preact from "@preact/preset-vite";
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig({
  plugins: [
    preact(),
    VitePWA({
      registerType: "autoUpdate",
      includeAssets: ["data/**/*.json"],
      manifest: {
        name: "German B1 Flashcards",
        short_name: "DE Flashcards",
        description: "Spaced repetition flashcards for Goethe B1 vocabulary",
        theme_color: "#2563eb",
        background_color: "#f5f5f5",
        display: "standalone",
        start_url: "/german-language/",
        scope: "/german-language/",
        icons: [
          {
            src: "icons/icon-192.png",
            sizes: "192x192",
            type: "image/png",
          },
          {
            src: "icons/icon-512.png",
            sizes: "512x512",
            type: "image/png",
          },
          {
            src: "icons/icon-512.png",
            sizes: "512x512",
            type: "image/png",
            purpose: "maskable",
          },
        ],
      },
      workbox: {
        globPatterns: ["**/*.{js,css,html,json,png,svg}"],
        runtimeCaching: [
          {
            urlPattern: /\/data\/.*\.json$/,
            handler: "CacheFirst",
            options: {
              cacheName: "deck-data",
              expiration: { maxEntries: 100, maxAgeSeconds: 7 * 24 * 60 * 60 },
            },
          },
        ],
      },
    }),
  ],
  base: "/german-language/",
  build: {
    outDir: "dist",
    minify: true,
  },
  test: {
    include: ["src/__tests__/**/*.test.ts"],
  },
});
