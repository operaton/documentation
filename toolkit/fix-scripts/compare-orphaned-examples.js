#!/usr/bin/env node

/**
 * Compare Orphaned vs Examples Directories
 * 
 * Checks if files exist in both orphaned/ and examples/ directories
 * and helps decide which to keep/delete
 */

const fs = require('fs').promises;
const path = require('path');
const { execSync } = require('child_process');

async function findDirectories() {
  console.log('🔍 Searching for orphaned/ and examples/ directories...\n');
  
  try {
    const orphanedDirs = execSync(
      'find static/img -type d -name "orphaned" 2>/dev/null',
      { encoding: 'utf8' }
    ).trim().split('\n').filter(Boolean);
    
    const examplesDirs = execSync(
      'find static/img -type d -name "examples" 2>/dev/null',
      { encoding: 'utf8' }
    ).trim().split('\n').filter(Boolean);
    
    return { orphanedDirs, examplesDirs };
  } catch (err) {
    console.error('Error finding directories:', err.message);
    return { orphanedDirs: [], examplesDirs: [] };
  }
}

async function getFilesInDirectory(dir) {
  try {
    const files = execSync(
      `find "${dir}" -type f 2>/dev/null`,
      { encoding: 'utf8' }
    ).trim().split('\n').filter(Boolean);
    
    return files.map(f => ({
      fullPath: f,
      relativePath: f.replace(dir + '/', ''),
      basename: path.basename(f),
      size: 0 // We'll get this if needed
    }));
  } catch (err) {
    return [];
  }
}

