#!/usr/bin/env node

/**
 * Enhanced Docusaurus Asset Migration Script
 * 
 * This script migrates ALL assets in two passes:
 * 1. REFERENCED assets: Found via markdown/HTML references
 * 2. ORPHANED assets: Found in img/bpmn directories but not referenced
 * 
 * CRITICAL: This moves files (not copies), so original directories become empty
 */

const fs = require('fs').promises;
const path = require('path');

// Configuration
const CONFIG = {
  docsPath: './docs',
  staticPath: './static/img',
  backupPath: './backup-assets',
  dryRun: false, // ALWAYS start with dry run!
  
  // All file extensions to migrate
  assetExtensions: [
    // Images
    '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp', '.ico',
    // BPMN & Process files
    '.bpmn', '.dmn', '.cmmn',
    // Documents (not markdown - those stay in docs/)
    '.pdf', '.odg', '.odt',
    // Scripts & Data
    '.js', '.json', '.xml', '.csv',
    // Note: .md and .mdx are intentionally excluded
  ],
  
  // Directories that commonly contain assets
  assetDirectoryNames: ['img', 'bpmn', 'images', 'assets'],
  
  // Sidebar sections for organization
  sidebarSections: {
    'get-started': ['docs/get-started'],
    'documentation': ['docs/documentation'],
    'security': ['docs/security']
  }
};

// Track all changes for reporting
const report = {
  filesScanned: 0,
  
  // Pass 1: Referenced assets
  referencedAssetsFound: 0,
  referencedAssetsMoved: 0,
  
  // Pass 2: Orphaned assets
  orphanedAssetsFound: 0,
  orphanedAssetsMoved: 0,
  
  filesUpdated: 0,
  errors: [],
  warnings: [],
  assetsByType: {},
  
  // Detailed lists
  referencedAssets: [],
  orphanedAssets: []
};

/**
 * Check if file is an asset we should migrate
 */
function isAssetFile(filename) {
  const ext = path.extname(filename).toLowerCase();
  return CONFIG.assetExtensions.includes(ext);
}

/**
 * Check if directory name suggests it contains assets
 */
function isAssetDirectory(dirname) {
  return CONFIG.assetDirectoryNames.includes(dirname.toLowerCase());
}

/**
 * Determine which sidebar section a file belongs to
 */
function getSidebarSection(filePath) {
  const normalizedPath = filePath.replace(/\\/g, '/');
  
  if (normalizedPath.includes('docs/get-started')) {
    return 'get-started';
  }
  if (normalizedPath.includes('docs/documentation')) {
    return 'documentation';
  }
  if (normalizedPath.includes('docs/security')) {
    return 'security';
  }
  
  return 'shared';
}

/**
 * Extract all asset references from markdown content
 */
function extractAssetReferences(content, filePath) {
  const assets = [];
  
  // Match markdown syntax: ![alt](path) or [text](path)
  const mdRegex = /!?\[([^\]]*)\]\(([^)]+)\)/g;
  let match;
  
  while ((match = mdRegex.exec(content)) !== null) {
    const isImage = match[0].startsWith('!');
    const assetPath = match[2];
    
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
        type: 'markdown'
      });
    }
  }
  
  // Match HTML img/a tags
  const htmlRegex = /<(?:img|a)[^>]+(?:src|href)=["']([^"']+)["'][^>]*>/g;
  
  while ((match = htmlRegex.exec(content)) !== null) {
    const assetPath = match[1];
    
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
        type: 'html'
      });
    }
  }
  
  // Match imports
  const importRegex = /import\s+(\w+)\s+from\s+['"]([^'"]+)['"];?/g;
  
  while ((match = importRegex.exec(content)) !== null) {
    const assetPath = match[2];
    
    if (isAssetFile(assetPath)) {
      assets.push({
        fullMatch: match[0],
        importName: match[1],
        path: assetPath,
        type: 'import'
      });
    }
  }
  
  return assets;
}

/**
 * Resolve asset path to absolute filesystem path
 */
