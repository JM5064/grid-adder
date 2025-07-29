// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { viteStaticCopy } from "vite-plugin-static-copy";

export default defineConfig({
  plugins: [
    react(),
    viteStaticCopy({
      targets: [
        // *** CHANGE THIS PATH if needed ***
        // Run the "Find the path quickly" command below to locate opencv_js.wasm
        {
          src: "node_modules/onnxruntime-web/dist/*.wasm",
          dest: "." // will end up at /opencv/opencv_js.wasm
        }
      ]
    })
  ],
  assetsInclude: ["**/*.wasm"], // make sure Vite serves wasm correctly
});