async function compareDirectories() {
  console.log('=' .repeat(70));
  console.log('ORPHANED vs EXAMPLES DIRECTORY COMPARISON');
  console.log('=' .repeat(70) + '\n');
  
  const { orphanedDirs, examplesDirs } = await findDirectories();
  
  console.log(`Found ${orphanedDirs.length} orphaned/ directories`);
  console.log(`Found ${examplesDirs.length} examples/ directories\n`);
  
  if (orphanedDirs.length === 0 && examplesDirs.length === 0) {
    console.log('✅ No orphaned/ or examples/ directories found!');
    console.log('Either they were never created or already cleaned up.\n');
    return;
  }
  
  // Check if both exist in same parent directories
  const orphanedParents = new Set(orphanedDirs.map(d => path.dirname(d)));
  const examplesParents = new Set(examplesDirs.map(d => path.dirname(d)));
  
  const commonParents = [...orphanedParents].filter(p => examplesParents.has(p));
  
  if (commonParents.length > 0) {
    console.log('⚠️  DUPLICATE DIRECTORIES FOUND!');
    console.log('Both orphaned/ and examples/ exist in these locations:\n');
    
    for (const parent of commonParents) {
      console.log(`📁 ${parent}/`);
      console.log(`   - orphaned/`);
      console.log(`   - examples/`);
      console.log('');
    }
  }
  
  console.log('\n' + '─'.repeat(70));
  console.log('DETAILED COMPARISON');
  console.log('─'.repeat(70) + '\n');
  
  // Compare file contents
  const allOrphanedFiles = [];
  const allExamplesFiles = [];
  
  for (const dir of orphanedDirs) {
    const files = await getFilesInDirectory(dir);
    allOrphanedFiles.push(...files);
  }
  
  for (const dir of examplesDirs) {
    const files = await getFilesInDirectory(dir);
    allExamplesFiles.push(...files);
  }
  
  console.log(`Total files in orphaned/ : ${allOrphanedFiles.length}`);
  console.log(`Total files in examples/ : ${allExamplesFiles.length}\n`);
  
  // Check for duplicates (same filename in both)
  const orphanedBasenames = new Set(allOrphanedFiles.map(f => f.basename));
  const examplesBasenames = new Set(allExamplesFiles.map(f => f.basename));
  
  const duplicateFiles = [...orphanedBasenames].filter(name => examplesBasenames.has(name));
  
  if (duplicateFiles.length > 0) {
    console.log(`⚠️  ${duplicateFiles.length} files exist in BOTH directories!\n`);
    console.log('Duplicate files:');
    duplicateFiles.slice(0, 10).forEach(name => console.log(`  - ${name}`));
    if (duplicateFiles.length > 10) {
      console.log(`  ... and ${duplicateFiles.length - 10} more\n`);
    }
  } else {
    console.log('✅ No duplicate filenames found\n');
  }
  
  // Files only in orphaned
  const onlyInOrphaned = [...orphanedBasenames].filter(name => !examplesBasenames.has(name));
  if (onlyInOrphaned.length > 0) {
    console.log(`\n📋 ${onlyInOrphaned.length} files ONLY in orphaned/:`);
    onlyInOrphaned.slice(0, 10).forEach(name => console.log(`  - ${name}`));
    if (onlyInOrphaned.length > 10) {
      console.log(`  ... and ${onlyInOrphaned.length - 10} more`);
    }
  }
  
  // Files only in examples
  const onlyInExamples = [...examplesBasenames].filter(name => !orphanedBasenames.has(name));
  if (onlyInExamples.length > 0) {
    console.log(`\n📋 ${onlyInExamples.length} files ONLY in examples/:`);
    onlyInExamples.slice(0, 10).forEach(name => console.log(`  - ${name}`));
    if (onlyInExamples.length > 10) {
      console.log(`  ... and ${onlyInExamples.length - 10} more`);
    }
  }
  
  console.log('\n' + '=' .repeat(70));
  console.log('RECOMMENDATION');
  console.log('=' .repeat(70) + '\n');
  
  if (orphanedDirs.length === 0) {
    console.log('✅ No orphaned/ directories to clean up!');
  } else if (examplesDirs.length === 0) {
    console.log('ℹ️  Only orphaned/ directories exist (no examples/)');
    console.log('This is fine - you can keep orphaned/ or rename it to examples/');
  } else if (duplicateFiles.length > 0) {
    console.log('⚠️  ACTION REQUIRED: Duplicate files detected!');
    console.log('\nOptions:');
    console.log('1. Compare the duplicate files to ensure they\'re identical');
    console.log('2. If identical, delete orphaned/ and keep examples/');
    console.log('3. If different, investigate which version is correct');
    console.log('\nTo compare duplicates:');
    console.log('  diff static/img/.../orphaned/file.png static/img/.../examples/file.png');
  } else if (onlyInOrphaned.length > 0) {
    console.log('⚠️  Files exist only in orphaned/');
    console.log('\nOptions:');
    console.log('1. Move files from orphaned/ to examples/');
    console.log('2. Keep both directories');
    console.log('3. Review and delete orphaned/ if files aren\'t needed');
  } else {
    console.log('✅ SAFE TO DELETE orphaned/ directories');
    console.log('All files are in examples/, orphaned/ is empty or redundant');
    console.log('\nCommand to delete:');
    console.log('  find static/img -type d -name "orphaned" -exec rm -rf {} +');
  }
  
  console.log('\n' + '=' .repeat(70));
  console.log('DETAILED FILE LISTINGS');
  console.log('=' .repeat(70) + '\n');
  
  if (orphanedDirs.length > 0) {
    console.log('📁 ORPHANED directories:\n');
    for (const dir of orphanedDirs) {
      const files = await getFilesInDirectory(dir);
      console.log(`${dir}/ (${files.length} files)`);
      if (files.length > 0 && files.length <= 5) {
        files.forEach(f => console.log(`  - ${f.basename}`));
      } else if (files.length > 5) {
        files.slice(0, 3).forEach(f => console.log(`  - ${f.basename}`));
        console.log(`  ... and ${files.length - 3} more`);
      }
      console.log('');
    }
  }
  
  if (examplesDirs.length > 0) {
    console.log('📁 EXAMPLES directories:\n');
    for (const dir of examplesDirs) {
      const files = await getFilesInDirectory(dir);
      console.log(`${dir}/ (${files.length} files)`);
      if (files.length > 0 && files.length <= 5) {
        files.forEach(f => console.log(`  - ${f.basename}`));
      } else if (files.length > 5) {
        files.slice(0, 3).forEach(f => console.log(`  - ${f.basename}`));
        console.log(`  ... and ${files.length - 3} more`);
      }
      console.log('');
    }
  }
}

compareDirectories().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
