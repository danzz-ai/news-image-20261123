// news-image-20261123 — "The World Today — 23 November 2026".
// The entry is a single image, entry.png, drawn by render_front_page.py.
// This program only copies it to the grader's output directory, so every
// run writes exactly the same bytes. Node 22, standard library only.
//
// Run locally: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, statSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = new URL("./entry.png", import.meta.url);
const dest = join(outDir, "entry.png");
copyFileSync(src, dest);

// Fail loudly instead of silently shipping a partial copy: the two runs
// the grader makes must write the same bytes, so a short copy is an error.
if (statSync(dest).size !== statSync(src).size) {
  throw new Error(`entry.png copy incomplete: ${statSync(dest).size} bytes`);
}
console.log(`wrote ${dest} ${statSync(dest).size} bytes`);
