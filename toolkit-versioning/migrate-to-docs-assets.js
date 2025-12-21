#!/usr/bin/env node

/**
 * Reverse Asset Migration: static/img → docs/assets
 * 
 * Moves assets from static/img/ to docs/assets/ for Docusaurus versioning support
 * Updates all markdown references to use relative paths
 */

const fs = require('fs').promises;
const path = require('path');

const CONFIG = {
  staticPath: './static/img',
  docsAssetsPath: './docs/assets',
  docsPath: './docs',
  dryRun: false, // ALWAYS start with dry run!
  
  // Asset extensions to migrate
  assetExtensions: [
    '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp', '.ico',
    '.pdf', '.odg', '.odt',
    '.xml', '.csv',
  ],
  
  // Directories to migrate (exclude Docusaurus originals)
  includeDirs: ['documentation', 'get-started', 'security'],
};

const report = {
  filesScanned: 0,
  assetsMoved: 0,
  filesUpdated: 0,
  errors: [],
  warnings: []
};

/**
 * Check if file is an asset we should migrate
 */
function isAssetFile(filename) {
  const ext = path.extname(filename).toLowerCase();
  return CONFIG.assetExtensions.includes(ext);
}

/**
 * Check if directory should be migrated
 */
function shouldMigrateDir(dirPath) {
  const normalizedPath = dirPath.replace(/\\/g, '/');
  return CONFIG.includeDirs.some(dir => normalizedPath.includes(`/${dir}/`) || normalizedPath.endsWith(`/${dir}`));
}

/**
 * Find all assets in static/img that should be migrated
 */
async function findAssetsToMigrate(dir, assets = []) {
  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      
      if (entry.isDirectory()) {
        if (shouldMigrateDir(fullPath)) {
          await findAssetsToMigrate(fullPath, assets);
        }
      } else if (entry.isFile() && isAssetFile(entry.name)) {
        assets.push(fullPath);
      }
    }
  } catch (err) {
    report.errors.push(`Error scanning ${dir}: ${err.message}`);
  }
  
  return assets;
}

/**
 * Get new path in docs/assets maintaining structure
 */
function getNewAssetPath(oldPath) {
  // static/img/documentation/intro/test.png -> docs/assets/documentation/intro/test.png
  const relativePath = path.relative(CONFIG.staticPath, oldPath);
  return path.join(CONFIG.docsAssetsPath, relativePath);
}

/**
 * Move asset file
 */
async function moveAsset(sourcePath, destPath) {
  try {
    const destDir = path.dirname(destPath);
    
    if (!CONFIG.dryRun) {
      await fs.mkdir(destDir, { recursive: true });
      await fs.copyFile(sourcePath, destPath);
      await fs.unlink(sourcePath);
    }
    
    return true;
  } catch (err) {
    report.errors.push(`Failed to move ${sourcePath}: ${err.message}`);
    return false;
  }
}

/**
 * Extract asset references from markdown
 */
function extractAssetReferences(content) {
  const assets = [];
  
  // Match absolute paths starting with /img/
  const absoluteRegex = /(!?\[[^\]]*\]\()(\/img\/[^)]+)(\))/g;
  let match;
  
  while ((match = absoluteRegex.exec(content)) !== null) {
    assets.push({
      fullMatch: match[0],
      prefix: match[1],
      path: match[2],
      suffix: match[3],
      type: 'absolute'
    });
  }
  
  return assets;
}

/**
 * Calculate relative path from markdown file to asset
 */
function getRelativePath(mdFilePath, assetPath) {
  // mdFilePath: docs/documentation/intro/index.md
  // assetPath: docs/assets/documentation/intro/test.png
  
  const mdDir = path.dirname(mdFilePath);
  const relativePath = path.relative(mdDir, assetPath);
  
  // Ensure forward slashes for cross-platform compatibility
  return relativePath.replace(/\\/g, '/');
}

/**
 * Find all markdown files
 */
async function findMarkdownFiles(dir, files = []) {
  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      
      if (entry.isDirectory()) {
        if (!entry.name.startsWith('_') && entry.name !== 'node_modules') {
          await findMarkdownFiles(fullPath, files);
        }
      } else if (entry.isFile() && !entry.name.startsWith('_')) {
        if (entry.name.match(/\.(md|mdx)$/)) {
          files.push(fullPath);
        }
      }
    }
  } catch (err) {
    report.errors.push(`Error reading ${dir}: ${err.message}`);
  }
  
  return files;
}

