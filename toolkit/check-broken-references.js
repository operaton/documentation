#!/usr/bin/env node

/**
 * Broken Asset Reference Checker
 * 
 * Scans all markdown files and reports asset references that don't exist
 */

const fs = require('fs').promises;
const path = require('path');

const CONFIG = {
  docsPath: './docs',
  staticPath: './static/img',
  assetExtensions: [
    '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp', '.ico',
    '.bpmn', '.dmn', '.cmmn',
    '.pdf', '.odg', '.odt',
    '.js', '.json', '.xml', '.csv',
  ]
};

const report = {
  mdFilesScanned: 0,
  totalReferences: 0,
  brokenReferences: [],
  workingReferences: 0,
  externalReferences: 0
};

function isAssetFile(filename) {
  const ext = path.extname(filename).toLowerCase();
  return CONFIG.assetExtensions.includes(ext);
}

async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

/**
 * Extract asset references from markdown content
 */
function extractAssetReferences(content, filePath) {
  const assets = [];
  
  // Match markdown syntax: ![alt](path) or [text](path)
  const mdRegex = /!?\[([^\]]*)\]\(([^)]+)\)/g;
  let match;
  
  while ((match = mdRegex.exec(content)) !== null) {
    const isImage = match[0].startsWith('!');
    const assetPath = match[2];
    const lineNumber = content.substring(0, match.index).split('\n').length;
    
    // Skip external URLs
    if (assetPath.startsWith('http://') || assetPath.startsWith('https://')) {
      continue;
    }
    
    // Skip anchors and empty paths
    if (assetPath.startsWith('#') || !assetPath.trim()) {
      continue;
    }
    
    // Only process if it's an image tag OR has an asset extension
    const hasAssetExtension = CONFIG.assetExtensions.some(ext => 
      assetPath.toLowerCase().includes(ext)
    );
    
    if (isImage || hasAssetExtension) {
      assets.push({
        fullMatch: match[0],
        alt: match[1],
        path: assetPath,
        type: isImage ? 'image' : 'link',
        lineNumber: lineNumber
      });
    }
  }
  
  // Match HTML img/a tags
  const htmlRegex = /<(?:img|a)[^>]+(?:src|href)=["']([^"']+)["'][^>]*>/g;
  
  while ((match = htmlRegex.exec(content)) !== null) {
    const assetPath = match[1];
    const lineNumber = content.substring(0, match.index).split('\n').length;
    
    if (assetPath.startsWith('http://') || assetPath.startsWith('https://')) {
      continue;
    }
    
    const hasAssetExtension = CONFIG.assetExtensions.some(ext => 
      assetPath.toLowerCase().includes(ext)
    );
    
    if (hasAssetExtension) {
      assets.push({
        fullMatch: match[0],
        path: assetPath,
        type: 'html',
        lineNumber: lineNumber
      });
    }
  }
  
  return assets;
}

/**
 * Resolve asset path to check if it exists
 */
async function checkAssetExists(assetPath, mdFilePath) {
  // Absolute path from /img/
  if (assetPath.startsWith('/img/')) {
    const fullPath = path.join(CONFIG.staticPath, assetPath.replace('/img/', ''));
    return {
      exists: await fileExists(fullPath),
      resolvedPath: fullPath
    };
  }
  
  // Relative path - resolve relative to markdown file's directory
  if (!path.isAbsolute(assetPath)) {
    const mdDir = path.dirname(mdFilePath);
    const fullPath = path.resolve(mdDir, assetPath);
    return {
      exists: await fileExists(fullPath),
      resolvedPath: fullPath
    };
  }
  
  return {
    exists: await fileExists(assetPath),
    resolvedPath: assetPath
  };
}

/**
 * Find all markdown files
 */
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
        } else if (entry.isFile()) {
          if (entry.name.startsWith('_')) {
            continue;
          }
          if (entry.name.match(/\.(md|mdx)$/)) {
            files.push(fullPath);
          }
        }
      }
    } catch (err) {
      // Ignore errors
    }
  }
  
  await search(dir);
  return files;
}

/**
 * Check a single markdown file for broken references
 */
async function checkMarkdownFile(filePath) {
  try {
    const content = await fs.readFile(filePath, 'utf8');
    const assets = extractAssetReferences(content, filePath);
    
    report.totalReferences += assets.length;
    
    for (const asset of assets) {
      // Skip template code
      if (asset.path.includes('{{') || asset.path.includes('}}')) {
        continue;
      }
      
      const check = await checkAssetExists(asset.path, filePath);
      
      if (!check.exists) {
        report.brokenReferences.push({
          mdFile: filePath,
          assetPath: asset.path,
          resolvedPath: check.resolvedPath,
          lineNumber: asset.lineNumber,
          type: asset.type,
          fullMatch: asset.fullMatch
        });
      } else {
        report.workingReferences++;
      }
    }
  } catch (err) {
    console.error(`Error checking ${filePath}: ${err.message}`);
  }
}

