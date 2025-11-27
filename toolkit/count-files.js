#!/usr/bin/env node

/**
 * File Counter Script (Files Only)
 * 
 * Counts actual files by extension in specified directories
 * Generates before/after comparison for migration verification
 */

const fs = require('fs').promises;
const path = require('path');

const CONFIG = {
  searchPaths: {
    docs: './docs',
    static: './static/img'
  },
  outputFile: './toolkit/file-count.md',
  // File extensions to track
  extensions: [
    '.bpmn', '.dmn', '.cmmn',
    '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp', '.ico',
    '.pdf', '.odg', '.odt',
    '.js', '.json', '.xml', '.csv',
    '.md', '.mdx'
  ]
};

/**
 * Recursively count files with given extension in directory
 */
async function countFilesInDirectory(dir, ext) {
  let count = 0;
  const fileList = [];
  
  async function search(currentDir) {
    try {
      const entries = await fs.readdir(currentDir, { withFileTypes: true });
      
      for (const entry of entries) {
        const fullPath = path.join(currentDir, entry.name);
        
        if (entry.isDirectory()) {
          // Skip node_modules and hidden directories
          if (entry.name === 'node_modules' || entry.name.startsWith('.')) {
            continue;
          }
          await search(fullPath);
        } else if (entry.isFile() && entry.name.endsWith(ext)) {
          count++;
          fileList.push(fullPath);
        }
      }
    } catch (err) {
      // Ignore directory read errors
    }
  }
  
  try {
    await fs.access(dir);
    await search(dir);
  } catch (err) {
    // Directory doesn't exist
  }
  
  return { count, fileList };
}

/**
 * Generate markdown table
 */
function generateMarkdownTable(docsData, staticData, timestamp) {
  let markdown = `# File Count Report\n\n`;
  markdown += `**Generated:** ${timestamp}\n\n`;
  
  markdown += `## Summary\n\n`;
  markdown += `| File Type | docs/ | static/img/ | Total |\n`;
  markdown += `|-----------|-------|-------------|-------|\n`;
  
  // Collect all extensions that have files
  const allExtensions = new Set([
    ...Object.keys(docsData),
    ...Object.keys(staticData)
  ]);
  
  const sortedExtensions = Array.from(allExtensions).sort((a, b) => {
    const aTotal = (docsData[a]?.count || 0) + (staticData[a]?.count || 0);
    const bTotal = (docsData[b]?.count || 0) + (staticData[b]?.count || 0);
    return bTotal - aTotal;
  });
  
  let totalDocs = 0;
  let totalStatic = 0;
  
  for (const ext of sortedExtensions) {
    const docsCount = docsData[ext]?.count || 0;
    const staticCount = staticData[ext]?.count || 0;
    const total = docsCount + staticCount;
    
    totalDocs += docsCount;
    totalStatic += staticCount;
    
    if (total > 0) {
      markdown += `| ${ext} | ${docsCount} | ${staticCount} | ${total} |\n`;
    }
  }
  
  markdown += `| **TOTAL** | **${totalDocs}** | **${totalStatic}** | **${totalDocs + totalStatic}** |\n`;
  
  markdown += `\n## Details\n\n`;
  
  for (const ext of sortedExtensions) {
    const docsFiles = docsData[ext]?.fileList || [];
    const staticFiles = staticData[ext]?.fileList || [];
    
    if (docsFiles.length > 0 || staticFiles.length > 0) {
      markdown += `### ${ext}\n\n`;
      
      if (docsFiles.length > 0) {
        markdown += `**In docs/ (${docsFiles.length} files):**\n\n`;
        
        if (docsFiles.length <= 20) {
          docsFiles.forEach(f => markdown += `- ${f}\n`);
        } else {
          docsFiles.slice(0, 10).forEach(f => markdown += `- ${f}\n`);
          markdown += `- ... (${docsFiles.length - 20} more files)\n`;
          docsFiles.slice(-10).forEach(f => markdown += `- ${f}\n`);
        }
        markdown += `\n`;
      }
      
      if (staticFiles.length > 0) {
        markdown += `**In static/img/ (${staticFiles.length} files):**\n\n`;
        
        if (staticFiles.length <= 20) {
          staticFiles.forEach(f => markdown += `- ${f}\n`);
        } else {
          staticFiles.slice(0, 10).forEach(f => markdown += `- ${f}\n`);
          markdown += `- ... (${staticFiles.length - 20} more files)\n`;
          staticFiles.slice(-10).forEach(f => markdown += `- ${f}\n`);
        }
        markdown += `\n`;
      }
    }
  }
  
  return markdown;
}

