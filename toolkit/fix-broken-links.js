#!/usr/bin/env node

/**
 * Fix Broken Markdown Links
 * 
 * This script fixes broken markdown links where:
 * 1. Links point to .md files but actual files are .mdx
 * 2. Links have incorrect relative paths
 * 
 * Run from your documentation project root:
 *   node fix-broken-links.js --dry-run
 *   node fix-broken-links.js
 */

const fs = require('fs').promises;
const path = require('path');

const CONFIG = {
  docsPath: './docs',
  dryRun: process.argv.includes('--dry-run'),
};

// Known fixes based on the warnings
const LINK_FIXES = [
  // process-engine.md -> process-engine.mdx (in deployment-descriptors/tags/)
  {
    pattern: /(deployment-descriptors\/tags\/process-engine)\.md(#[^\s)\]]*)?/g,
    replacement: '$1.mdx$2',
    description: 'Fix process-engine.md -> process-engine.mdx'
  },
  // configuration.md -> configuration.mdx (for spring-boot-integration)
  {
    pattern: /(spring-boot-integration\/configuration)\.md(#[^\s)\]]*)?/g,
    replacement: '$1.mdx$2',
    description: 'Fix spring-boot-integration/configuration.md -> configuration.mdx'
  },
];

const report = {
  filesScanned: 0,
  filesModified: 0,
  fixesApplied: 0,
  fixes: []
};

async function findMarkdownFiles(dir) {
  const files = [];
  
  async function search(currentDir) {
    try {
      const entries = await fs.readdir(currentDir, { withFileTypes: true });
      
      for (const entry of entries) {
        const fullPath = path.join(currentDir, entry.name);
        
        if (entry.isDirectory()) {
          if (entry.name.startsWith('_') || entry.name === 'node_modules') {
            continue;
          }
          await search(fullPath);
        } else if (entry.isFile() && /\.(md|mdx)$/.test(entry.name)) {
          files.push(fullPath);
        }
      }
    } catch (err) {
      // Ignore errors
    }
  }
  
  await search(dir);
  return files;
}

async function fixFile(filePath) {
  try {
    let content = await fs.readFile(filePath, 'utf8');
    let modified = false;
    const fileRelPath = path.relative(CONFIG.docsPath, filePath);
    
    for (const fix of LINK_FIXES) {
      const matches = content.match(fix.pattern);
      if (matches) {
        const originalContent = content;
        content = content.replace(fix.pattern, fix.replacement);
        
        if (content !== originalContent) {
          modified = true;
          report.fixesApplied += matches.length;
          report.fixes.push({
            file: fileRelPath,
            pattern: fix.description,
            count: matches.length,
            matches: matches.slice(0, 3) // Show first 3 matches
          });
        }
      }
    }
    
    if (modified && !CONFIG.dryRun) {
      await fs.writeFile(filePath, content, 'utf8');
      report.filesModified++;
    } else if (modified) {
      report.filesModified++;
    }
    
    return modified;
  } catch (err) {
    console.error(`Error processing ${filePath}: ${err.message}`);
    return false;
  }
}

async function main() {
  console.log('🔗 Fixing broken markdown links...\n');
  console.log(`Mode: ${CONFIG.dryRun ? 'DRY RUN (no changes)' : 'LIVE'}\n`);
  
  // Check if docs directory exists
  try {
    await fs.access(CONFIG.docsPath);
  } catch {
    console.error('Error: docs/ directory not found');
    console.error('Please run this script from your Docusaurus project root');
    process.exit(1);
  }
  
  // Find all markdown files
  console.log('Scanning for markdown files...');
  const mdFiles = await findMarkdownFiles(CONFIG.docsPath);
  report.filesScanned = mdFiles.length;
  console.log(`Found ${mdFiles.length} markdown files\n`);
  
  // Process each file
  console.log('Processing files...');
  for (const file of mdFiles) {
    const modified = await fixFile(file);
    if (modified) {
      const relPath = path.relative(CONFIG.docsPath, file);
      console.log(`  ✓ ${relPath}`);
    }
  }
  
  // Print report
  console.log('\n' + '='.repeat(70));
  console.log('SUMMARY');
  console.log('='.repeat(70));
  console.log(`Files scanned: ${report.filesScanned}`);
  console.log(`Files modified: ${report.filesModified}`);
  console.log(`Total fixes applied: ${report.fixesApplied}`);
  
  if (report.fixes.length > 0) {
    console.log('\nFixes by file:');
    report.fixes.forEach(fix => {
      console.log(`\n  ${fix.file}`);
      console.log(`    ${fix.pattern}: ${fix.count} occurrences`);
      fix.matches.forEach(m => console.log(`      - ${m}`));
    });
  }
  
  console.log('='.repeat(70) + '\n');
  
  if (CONFIG.dryRun) {
    console.log('💡 This was a dry run. Run without --dry-run to apply changes.\n');
  } else {
    console.log('✅ Fixes applied!\n');
    console.log('Next steps:');
    console.log('1. Run npm start to verify the warnings are fixed');
    console.log('2. Check git diff to review changes');
    console.log('3. Commit the changes\n');
  }
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
