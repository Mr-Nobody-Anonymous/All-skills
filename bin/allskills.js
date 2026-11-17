#!/usr/bin/env node
/**
 * npm / npx entry point for the All-Skills CLI (scripts/allskills.py).
 *
 * Workspace (same rule as the Python CLIs):
 *   1. --workspace PATH or ALL_SKILLS_WORKSPACE
 *   2. the nearest directory, from the current one upwards, containing skills/registry.json
 *   3. the files shipped in this npm package
 * The workspace's own scripts/allskills.py is used when it has one, so a checkout
 * and the npm package expose the same commands.
 *
 * Requires Python >= 3.10 with the dependencies from requirements.txt.
 */
'use strict';

const { spawn, spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const packageRoot = path.resolve(__dirname, '..');
const isWorkspace = (dir) => fs.existsSync(path.join(dir, 'skills', 'registry.json'));

function takeWorkspaceFlag(args) {
  const rest = [];
  let workspace = null;
  for (let i = 0; i < args.length; i += 1) {
    if (args[i] === '--workspace') {
      workspace = args[i + 1];
      i += 1;
    } else if (args[i].startsWith('--workspace=')) {
      workspace = args[i].slice('--workspace='.length);
    } else {
      rest.push(args[i]);
    }
  }
  return { workspace, rest };
}

function findWorkspace(explicit) {
  const requested = explicit || process.env.ALL_SKILLS_WORKSPACE;
  if (requested) {
    const dir = path.resolve(requested);
    if (!isWorkspace(dir)) {
      console.error(`Error: ${dir} is not an All-Skills workspace (no skills/registry.json).`);
      process.exit(2);
    }
    return dir;
  }
  let dir = process.cwd();
  for (;;) {
    if (isWorkspace(dir)) return dir;
    const parent = path.dirname(dir);
    if (parent === dir) return packageRoot;
    dir = parent;
  }
}

const CHECK = [
  'import sys',
  'if sys.version_info < (3, 10): sys.exit(2)',
  'try:',
  '    import yaml, jsonschema, networkx  # noqa: F401',
  'except ImportError:',
  '    sys.exit(3)',
].join('\n');

function findPython() {
  const candidates = process.platform === 'win32'
    ? [['py', ['-3']], ['python', []], ['python3', []]]
    : [['python3', []], ['python', []]];
  let sawOldOrMissingDeps = null;
  for (const [cmd, prefix] of candidates) {
    const probe = spawnSync(cmd, [...prefix, '-c', CHECK], { encoding: 'utf8' });
    if (probe.error) continue;
    if (probe.status === 0) return { cmd, prefix };
    sawOldOrMissingDeps = sawOldOrMissingDeps || probe.status;
  }
  const requirements = path.join(packageRoot, 'requirements.txt');
  if (sawOldOrMissingDeps === 3) {
    console.error(`All-Skills needs its Python dependencies. Install them with:\n  python3 -m pip install -r "${requirements}"`);
  } else if (sawOldOrMissingDeps === 2) {
    console.error('All-Skills requires Python 3.10 or newer.');
  } else {
    console.error('Python 3.10+ was not found on PATH. Install Python, then run:\n'
      + `  python3 -m pip install -r "${requirements}"`);
  }
  process.exit(1);
}

const { workspace: flag, rest } = takeWorkspaceFlag(process.argv.slice(2));
const workspace = findWorkspace(flag);
const script = fs.existsSync(path.join(workspace, 'scripts', 'allskills.py'))
  ? path.join(workspace, 'scripts', 'allskills.py')
  : path.join(packageRoot, 'scripts', 'allskills.py');
const python = findPython();

const child = spawn(python.cmd, [...python.prefix, script, ...rest], {
  cwd: workspace,
  stdio: 'inherit',
  env: { ...process.env, ALL_SKILLS_WORKSPACE: workspace, PYTHONIOENCODING: 'utf-8' },
});
child.on('close', (code) => process.exit(code ?? 1));
child.on('error', (err) => {
  console.error(`Failed to start the All-Skills CLI: ${err.message}`);
  process.exit(1);
});