function resolveAssetPath(assetPath, mdFilePath) {
  // Already absolute path from /img/
  if (assetPath.startsWith('/img/')) {
    return path.join(CONFIG.staticPath, assetPath.replace('/img/', ''));
  }
  
  // Relative path
  if (!path.isAbsolute(assetPath)) {
    const mdDir = path.dirname(mdFilePath);
    return path.resolve(mdDir, assetPath);
  }
  
  return assetPath;
}

/**
 * Generate new organized path for an asset
 */
function getNewAssetPath(oldPath, sidebarSection, mdFilePath) {
  const ext = path.extname(oldPath);
  const basename = path.basename(oldPath, ext);
  
  // Create subfolder structure based on doc's location within section
  const normalizedMdPath = mdFilePath.replace(/\\/g, '/');
  
  let subPath = '';
  if (sidebarSection !== 'shared') {
    const sectionPrefix = `docs/${sidebarSection}/`;
    const sectionIndex = normalizedMdPath.indexOf(sectionPrefix);
    
    if (sectionIndex !== -1) {
      const pathAfterSection = normalizedMdPath.substring(sectionIndex + sectionPrefix.length);
      const docParts = path.dirname(pathAfterSection).split('/').filter(p => p && p !== '.');
      subPath = docParts.join('/');
    }
  }
  
  // Build new path
  let newPath;
  if (subPath) {
    newPath = path.join(CONFIG.staticPath, sidebarSection, subPath, `${basename}${ext}`);
  } else {
    newPath = path.join(CONFIG.staticPath, sidebarSection, `${basename}${ext}`);
  }
  
  return newPath;
}

/**
 * Generate path for orphaned asset (no markdown reference)
 */
function getOrphanedAssetPath(oldPath) {
  const normalizedPath = oldPath.replace(/\\/g, '/');
  const sidebarSection = getSidebarSection(normalizedPath);
  
  // Extract the relative path from the section root
  let relativePath = '';
  
  if (normalizedPath.includes('docs/get-started')) {
    relativePath = normalizedPath.split('docs/get-started/')[1];
  } else if (normalizedPath.includes('docs/documentation')) {
    relativePath = normalizedPath.split('docs/documentation/')[1];
  } else if (normalizedPath.includes('docs/security')) {
    relativePath = normalizedPath.split('docs/security/')[1];
  } else {
    relativePath = path.basename(oldPath);
  }
  
  // Build new path maintaining directory structure
  return path.join(CONFIG.staticPath, sidebarSection, 'orphaned', relativePath);
}

/**
 * Convert absolute filesystem path to docusaurus /img/ reference
 */
function getDocusaurusPath(absolutePath) {
  const relativePath = path.relative(CONFIG.staticPath, absolutePath);
  return '/img/' + relativePath.replace(/\\/g, '/');
}

/**
 * Check if file exists
 */
async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

/**
 * Ensure directory exists
 */
async function ensureDir(dirPath) {
  try {
    await fs.mkdir(dirPath, { recursive: true });
  } catch (err) {
    if (err.code !== 'EEXIST') throw err;
  }
}

/**
 * Recursively find all markdown files
 */
async function findMarkdownFiles(dir) {
  const files = [];
  
  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      
      if (entry.isDirectory()) {
        if (entry.name.startsWith('_') || entry.name === 'node_modules') {
          continue;
        }
        files.push(...await findMarkdownFiles(fullPath));
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
    report.errors.push(`Error reading directory ${dir}: ${err.message}`);
  }
  
  return files;
}

/**
 * Recursively find all asset files in docs/
 */
async function findAllAssets(dir, foundAssets = new Set()) {
  const assets = [];
  
  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      
      if (entry.isDirectory()) {
        if (entry.name.startsWith('_') || entry.name === 'node_modules') {
          continue;
        }
        assets.push(...await findAllAssets(fullPath, foundAssets));
      } else if (entry.isFile() && isAssetFile(entry.name)) {
        // Normalize path for comparison (absolute path with forward slashes)
        const normalizedPath = path.resolve(fullPath).replace(/\\/g, '/');
        
        // Only add if not already found in pass 1
        if (!foundAssets.has(normalizedPath)) {
          assets.push(fullPath);
        }
      }
    }
  } catch (err) {
    report.errors.push(`Error scanning directory ${dir}: ${err.message}`);
  }
  
  return assets;
}

