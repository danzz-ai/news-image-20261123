// news-image-20261123 — "The World Today — 23 November 2026".
// The entry is one pre-rendered image. This program copies entry.png into
// the directory the grader passes in, so both grader runs write identical
// bytes. Node 22, standard library only.

import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const sourcePath = fileURLToPath(new URL("./entry.png", import.meta.url));
if (!existsSync(sourcePath)) {
  throw new Error(`entry.png missing next to main.ts: ${sourcePath}`);
}
const targetPath = join(outputDir, "entry.png");

mkdirSync(dirname(targetPath), { recursive: true });
copyFileSync(sourcePath, targetPath);

const sourceSize = statSync(sourcePath).size;
const targetSize = statSync(targetPath).size;
if (targetSize !== sourceSize) {
  throw new Error(`incomplete copy: wrote ${targetSize} of ${sourceSize} bytes`);
}
console.log(`entry.png -> ${targetPath} (${targetSize} bytes)`);