/**
 * Update markdown file references
 */
async function updateMarkdownFile(filePath) {
  try {
    const content = await fs.readFile(filePath, 'utf8');
    const assets = extractAssetReferences(content);
    
    if (assets.length === 0) {
      return { updated: false };
    }
    
    let updatedContent = content;
    const changes = [];
    
    for (const asset of assets) {
      // Convert /img/documentation/... to docs/assets/documentation/...
      const oldAbsolutePath = asset.path.replace(/^\/img\//, '');
      const newAssetPath = path.join(CONFIG.docsAssetsPath, oldAbsolutePath);
      
      // Calculate relative path from markdown to new asset location
      const relativePath = getRelativePath(filePath, newAssetPath);
      
      // Replace absolute path with relative
      const newReference = asset.prefix + relativePath + asset.suffix;
      updatedContent = updatedContent.replace(asset.fullMatch, newReference);
      
      changes.push({
        old: asset.path,
        new: relativePath
      });
    }
    
    if (updatedContent !== content && !CONFIG.dryRun) {
      await fs.writeFile(filePath, updatedContent, 'utf8');
      report.filesUpdated++;
    }
    
    return {
      updated: updatedContent !== content,
      changes
    };
    
  } catch (err) {
    report.errors.push(`Error processing ${filePath}: ${err.message}`);
    return { updated: false };
  }
}

/**
 * Main execution
 */
async function main() {
  console.log('🔄 Reverse Asset Migration: static/img → docs/assets\n');
  console.log('This migration enables Docusaurus versioning support\n');
  
  // Find all assets to migrate
  console.log('=== Finding assets in static/img ===\n');
  const assetsToMigrate = await findAssetsToMigrate(CONFIG.staticPath);
  console.log(`Found ${assetsToMigrate.length} assets to migrate\n`);
  
  // Move assets
  console.log('=== Moving assets to docs/assets ===\n');
  for (const assetPath of assetsToMigrate) {
    const newPath = getNewAssetPath(assetPath);
    const relativePath = path.relative(CONFIG.staticPath, assetPath);
    
    if (await moveAsset(assetPath, newPath)) {
      report.assetsMoved++;
      console.log(`✓ ${relativePath}`);
    }
  }
  
  // Find and update markdown files
  console.log('\n=== Updating markdown references ===\n');
  const mdFiles = await findMarkdownFiles(CONFIG.docsPath);
  report.filesScanned = mdFiles.length;
  
  for (const file of mdFiles) {
    const result = await updateMarkdownFile(file);
    if (result.updated) {
      console.log(`✓ ${path.relative(CONFIG.docsPath, file)} (${result.changes.length} refs)`);
    }
  }
  
  // Print report
  console.log('\n' + '='.repeat(70));
  console.log('MIGRATION REPORT');
  console.log('='.repeat(70));
  console.log(`Mode: ${CONFIG.dryRun ? 'DRY RUN' : 'LIVE'}`);
  console.log(`\nAssets moved: ${report.assetsMoved}`);
  console.log(`Markdown files updated: ${report.filesUpdated}`);
  console.log(`Total markdown files scanned: ${report.filesScanned}`);
  
  if (report.warnings.length > 0) {
    console.log(`\n⚠️  Warnings: ${report.warnings.length}`);
    report.warnings.forEach(w => console.log(`  - ${w}`));
  }
  
  if (report.errors.length > 0) {
    console.log(`\n❌ Errors: ${report.errors.length}`);
    report.errors.forEach(e => console.log(`  - ${e}`));
  }
  
  console.log('='.repeat(70) + '\n');
  
  if (CONFIG.dryRun) {
    console.log('💡 This was a dry run. Set dryRun: false to apply changes.\n');
  } else {
    console.log('✅ Migration complete!\n');
    console.log('Next steps:');
    console.log('1. Test documentation (npm start)');
    console.log('2. Verify all images display');
    console.log('3. Test versioning: npm run docusaurus docs:version 1.0.0');
    console.log('4. Verify versioned docs include images\n');
  }
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});