/**
 * Move file from source to destination (copy then delete source)
 */
async function moveFile(sourcePath, destPath) {
  try {
    await ensureDir(path.dirname(destPath));
    
    if (CONFIG.dryRun) {
      return await fileExists(sourcePath);
    }
    
    // Copy the file
    await fs.copyFile(sourcePath, destPath);
    
    // Delete the source file (this completes the "move")
    await fs.unlink(sourcePath);
    
    return true;
  } catch (err) {
    report.errors.push(`Failed to move ${sourcePath} to ${destPath}: ${err.message}`);
    return false;
  }
}

/**
 * PASS 1: Process referenced assets in markdown files
 */
async function processMarkdownFile(filePath, referencedAssets) {
  try {
    const content = await fs.readFile(filePath, 'utf8');
    const assets = extractAssetReferences(content, filePath);
    
    if (assets.length === 0) {
      return { updated: false };
    }
    
    report.referencedAssetsFound += assets.length;
    
    const sidebarSection = getSidebarSection(filePath);
    let updatedContent = content;
    const assetChanges = [];
    
    for (const asset of assets) {
      const oldAbsolutePath = resolveAssetPath(asset.path, filePath);
      
      // Track this asset as referenced (use absolute path with forward slashes)
      const normalizedPath = path.resolve(oldAbsolutePath).replace(/\\/g, '/');
      referencedAssets.add(normalizedPath);
      
      // Check if asset file exists
      if (!await fileExists(oldAbsolutePath)) {
        if (asset.path.includes('{{') || asset.path.includes('}}')) {
          continue;
        }
        report.warnings.push(`Asset not found: ${asset.path} (referenced in ${filePath})`);
        continue;
      }
      
      // Track asset types
      const ext = path.extname(oldAbsolutePath);
      report.assetsByType[ext] = (report.assetsByType[ext] || 0) + 1;
      
      // Generate new organized path
      const newAbsolutePath = getNewAssetPath(oldAbsolutePath, sidebarSection, filePath);
      
      // Skip if already in correct location
      if (oldAbsolutePath === newAbsolutePath) {
        continue;
      }
      
      // Move asset file
      const moved = await moveFile(oldAbsolutePath, newAbsolutePath);
      if (moved) {
        report.referencedAssetsMoved++;
        report.referencedAssets.push({
          old: oldAbsolutePath,
          new: newAbsolutePath,
          referencedBy: filePath
        });
      }
      
      // Update reference in content
      const newDocusaurusPath = getDocusaurusPath(newAbsolutePath);
      
      if (asset.type === 'markdown') {
        const newReference = asset.fullMatch.replace(asset.path, newDocusaurusPath);
        updatedContent = updatedContent.replace(asset.fullMatch, newReference);
      } else if (asset.type === 'html') {
        const newReference = asset.fullMatch.replace(asset.path, newDocusaurusPath);
        updatedContent = updatedContent.replace(asset.fullMatch, newReference);
      } else if (asset.type === 'import') {
        const relativeNewPath = path.relative(path.dirname(filePath), newAbsolutePath);
        const newImport = `import ${asset.importName} from '${relativeNewPath.replace(/\\/g, '/')}';`;
        updatedContent = updatedContent.replace(asset.fullMatch, newImport);
      }
      
      assetChanges.push({
        old: asset.path,
        new: newDocusaurusPath
      });
    }
    
    // Write updated content
    if (updatedContent !== content && !CONFIG.dryRun) {
      await fs.writeFile(filePath, updatedContent, 'utf8');
      report.filesUpdated++;
    }
    
    return {
      updated: updatedContent !== content,
      changes: assetChanges
    };
    
  } catch (err) {
    report.errors.push(`Error processing ${filePath}: ${err.message}`);
    return { updated: false };
  }
}

/**
 * PASS 2: Process orphaned assets (not referenced in any markdown)
 */
