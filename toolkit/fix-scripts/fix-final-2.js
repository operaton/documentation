#!/usr/bin/env node

/**
 * Fix Last 2 References - Plugin Overlay Images
 * 
 * Files are in .../extend/ directory, not .../plugin-points/
 */

const fs = require('fs').promises;

async function fixLastTwo() {
  const file = 'docs/documentation/webapps/cockpit/extend/plugins.md';
  
  console.log('🔧 Fixing last 2 broken references...\n');
  console.log(`📝 File: ${file}\n`);
  
  try {
    let content = await fs.readFile(file, 'utf8');
    let changes = 0;
    
    // Fix 1: case-definition
    const oldPath1 = '/img/documentation/webapps/cockpit/plugin-points/plugin-point-case-definition-diagram-overlay.png';
    const newPath1 = '/img/documentation/webapps/cockpit/extend/plugin-point-case-definition-diagram-overlay.png';
    
    if (content.includes(oldPath1)) {
      content = content.replace(
        new RegExp(oldPath1.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'),
        newPath1
      );
      changes++;
      console.log('✅ Fixed: plugin-point-case-definition-diagram-overlay.png');
      console.log(`   Old: .../plugin-points/...`);
      console.log(`   New: .../extend/...\n`);
    }
    
    // Fix 2: case-instance
    const oldPath2 = '/img/documentation/webapps/cockpit/plugin-points/plugin-point-case-instance-diagram-overlay.png';
    const newPath2 = '/img/documentation/webapps/cockpit/extend/plugin-point-case-instance-diagram-overlay.png';
    
    if (content.includes(oldPath2)) {
      content = content.replace(
        new RegExp(oldPath2.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'),
        newPath2
      );
      changes++;
      console.log('✅ Fixed: plugin-point-case-instance-diagram-overlay.png');
      console.log(`   Old: .../plugin-points/...`);
      console.log(`   New: .../extend/...\n`);
    }
    
    if (changes > 0) {
      await fs.writeFile(file, content, 'utf8');
      console.log('=' .repeat(70));
      console.log(`✅ SUCCESS! Fixed ${changes} reference(s)`);
      console.log('=' .repeat(70));
      console.log('\nNext steps:');
      console.log('1. Run: node check-broken-references.js');
      console.log('2. Should show: Broken references: 0 ✅');
      console.log('3. Test: npm start');
      console.log('4. Should build with 0 errors! 🎉\n');
    } else {
      console.log('⚠️  No changes needed - references may already be fixed\n');
    }
    
  } catch (err) {
    console.error(`❌ Error: ${err.message}`);
    process.exit(1);
  }
}

fixLastTwo();