/**
 * Main execution
 */
async function main() {
  console.log('📊 Counting files in codebase...\n');
  
  const timestamp = new Date().toISOString().replace('T', ' ').substring(0, 19);
  
  const docsData = {};
  const staticData = {};
  
  console.log('Searching in docs/...');
  for (const ext of CONFIG.extensions) {
    process.stdout.write(`  ${ext}... `);
    const result = await countFilesInDirectory(CONFIG.searchPaths.docs, ext);
    docsData[ext] = result;
    console.log(`${result.count} files`);
  }
  
  console.log('\nSearching in static/img/...');
  for (const ext of CONFIG.extensions) {
    process.stdout.write(`  ${ext}... `);
    const result = await countFilesInDirectory(CONFIG.searchPaths.static, ext);
    staticData[ext] = result;
    console.log(`${result.count} files`);
  }
  
  // Generate markdown
  const markdown = generateMarkdownTable(docsData, staticData, timestamp);
  
  // Ensure output directory exists
  const outputDir = path.dirname(CONFIG.outputFile);
  try {
    await fs.mkdir(outputDir, { recursive: true });
  } catch (err) {
    // Directory might already exist
  }
  
  // Write to file
  await fs.writeFile(CONFIG.outputFile, markdown, 'utf8');
  
  console.log('\n✅ Report generated!');
  console.log(`📄 Saved to: ${CONFIG.outputFile}\n`);
  
  // Print summary to console
  console.log('='.repeat(70));
  console.log('SUMMARY');
  console.log('='.repeat(70));
  console.log('\nFile Type          docs/    static/img/    Total');
  console.log('-'.repeat(55));
  
  // Calculate totals
  let totalDocs = 0;
  let totalStatic = 0;
  
  const allExtensions = new Set([
    ...Object.keys(docsData),
    ...Object.keys(staticData)
  ]);
  
  const sortedExtensions = Array.from(allExtensions).sort((a, b) => {
    const aTotal = (docsData[a]?.count || 0) + (staticData[a]?.count || 0);
    const bTotal = (docsData[b]?.count || 0) + (staticData[b]?.count || 0);
    return bTotal - aTotal;
  });
  
  sortedExtensions.forEach(ext => {
    const docsCount = docsData[ext]?.count || 0;
    const staticCount = staticData[ext]?.count || 0;
    const total = docsCount + staticCount;
    
    totalDocs += docsCount;
    totalStatic += staticCount;
    
    if (total > 0) {
      const extStr = ext.padEnd(15);
      const docsStr = docsCount.toString().padStart(8);
      const staticStr = staticCount.toString().padStart(13);
      const totalStr = total.toString().padStart(9);
      console.log(`${extStr} ${docsStr} ${staticStr} ${totalStr}`);
    }
  });
  
  console.log('-'.repeat(55));
  const docsStr = totalDocs.toString().padStart(8);
  const staticStr = totalStatic.toString().padStart(13);
  const totalStr = (totalDocs + totalStatic).toString().padStart(9);
  console.log(`${'TOTAL'.padEnd(15)} ${docsStr} ${staticStr} ${totalStr}`);
  
  console.log('='.repeat(70) + '\n');
  
  // Migration status check
  const assetExtensions = ['.bpmn', '.dmn', '.png', '.svg', '.jpg', '.jpeg', '.gif', '.odg', '.js'];
  const assetsInDocs = assetExtensions.reduce((sum, ext) => sum + (docsData[ext]?.count || 0), 0);
  const assetsInStatic = assetExtensions.reduce((sum, ext) => sum + (staticData[ext]?.count || 0), 0);
  
  if (assetsInDocs > 0 && assetsInStatic === 0) {
    console.log('📋 Status: BEFORE migration');
    console.log(`   ${assetsInDocs} asset files in docs/ (ready to migrate)\n`);
  } else if (assetsInDocs === 0 && assetsInStatic > 0) {
    console.log('✅ Status: AFTER migration');
    console.log(`   ${assetsInStatic} asset files in static/img/ (migration complete)\n`);
  } else if (assetsInDocs > 0 && assetsInStatic > 0) {
    console.log('⚠️  Status: PARTIAL migration');
    console.log(`   ${assetsInDocs} assets still in docs/`);
    console.log(`   ${assetsInStatic} assets in static/img/\n`);
  } else {
    console.log('ℹ️  Status: No asset files found\n');
  }
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