async function processOrphanedAssets(referencedAssets) {
  console.log('\n=== PASS 2: Scanning for orphaned assets ===\n');
  
  const allAssets = await findAllAssets(CONFIG.docsPath, referencedAssets);
  report.orphanedAssetsFound = allAssets.length;
  
  if (allAssets.length === 0) {
    console.log('✓ No orphaned assets found - all assets are referenced!');
    return;
  }
  
  console.log(`Found ${allAssets.length} orphaned assets (not referenced in markdown):`);
  
  for (const assetPath of allAssets) {
    const ext = path.extname(assetPath);
    const relativePath = path.relative(CONFIG.docsPath, assetPath);
    
    // Generate destination path
    const newPath = getOrphanedAssetPath(assetPath);
    
    // Move the file
    const moved = await moveFile(assetPath, newPath);
    if (moved) {
      report.orphanedAssetsMoved++;
      report.orphanedAssets.push({
        old: assetPath,
        new: newPath,
        type: ext
      });
      console.log(`  ${relativePath} → ${path.relative(CONFIG.staticPath, newPath)}`);
    }
  }
}

/**
 * Create backup
 */
async function createBackup() {
  if (CONFIG.dryRun) return;
  
  try {
    console.log('Creating backup...');
    await ensureDir(CONFIG.backupPath);
    
    if (await fileExists(CONFIG.staticPath)) {
      const cpCommand = require('child_process').execSync;
      cpCommand(`cp -r "${CONFIG.staticPath}" "${CONFIG.backupPath}/"`);
      console.log(`✓ Backup created at ${CONFIG.backupPath}`);
    }
  } catch (err) {
    console.error('Warning: Could not create backup:', err.message);
  }
}

/**
 * Print final report
 */
function printReport() {
  console.log('\n' + '='.repeat(70));
  console.log('MIGRATION REPORT');
  console.log('='.repeat(70));
  console.log(`Mode: ${CONFIG.dryRun ? 'DRY RUN (no changes made)' : 'LIVE'}`);
  console.log(`\nMarkdown files scanned: ${report.filesScanned}`);
  
  console.log('\n--- PASS 1: Referenced Assets ---');
  console.log(`Assets found in markdown: ${report.referencedAssetsFound}`);
  console.log(`Assets moved: ${report.referencedAssetsMoved}`);
  
  console.log('\n--- PASS 2: Orphaned Assets ---');
  console.log(`Orphaned assets found: ${report.orphanedAssetsFound}`);
  console.log(`Orphaned assets moved: ${report.orphanedAssetsMoved}`);
  
  console.log('\n--- TOTALS ---');
  const totalFound = report.referencedAssetsFound + report.orphanedAssetsFound;
  const totalMoved = report.referencedAssetsMoved + report.orphanedAssetsMoved;
  console.log(`Total assets found: ${totalFound}`);
  console.log(`Total assets moved: ${totalMoved}`);
  console.log(`Markdown files updated: ${report.filesUpdated}`);
  
  if (Object.keys(report.assetsByType).length > 0) {
    console.log('\nAssets by type:');
    Object.entries(report.assetsByType)
      .sort((a, b) => b[1] - a[1])
      .forEach(([type, count]) => {
        console.log(`  ${type}: ${count}`);
      });
  }
  
  if (report.orphanedAssets.length > 0) {
    console.log(`\n⚠️  Orphaned Assets (${report.orphanedAssets.length}):`);
    console.log('These assets were not referenced in any markdown file.');
    console.log('They have been moved to static/img/*/orphaned/ directories.');
    console.log('\nRecommendations:');
    console.log('1. Review the orphaned assets list below');
    console.log('2. Determine if they are still needed');
    console.log('3. Either reference them in docs or delete them');
    console.log('4. Consider creating a cleanup task\n');
    
    // Group by type
    const byType = {};
    report.orphanedAssets.forEach(asset => {
      if (!byType[asset.type]) byType[asset.type] = [];
      byType[asset.type].push(asset);
    });
    
    Object.entries(byType).forEach(([type, assets]) => {
      console.log(`\n  ${type} files (${assets.length}):`);
      assets.slice(0, 5).forEach(a => {
        console.log(`    - ${path.relative(CONFIG.docsPath, a.old)}`);
      });
      if (assets.length > 5) {
        console.log(`    ... and ${assets.length - 5} more`);
      }
    });
  }
  
  if (report.warnings.length > 0) {
    console.log(`\n⚠️  Warnings: ${report.warnings.length}`);
    report.warnings.slice(0, 5).forEach(w => console.log(`  - ${w}`));
    if (report.warnings.length > 5) {
      console.log(`  ... and ${report.warnings.length - 5} more`);
    }
  }
  
  if (report.errors.length > 0) {
    console.log(`\n❌ Errors: ${report.errors.length}`);
    report.errors.forEach(e => console.log(`  - ${e}`));
  }
  
  console.log('='.repeat(70) + '\n');
}

