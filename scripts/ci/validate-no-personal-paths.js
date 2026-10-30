#!/usr/bin/env node
/**
 * Prevent shipping user-specific absolute paths in public docs/skills/commands.
 *
 * Catches generic `/Users/<name>` (macOS) and `C:\Users\<name>` (Windows) paths,
 * while allowing obvious placeholder usernames used in templates/examples.
 * Forensic incident reports under `docs/fixes/` are exempt because they may
 * legitimately document a reporter's local machine path.
 */

'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '../..');
const TARGETS = [
  'README.md',
  'skills',
  'commands',
  'agents',
  'docs',
  '.opencode/commands',
];

const EXEMPT_PREFIXES = [
  'docs/fixes/',
];

const PLACEHOLDER_USERNAMES = new Set([
  'example',
  'me',
  'user',
  'username',
  'you',
  'yourname',
  'yourusername',
  'your-username',
]);

const POSIX_USER_RE = /\/Users\/([a-zA-Z][a-zA-Z0-9._-]*)/g;
const WIN_USER_RE = /C:\\Users\\([a-zA-Z][a-zA-Z0-9._-]*)/gi;

function repoRelative(file) {
  return path.relative(ROOT, file).split(path.sep).join('/');
}

function isExempt(file) {
  const rel = repoRelative(file);
  return EXEMPT_PREFIXES.some(prefix => rel.startsWith(prefix));
}

function findLeaks(content) {
  const leaks = [];

  for (const pattern of [POSIX_USER_RE, WIN_USER_RE]) {
    pattern.lastIndex = 0;
    let match;

    while ((match = pattern.exec(content)) !== null) {
      if (!PLACEHOLDER_USERNAMES.has(match[1].toLowerCase())) {
        leaks.push(match[0]);
      }
    }
  }

  return leaks;
}

function collectFiles(targetPath, out) {
  if (!fs.existsSync(targetPath)) return;
  const stat = fs.statSync(targetPath);
  if (stat.isFile()) {
    out.push(targetPath);
    return;
  }

  for (const entry of fs.readdirSync(targetPath)) {
    if (entry === 'node_modules' || entry === '.git') continue;
    collectFiles(path.join(targetPath, entry), out);
  }
}

const files = [];
for (const target of TARGETS) {
  collectFiles(path.join(ROOT, target), files);
}

let failures = 0;
for (const file of files) {
  if (!/\.(md|json|js|ts|sh|toml|yml|yaml)$/i.test(file)) continue;
  if (isExempt(file)) continue;

  const content = fs.readFileSync(file, 'utf8');
  const leaks = findLeaks(content);

  for (const leak of leaks) {
    console.error(`ERROR: personal path "${leak}" detected in ${repoRelative(file)}`);
    failures += 1;
  }
}

// ── symlinks ───────────────────────────────────────────────────────────────
// `git ls-files -s` reports symlinks with mode 120000; the blob content is the
// link target, which is what `git show :<path>` prints.
const { execFileSync } = require('child_process');

function trackedSymlinks() {
  let listing;
  try {
    listing = execFileSync('git', ['ls-files', '-s'], { cwd: ROOT, encoding: 'utf8' });
  } catch {
    return null; // not a git checkout (npm package / sdist): nothing to check
  }
  const links = [];
  for (const line of listing.split('\n')) {
    if (!line.trim()) continue;
    const [meta, ...rest] = line.split('\t');
    if (meta.split(/\s+/)[0] !== '120000') continue;
    const file = rest.join('\t');
    const target = execFileSync('git', ['show', `:${file}`], { cwd: ROOT, encoding: 'utf8' }).trim();
    links.push({ file, target });
  }
  return links;
}

const links = trackedSymlinks();
if (links) {
  for (const { file, target } of links) {
    if (path.isAbsolute(target)) {
      console.error(`ERROR: symlink ${file} has an absolute target "${target}"`);
      failures += 1;
      continue;
    }
    const resolved = path.resolve(path.dirname(path.join(ROOT, file)), target);
    const relative = path.relative(ROOT, resolved);
    if (relative.startsWith('..') || path.isAbsolute(relative)) {
      console.error(`ERROR: symlink ${file} points outside the repository "${target}"`);
      failures += 1;
    }
  }
}

if (failures > 0) {
  process.exit(1);
}

console.log('Validated: no personal absolute paths or machine-local symlinks in shipped files');
