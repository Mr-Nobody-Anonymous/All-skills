#!/usr/bin/env node
/**
 * All-Skills CLI Node wrapper
 * Bridges npx / npm CLI invocations to Python allskills engine
 */
const { spawn } = require('child_process');
const path = require('path');

const repoRoot = path.resolve(__dirname, '..');
const pythonScript = path.join(repoRoot, 'scripts', 'allskills.py');

const args = process.argv.slice(2);
const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';

const child = spawn(pythonCmd, [pythonScript, ...args], {
  cwd: repoRoot,
  stdio: 'inherit',
  env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
});

child.on('close', (code) => {
  process.exit(code ?? 0);
});

child.on('error', (err) => {
  console.error(`Failed to start All-Skills CLI: ${err.message}`);
  console.error('Please ensure Python 3.10+ is installed and available on your PATH.');
  process.exit(1);
});