/**
 * Generate markdown report
 */
function generateMarkdownReport() {
  let md = '# Broken Asset References Report\n\n';
  md += `**Generated:** ${new Date().toISOString().replace('T', ' ').substring(0, 19)}\n\n`;
  
  md += '## Summary\n\n';
  md += `- Markdown files scanned: ${report.mdFilesScanned}\n`;
  md += `- Total asset references: ${report.totalReferences}\n`;
  md += `- Working references: ${report.workingReferences}\n`;
  md += `- **Broken references: ${report.brokenReferences.length}**\n\n`;
  
  if (report.brokenReferences.length === 0) {
    md += '✅ **No broken references found!**\n';
    return md;
  }
  
  md += '## Broken References by File\n\n';
  
  // Group by markdown file
  const byFile = {};
  report.brokenReferences.forEach(ref => {
    if (!byFile[ref.mdFile]) {
      byFile[ref.mdFile] = [];
    }
    byFile[ref.mdFile].push(ref);
  });
  
  Object.keys(byFile).sort().forEach(mdFile => {
    const refs = byFile[mdFile];
    const relativePath = path.relative(CONFIG.docsPath, mdFile);
    
    md += `### ${relativePath}\n\n`;
    md += `**${refs.length} broken reference${refs.length > 1 ? 's' : ''}:**\n\n`;
    
    refs.forEach(ref => {
      md += `- **Line ${ref.lineNumber}:** \`${ref.assetPath}\`\n`;
      md += `  - Type: ${ref.type}\n`;
      md += `  - Tried to resolve to: \`${ref.resolvedPath}\`\n`;
      md += `  - Full reference: \`${ref.fullMatch.substring(0, 80)}${ref.fullMatch.length > 80 ? '...' : ''}\`\n\n`;
    });
  });
  
  md += '## Quick Fix Guide\n\n';
  md += 'For each broken reference, you can:\n\n';
  md += '1. **Find the missing asset:** Search for it in your project or recreate it\n';
  md += '2. **Fix the path:** Update the markdown to point to the correct location\n';
  md += '3. **Remove the reference:** If the asset is no longer needed\n\n';
  
  // Group by missing file
  md += '## Missing Assets List\n\n';
  const missingAssets = {};
  report.brokenReferences.forEach(ref => {
    const basename = path.basename(ref.assetPath);
    if (!missingAssets[basename]) {
      missingAssets[basename] = [];
    }
    missingAssets[basename].push(ref.mdFile);
  });
  
  Object.keys(missingAssets).sort().forEach(asset => {
    const files = missingAssets[asset];
    md += `- **${asset}** - Referenced in ${files.length} file${files.length > 1 ? 's' : ''}\n`;
    files.forEach(file => {
      md += `  - ${path.relative(CONFIG.docsPath, file)}\n`;
    });
  });
  
  return md;
}

/**
 * Main execution
 */
async function main() {
  console.log('🔍 Scanning for broken asset references...\n');
  
  // Find all markdown files
  console.log('Finding markdown files...');
  const mdFiles = await findMarkdownFiles(CONFIG.docsPath);
  report.mdFilesScanned = mdFiles.length;
  console.log(`Found ${mdFiles.length} markdown files\n`);
  
  // Check each file
  console.log('Checking asset references...');
  for (const file of mdFiles) {
    await checkMarkdownFile(file);
    process.stdout.write('.');
  }
  console.log('\n');
  
  // Generate report
  const markdownReport = generateMarkdownReport();
  const outputFile = './broken-asset-references.md';
  await fs.writeFile(outputFile, markdownReport, 'utf8');
  
  // Print summary to console
  console.log('='.repeat(70));
  console.log('SUMMARY');
  console.log('='.repeat(70));
  console.log(`Markdown files scanned: ${report.mdFilesScanned}`);
  console.log(`Total asset references: ${report.totalReferences}`);
  console.log(`Working references: ${report.workingReferences}`);
  console.log(`Broken references: ${report.brokenReferences.length}`);
  console.log('='.repeat(70) + '\n');
  
  if (report.brokenReferences.length > 0) {
    console.log('⚠️  Found broken asset references!\n');
    console.log('Most common missing assets:');
    
    // Show top 10 missing assets
    const missingAssets = {};
    report.brokenReferences.forEach(ref => {
      const basename = path.basename(ref.assetPath);
      missingAssets[basename] = (missingAssets[basename] || 0) + 1;
    });
    
    Object.entries(missingAssets)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .forEach(([asset, count]) => {
        console.log(`  ${asset}: ${count} reference${count > 1 ? 's' : ''}`);
      });
    
    console.log(`\n📄 Full report saved to: ${outputFile}\n`);
  } else {
    console.log('✅ No broken references found!\n');
  }
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
