#!/usr/bin/env node

/**
 * Documentation Error Checker
 * 
 * Scans documentation for real errors that will cause problems:
 * - Deprecated <a name="..."> anchors (breaks navigation)
 * - Duplicate IDs in actual HTML (not in code blocks)
 * 
 * Run from your documentation project root:
 *   node check-doc-errors.js
 *   node check-doc-errors.js --fix
 */

const fs = require('fs').promises;
const path = require('path');

const CONFIG = {
  docsPath: './docs',
  fix: process.argv.includes('--fix'),
};

const report = {
  filesScanned: 0,
  issues: [],
  fixedCount: 0,
};

async function findDocFiles(dir) {
  const files = [];
  
  async function search(currentDir) {
    try {
      const entries = await fs.readdir(currentDir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(currentDir, entry.name);
        if (entry.isDirectory()) {
          if (!entry.name.startsWith('_') && entry.name !== 'node_modules') {
            await search(fullPath);
          }
        } else if (entry.isFile() && /\.(md|mdx)$/.test(entry.name)) {
          files.push(fullPath);
        }
      }
    } catch (err) { /* ignore */ }
  }
  
  await search(dir);
  return files;
}

function getLineNumber(content, index) {
  return content.substring(0, index).split('\n').length;
}

/**
 * Check if an index position is inside a code block
 */
function isInsideCodeBlock(content, index) {
  // Check if inside fenced code block (```)
  const beforeIndex = content.substring(0, index);
  const fenceMatches = beforeIndex.match(/```/g);
  if (fenceMatches && fenceMatches.length % 2 === 1) {
    return true; // Odd number of ``` means we're inside a code block
  }
  
  // Check if inside <pre> or <code> tags
  const lastPreOpen = beforeIndex.lastIndexOf('<pre');
  const lastPreClose = beforeIndex.lastIndexOf('</pre>');
  if (lastPreOpen > lastPreClose) {
    return true;
  }
  
  // Check if the line starts with 4 spaces or tab (indented code block)
  const lineStart = beforeIndex.lastIndexOf('\n') + 1;
  const linePrefix = content.substring(lineStart, index);
  if (/^(\s{4}|\t)/.test(linePrefix)) {
    return true;
  }
  
  // Check if inside inline code (`)
  const lineEnd = content.indexOf('\n', index);
  const line = content.substring(lineStart, lineEnd === -1 ? content.length : lineEnd);
  const posInLine = index - lineStart;
  
  let inBacktick = false;
  for (let i = 0; i < posInLine; i++) {
    if (line[i] === '`') inBacktick = !inBacktick;
  }
  if (inBacktick) return true;
  
  return false;
}

/**
 * Check for duplicate IDs in actual HTML elements (not in code blocks)
 */
function checkDuplicateIds(content, filePath) {
  const issues = [];
  const idPattern = /\bid=["']([^"']+)["']/gi;
  const ids = new Map();
  
  let match;
  while ((match = idPattern.exec(content)) !== null) {
    // Skip if inside code block
    if (isInsideCodeBlock(content, match.index)) {
      continue;
    }
    
    const id = match[1];
    const line = getLineNumber(content, match.index);
    
    if (ids.has(id)) {
      issues.push({
        line,
        match: `id="${id}"`,
        message: `Duplicate ID "${id}" (first at line ${ids.get(id)})`,
      });
    } else {
      ids.set(id, line);
    }
  }
  
  return issues;
}

/**
 * Check for deprecated <a name="..."> anchors (not in code blocks)
 */
function checkDeprecatedAnchors(content, filePath) {
  const issues = [];
  const pattern = /<a\s+name=["']([^"']+)["']\s*>\s*<\/a>/gi;
  
  let match;
  while ((match = pattern.exec(content)) !== null) {
    // Skip if inside code block
    if (isInsideCodeBlock(content, match.index)) {
      continue;
    }
    
    const line = getLineNumber(content, match.index);
    issues.push({
      line,
      match: match[0].substring(0, 80),
      suggestion: `Change to id="${match[1]}"`,
    });
  }
  
  return issues;
}

async function checkFile(filePath) {
  try {
    let content = await fs.readFile(filePath, 'utf8');
    const relPath = path.relative(CONFIG.docsPath, filePath).replace(/\\/g, '/');
    let modified = false;
    
    // Check for duplicate IDs
    const dupes = checkDuplicateIds(content, filePath);
    for (const dupe of dupes) {
      report.issues.push({
        file: relPath,
        name: 'Duplicate ID attributes',
        line: dupe.line,
        match: dupe.match,
        message: dupe.message,
      });
    }
    
    // Check for deprecated anchors
    const anchors = checkDeprecatedAnchors(content, filePath);
    for (const anchor of anchors) {
      report.issues.push({
        file: relPath,
        name: 'Deprecated <a name="..."> anchor',
        line: anchor.line,
        match: anchor.match,
        suggestion: anchor.suggestion,
      });
    }
    
    // Apply fix for <a name="..."> in table cells
    if (CONFIG.fix) {
      const fixPattern = /<td><a\s+name=["']([^"']+)["']\s*><\/a>/gi;
      const before = content;
      content = content.replace(fixPattern, '<td id="$1">');
      if (content !== before) {
        modified = true;
        report.fixedCount += (before.match(fixPattern) || []).length;
      }
    }
    
    if (modified) {
      await fs.writeFile(filePath, content, 'utf8');
    }
    
  } catch (err) {
    console.error(`Error: ${filePath}: ${err.message}`);
  }
}

async function main() {
  console.log('🔍 Documentation Error Checker\n');
  
  try {
    await fs.access(CONFIG.docsPath);
  } catch {
    console.error('Error: docs/ directory not found');
    process.exit(1);
  }
  
  const files = await findDocFiles(CONFIG.docsPath);
  report.filesScanned = files.length;
  
  for (const file of files) {
    await checkFile(file);
  }
  
  // Print results
  console.log('='.repeat(60));
  
  if (report.issues.length === 0) {
    console.log('✅ No errors found!\n');
  } else {
    console.log(`❌ Found ${report.issues.length} error(s):\n`);
    
    // Group by file
    const byFile = {};
    report.issues.forEach(issue => {
      if (!byFile[issue.file]) byFile[issue.file] = [];
      byFile[issue.file].push(issue);
    });
    
    for (const [file, issues] of Object.entries(byFile)) {
      console.log(`  ${file}:`);
      issues.forEach(issue => {
        console.log(`    Line ${issue.line}: ${issue.name}`);
        console.log(`      ${issue.match}`);
        if (issue.suggestion) console.log(`      → ${issue.suggestion}`);
        if (issue.message) console.log(`      → ${issue.message}`);
      });
      console.log();
    }
  }
  
  console.log('='.repeat(60));
  console.log(`Files scanned: ${report.filesScanned}`);
  console.log(`Errors found: ${report.issues.length}`);
  if (CONFIG.fix) console.log(`Errors fixed: ${report.fixedCount}`);
  console.log('='.repeat(60) + '\n');
  
  if (!CONFIG.fix && report.issues.length > 0) {
    console.log('💡 Run with --fix to auto-fix <a name="..."> issues\n');
  }
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
