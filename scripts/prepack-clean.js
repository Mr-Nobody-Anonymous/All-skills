#!/usr/bin/env node
/**
 * prepack cleanup for `npm pack` / `npm publish`.
 *
 * The package whitelist (`files` in package.json) covers whole directories, so
 * local __pycache__ directories and *.pyc/*.pyo files would silently ship in the
 * tarball. This script removes them (they are gitignored build artifacts) so a
 * locally packed artifact matches a fresh CI build. In a clean CI checkout this
 * is a no-op.
 */
const { readdirSync, rmSync, statSync } = require("node:fs");
const { join, relative } = require("node:path");

const ROOT = __dirname + "/..";
const SKIP = new Set([".git", "node_modules"]);
let removedDirs = 0;
let removedFiles = 0;

function walk(dir) {
  let entries;
  try {
    entries = readdirSync(dir, { withFileTypes: true });
  } catch {
    return;
  }
  for (const entry of entries) {
    if (SKIP.has(entry.name)) continue;
    const full = join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === "__pycache__") {
        rmSync(full, { recursive: true, force: true });
        removedDirs += 1;
        continue;
      }
      walk(full);
      continue;
    }
    if (entry.isFile() && /\.(pyc|pyo)$/.test(entry.name)) {
      rmSync(full, { force: true });
      removedFiles += 1;
    }
  }
}

walk(ROOT);
console.log(
  `prepack-clean: removed ${removedDirs} __pycache__ director${removedDirs === 1 ? "y" : "ies"} and ${removedFiles} bytecode file(s)`
);
