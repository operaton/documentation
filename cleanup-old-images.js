#!/usr/bin/env node

/**
 * Cleanup Old Images Script
 * 
 * After successful migration, this script removes old image folders
 * from the docs directory since images are now in static/img/
 * 
 * IMPORTANT: Only run this after verifying the migration worked!
 */

const fs = require('fs').promises;
const path = require('path');

const CONFIG = {
  docsPath: './docs',
  dryRun: true, // Set to false to actually delete
  dirsToRemove: [], // Will be populated during scan
};

const stats = {
  dirsFound: 0,
  dirsDeleted: 0,
  filesFound: 0,
  errors: []
};

/**
 * Recursively find all 'img' and 'bpmn' directories in docs
 */
async function findImageDirs(dir, imageDirs = []) {
  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      
      if (entry.isDirectory()) {
        // Skip node_modules and hidden directories
        if (entry.name === 'node_modules' || entry.name.startsWith('.')) {
          continue;
        }
        
        // Check if this is an image directory
        if (entry.name === 'img' || entry.name === 'bpmn') {
          imageDirs.push(fullPath);
          stats.dirsFound++;
          
          // Count files in this directory
          const files = await countFiles(fullPath);
          stats.filesFound += files;
        } else {
          // Recurse into other directories
          await findImageDirs(fullPath, imageDirs);
        }
      }
    }
  } catch (err) {
    stats.errors.push(`Error reading directory ${dir}: ${err.message}`);
  }
  
  return imageDirs;
}

/**
 * Count files in a directory recursively
 */
async function countFiles(dir) {
  let count = 0;
  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      
      if (entry.isFile()) {
        count++;
      } else if (entry.isDirectory()) {
        count += await countFiles(fullPath);
      }
    }
  } catch (err) {
    // Ignore errors
  }
  
  return count;
}

/**
 * Delete a directory and all its contents
 */
async function deleteDirectory(dir) {
  try {
    await fs.rm(dir, { recursive: true, force: true });
    stats.dirsDeleted++;
    return true;
  } catch (err) {
    stats.errors.push(`Failed to delete ${dir}: ${err.message}`);
    return false;
  }
}

/**
 * Main execution
 */
async function main() {
  console.log('🧹 Old Image Cleanup Script\n');
  console.log('='.repeat(60));
  console.log(`Mode: ${CONFIG.dryRun ? 'DRY RUN (no changes)' : 'LIVE (will delete)'}`);
  console.log('='.repeat(60) + '\n');
  
  // Verify docs path exists
  try {
    await fs.access(CONFIG.docsPath);
  } catch (err) {
    console.error('Error: Could not find docs directory');
    console.error('Please run this script from your Docusaurus project root');
    process.exit(1);
  }
  
  // Find all image directories
  console.log('Scanning for old image directories...\n');
  const imageDirs = await findImageDirs(CONFIG.docsPath);
  
  if (imageDirs.length === 0) {
    console.log('✓ No old image directories found!\n');
    return;
  }
  
  // Display what will be deleted
  console.log(`Found ${stats.dirsFound} directories containing ${stats.filesFound} files:\n`);
  
  imageDirs.forEach((dir, index) => {
    console.log(`${index + 1}. ${dir}`);
  });
  
  console.log('\n' + '='.repeat(60));
  
  if (CONFIG.dryRun) {
    console.log('\n💡 This is a DRY RUN. No files were deleted.');
    console.log('\nTo actually delete these directories:');
    console.log('1. Verify your documentation works correctly');
    console.log('2. Edit this script and set dryRun: false');
    console.log('3. Run the script again\n');
  } else {
    // Actually delete the directories
    console.log('\n🗑️  Deleting directories...\n');
    
    for (const dir of imageDirs) {
      const success = await deleteDirectory(dir);
      if (success) {
        console.log(`✓ Deleted: ${dir}`);
      } else {
        console.log(`✗ Failed: ${dir}`);
      }
    }
    
    console.log('\n' + '='.repeat(60));
    console.log('CLEANUP COMPLETE');
    console.log('='.repeat(60));
    console.log(`Directories deleted: ${stats.dirsDeleted}`);
    console.log(`Files removed: ${stats.filesFound}`);
    
    if (stats.errors.length > 0) {
      console.log(`\n⚠️  Errors: ${stats.errors.length}`);
      stats.errors.forEach(e => console.log(`  - ${e}`));
    }
    
    console.log('\n✅ Old image directories have been removed!');
    console.log('You can now safely delete the backup-images directory.\n');
  }
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
