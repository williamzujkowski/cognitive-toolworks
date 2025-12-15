#!/usr/bin/env node
// TypeScript CLI Example: simple file counter
// Demonstrates: shebang, arg parsing, exit codes, fs operations

import { readdirSync, statSync } from 'fs';
import { resolve } from 'path';

interface CountResult {
  files: number;
  directories: number;
}

function countItems(dirPath: string): CountResult {
  const items = readdirSync(dirPath);
  const result: CountResult = { files: 0, directories: 0 };

  items.forEach(item => {
    const fullPath = resolve(dirPath, item);
    statSync(fullPath).isDirectory() ? result.directories++ : result.files++;
  });

  return result;
}

const [,, targetDir = '.'] = process.argv;
const result = countItems(targetDir);
console.log(`📁 ${result.directories} directories, 📄 ${result.files} files`);
process.exit(0);