/**
 * Clean up empty directories
 */
async function cleanupEmptyDirs(dir) {
  if (CONFIG.dryRun) return;
  
  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      if (entry.isDirectory()) {
        const fullPath = path.join(dir, entry.name);
        await cleanupEmptyDirs(fullPath);
      }
    }
    
    const remainingEntries = await fs.readdir(dir);
    if (remainingEntries.length === 0) {
      await fs.rmdir(dir);
      console.log(`✓ Removed empty directory: ${dir}`);
    }
  } catch (err) {
    // Ignore errors in cleanup
  }
}

/**
 * Main execution
 */
async function main() {
  console.log('🚀 Starting Enhanced Docusaurus Asset Migration...\n');
  console.log('This migration runs in TWO passes:');
  console.log('  PASS 1: Migrate assets referenced in markdown files');
  console.log('  PASS 2: Migrate orphaned assets (not referenced anywhere)\n');
  
  // Validate paths exist
  try {
    await fs.access(CONFIG.docsPath);
  } catch (err) {
    console.error('Error: Could not find docs directory');
    console.error('Please run this script from your Docusaurus project root');
    process.exit(1);
  }
  
  // Create backup
  if (!CONFIG.dryRun) {
    await createBackup();
  }
  
  // Track which assets are referenced
  const referencedAssets = new Set();
  
  // PASS 1: Process markdown files and referenced assets
  console.log('=== PASS 1: Processing markdown files ===\n');
  console.log('Scanning for markdown files...');
  const mdFiles = await findMarkdownFiles(CONFIG.docsPath);
  console.log(`Found ${mdFiles.length} markdown files\n`);
  
  report.filesScanned = mdFiles.length;
  
  console.log('Processing files...');
  for (const file of mdFiles) {
    const result = await processMarkdownFile(file, referencedAssets);
    if (result.updated) {
      console.log(`✓ Updated: ${path.relative(CONFIG.docsPath, file)}`);
      if (result.changes.length > 0 && result.changes.length <= 3) {
        result.changes.forEach(c => {
          console.log(`    ${c.old} → ${c.new}`);
        });
      } else if (result.changes.length > 3) {
        console.log(`    (${result.changes.length} assets updated)`);
      }
    }
  }
  
  // PASS 2: Find and process orphaned assets
  console.log(`\nPass 1 tracked ${referencedAssets.size} unique asset paths as referenced`);
  await processOrphanedAssets(referencedAssets);
  
  // Clean up empty directories
  if (!CONFIG.dryRun) {
    console.log('\nCleaning up empty directories...');
    await cleanupEmptyDirs(CONFIG.docsPath);
  }
  
  // Print final report
  printReport();
  
  if (CONFIG.dryRun) {
    console.log('💡 This was a dry run. To apply changes, set dryRun: false in the script.\n');
    console.log('Recommended next steps:');
    console.log('1. Review the orphaned assets list above');
    console.log('2. Decide which orphaned assets to keep vs. delete');
    console.log('3. Set dryRun: false and run the migration');
    console.log('4. Test your documentation (npm start)');
    console.log('5. Verify all assets display correctly\n');
  } else {
    console.log('✅ Migration complete!\n');
    console.log('Next steps:');
    console.log('1. Test your documentation locally (npm start)');
    console.log('2. Verify all assets display correctly');
    console.log('3. Review orphaned assets in static/img/*/orphaned/');
    console.log('4. Clean up orphaned assets if not needed');
    console.log(`5. Backup is available at ${CONFIG.backupPath}\n`);
  }
}

// Run the script
main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
