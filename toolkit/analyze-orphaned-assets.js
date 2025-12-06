#!/usr/bin/env node

/**
 * Orphaned Assets Analyzer
 * 
 * Reviews the 91 orphaned assets and provides recommendations
 */

const fs = require('fs').promises;
const path = require('path');

const orphanedAssets = {
  bpmn: [
    'documentation/reference/bpmn20/events/bpmn/catchandthrowpattern.bpmn',
    'documentation/reference/bpmn20/events/bpmn/compensation-event-subprocess.bpmn',
    'documentation/reference/bpmn20/events/bpmn/compensation-intermediate-throw-event.bpmn',
    'documentation/reference/bpmn20/events/bpmn/conditionalEventScopes.bpmn',
    'documentation/reference/bpmn20/events/bpmn/conditionalEventScopesHighestFirst.bpmn',
    'documentation/reference/bpmn20/events/bpmn/escalation-boundary-event.bpmn',
    'documentation/reference/bpmn20/events/bpmn/escalation-end-event.bpmn',
    'documentation/reference/bpmn20/events/bpmn/escalation-example.bpmn',
    'documentation/reference/bpmn20/events/bpmn/escalation-intermediate-throw-event.bpmn',
    'documentation/reference/bpmn20/events/bpmn/escalation-start-event.bpmn',
    'documentation/reference/bpmn20/events/bpmn/event-conditional-parallel-boundary.bpmn',
    'documentation/reference/bpmn20/events/bpmn/event-conditional.bpmn',
    'documentation/reference/bpmn20/events/bpmn/event-conditional2.bpmn',
    'documentation/reference/bpmn20/events/bpmn/event-error.bpmn',
    'documentation/reference/bpmn20/events/bpmn/event-link.bpmn',
    'documentation/reference/bpmn20/events/bpmn/event-message-start-alternative.bpmn',
    'documentation/reference/bpmn20/events/bpmn/event-message-throwing.bpmn',
    'documentation/reference/bpmn20/events/bpmn/event-message.bpmn',
    'documentation/reference/bpmn20/events/bpmn/event-none-intermediate.bpmn',
    'documentation/reference/bpmn20/events/bpmn/event-none.bpmn',
    'documentation/reference/bpmn20/events/bpmn/event-signal-catching.bpmn',
    'documentation/reference/bpmn20/events/bpmn/event-signal-throwing.bpmn',
    'documentation/reference/bpmn20/events/bpmn/event-subprocess-alternative1.bpmn',
    'documentation/reference/bpmn20/events/bpmn/event-subprocess-alternative2.bpmn',
    'documentation/reference/bpmn20/events/bpmn/event-terminate.bpmn',
    'documentation/reference/bpmn20/events/bpmn/event-timer.bpmn',
    'documentation/reference/bpmn20/gateways/bpmn/event-based-gateway.bpmn',
    'documentation/reference/bpmn20/gateways/bpmn/exclusive-gateway.bpmn',
    'documentation/reference/bpmn20/gateways/bpmn/inclusive-gateway.bpmn',
    'documentation/reference/bpmn20/gateways/bpmn/inclusive_gateway_scenario_1.bpmn',
    'documentation/reference/bpmn20/gateways/bpmn/inclusive_gateway_scenario_2.bpmn',
    'documentation/reference/bpmn20/gateways/bpmn/inclusive_gateway_scenario_3.bpmn',
    'documentation/reference/bpmn20/gateways/bpmn/inclusive_gateway_scenario_4.bpmn',
    'documentation/reference/bpmn20/gateways/bpmn/parallel-gateway-unbalanced.bpmn',
    'documentation/reference/bpmn20/gateways/bpmn/parallel-gateway.bpmn',
    'documentation/reference/bpmn20/gateways/bpmn/sequence-flow-conditional.bpmn',
    'documentation/reference/bpmn20/gateways/bpmn/sequence-flow-parallel.bpmn',
    'documentation/reference/bpmn20/subprocesses/bpmn/business-transaction.bpmn',
    'documentation/reference/bpmn20/subprocesses/bpmn/call-activity.bpmn',
    'documentation/reference/bpmn20/subprocesses/bpmn/event-subprocess-alternative1.bpmn',
    'documentation/reference/bpmn20/subprocesses/bpmn/event-subprocess-alternative2.bpmn',
    'documentation/reference/bpmn20/subprocesses/bpmn/event-subprocess.bpmn',
    'documentation/reference/bpmn20/subprocesses/bpmn/subprocess.bpmn',
    'documentation/reference/bpmn20/subprocesses/bpmn/subprocess_attached.bpmn',
    'documentation/reference/bpmn20/subprocesses/bpmn/subprocess_event.bpmn',
    'documentation/reference/bpmn20/subprocesses/bpmn/subprocess_expanded.bpmn',
    'documentation/reference/bpmn20/tasks/bpmn/compensation-marker.bpmn',
    'documentation/reference/bpmn20/tasks/bpmn/loop-alternative.bpmn',
    'documentation/reference/bpmn20/tasks/bpmn/multiple-instance-boundary.bpmn',
    'documentation/reference/bpmn20/tasks/bpmn/multiple-instance.bpmn',
    'documentation/user-guide/process-engine/bpmn/example1.bpmn',
    'documentation/user-guide/process-engine/bpmn/example2.bpmn',
    'documentation/user-guide/process-engine/bpmn/example3.bpmn',
    'documentation/user-guide/process-engine/bpmn/example4.bpmn',
    'documentation/user-guide/process-engine/bpmn/example5.bpmn',
    'documentation/user-guide/process-engine/bpmn/process-instance-migration/example-boundary-timer1.bpmn',
    'documentation/user-guide/process-engine/bpmn/process-instance-migration/example-boundary-timer2.bpmn',
    'documentation/user-guide/process-engine/bpmn/process-instance-migration/example-compensation1.bpmn',
    'documentation/user-guide/process-engine/bpmn/process-instance-migration/example-compensation2.bpmn',
    'documentation/user-guide/process-engine/bpmn/process-instance-migration/example-compensation3.bpmn',
    'documentation/user-guide/process-engine/bpmn/process-instance-migration/example-compensation4.bpmn',
    'documentation/user-guide/process-engine/bpmn/process-instance-migration/example-compensation5.bpmn',
    'documentation/user-guide/process-engine/bpmn/process-instance-migration/example-compensation6.bpmn',
    'documentation/user-guide/process-engine/bpmn/process-instance-migration/example1.bpmn',
    'documentation/user-guide/process-engine/bpmn/process-instance-migration/example2.bpmn',
    'documentation/user-guide/process-engine/bpmn/x_event-based-gateway.bpmn'
  ],
  
  images: [
    'documentation/img/docsVersionDropdown.png',
    'documentation/img/localeDropdown.png',
    'documentation/reference/dmn/decision-literal-expression/img/decision-id.png',
    'documentation/reference/dmn/decision-literal-expression/img/decision-literal-expression.png',
    'documentation/reference/dmn/decision-literal-expression/img/decision-name.png',
    'documentation/user-guide/ext-client/img/externalTaskCient.png',
    'documentation/user-guide/process-engine/img/process-engine-history.png',
    'documentation/webapps/cockpit/img/cockpit-edit-dmn-dialog.png',
    'documentation/webapps/cockpit/img/cockpit-plugins/architecture.png',
    'documentation/webapps/cockpit/img/migration/step4_error.png',
    'documentation/webapps/tasklist/img/tasklist-dashboard.png',
    'documentation/webapps/tasklist/img/tasklist-generic-form.png',
    'documentation/webapps/welcome/img/welcome-start-page-view.png',
    'get-started/archive/java-process-app/img/modeler-save-diagram.png',
    'get-started/archive/javaee7/img/javaee.png',
    'get-started/archive/javaee7/img/start-form.png',
    'get-started/archive/spring/img/Spring_Logo.png',
    'get-started/quick-start/img/modeler-dmn1.png',
    'get-started/quick-start/img/niall-says-congrats.png'
  ],
  
  special: [
    'documentation/reference/dmn/decision-literal-expression/img/decision-literal-expression.dmn',
    'documentation/reference/dmn/drg/img/drg.dmn',
    'documentation/reference/dmn/decision-table/img/dish-table.svg',
    'documentation/reference/dmn/decision-table/img/map.js',
    'documentation/user-guide/process-engine/img/api.services.odg',
    'versions.json'
  ]
};

async function fileExists(filePath) {
  try {
    await fs.access(path.join('docs', filePath));
    return true;
  } catch {
    return false;
  }
}

async function analyzeOrphanedAssets() {
  console.log('🔍 Analyzing Orphaned Assets\n');
  console.log('=' .repeat(70));
  
  // Analyze BPMN files
  console.log('\n1️⃣  BPMN FILES (66 files)');
  console.log('-'.repeat(70));
  console.log('These appear to be example/reference BPMN diagrams.\n');
  
  const bpmnCategories = {
    events: orphanedAssets.bpmn.filter(f => f.includes('/events/')),
    gateways: orphanedAssets.bpmn.filter(f => f.includes('/gateways/')),
    subprocesses: orphanedAssets.bpmn.filter(f => f.includes('/subprocesses/')),
    tasks: orphanedAssets.bpmn.filter(f => f.includes('/tasks/')),
    migration: orphanedAssets.bpmn.filter(f => f.includes('/process-instance-migration/')),
    other: orphanedAssets.bpmn.filter(f => 
      !f.includes('/events/') && 
      !f.includes('/gateways/') && 
      !f.includes('/subprocesses/') && 
      !f.includes('/tasks/') &&
      !f.includes('/process-instance-migration/')
    )
  };
  
  Object.entries(bpmnCategories).forEach(([category, files]) => {
    if (files.length > 0) {
      console.log(`\n  ${category.toUpperCase()} (${files.length} files):`);
      console.log(`    Location: ${path.dirname(files[0]).replace('documentation/', '')}`);
      console.log(`    Examples: ${files.slice(0, 2).map(f => path.basename(f)).join(', ')}`);
    }
  });
  
  console.log('\n  📋 RECOMMENDATION:');
  console.log('    ✅ KEEP these files - they are reference examples for BPMN documentation');
  console.log('    📂 Move to: static/img/documentation/reference/bpmn20/examples/');
  console.log('    📝 Consider adding download links in relevant documentation pages');
  
  // Analyze images
  console.log('\n\n2️⃣  IMAGE FILES (19 files)');
  console.log('-'.repeat(70));
  
  const imageCategories = {
    docusaurus: orphanedAssets.images.filter(f => f.includes('docsVersionDropdown') || f.includes('localeDropdown')),
    dmn: orphanedAssets.images.filter(f => f.includes('/dmn/')),
    webapps: orphanedAssets.images.filter(f => f.includes('/webapps/')),
    getStarted: orphanedAssets.images.filter(f => f.includes('/get-started/')),
    other: orphanedAssets.images.filter(f => 
      !f.includes('docsVersionDropdown') && 
      !f.includes('localeDropdown') &&
      !f.includes('/dmn/') &&
      !f.includes('/webapps/') &&
      !f.includes('/get-started/')
    )
  };
  
  Object.entries(imageCategories).forEach(([category, files]) => {
    if (files.length > 0) {
      console.log(`\n  ${category.toUpperCase()} (${files.length} files):`);
      files.forEach(f => {
        console.log(`    - ${f}`);
      });
    }
  });
  
  console.log('\n  📋 RECOMMENDATION:');
  console.log('    ⚠️  REVIEW NEEDED:');
  console.log('       • Docusaurus UI images: Likely unused (old UI screenshots)');
  console.log('       • DMN images: May be alternate versions or deprecated');
  console.log('       • Webapp images: Could be old screenshots or deprecated features');
  console.log('       • Get-started images: Archive/legacy tutorial images');
  console.log('    ❓ Decision: Delete or move to archive?');
  
  // Analyze special files
  console.log('\n\n3️⃣  SPECIAL FILES (6 files)');
  console.log('-'.repeat(70));
  
  for (const file of orphanedAssets.special) {
    const ext = path.extname(file);
    const basename = path.basename(file);
    console.log(`\n  ${basename} (${ext})`);
    console.log(`    Location: ${path.dirname(file)}`);
    
    if (basename === 'versions.json') {
      console.log('    ⚠️  CRITICAL: This may be a Docusaurus versioning config file!');
      console.log('    📋 RECOMMENDATION: EXCLUDE from migration or verify it\'s not needed');
    } else if (ext === '.dmn') {
      console.log('    ℹ️  DMN decision model file (example/reference)');
      console.log('    📋 RECOMMENDATION: Keep with BPMN examples');
    } else if (ext === '.odg') {
      console.log('    ℹ️  OpenDocument Graphics (source file for diagrams)');
      console.log('    📋 RECOMMENDATION: Keep as source file, or move to separate /src directory');
    } else if (ext === '.svg') {
      console.log('    ℹ️  SVG image (might be generated from source)');
      console.log('    📋 RECOMMENDATION: Keep if used in documentation');
    } else if (ext === '.js') {
      console.log('    ℹ️  JavaScript utility file');
      console.log('    📋 RECOMMENDATION: Review purpose, might be DMN table configuration');
    }
  }
  
  // Summary and action items
  console.log('\n\n' + '='.repeat(70));
  console.log('📊 SUMMARY & ACTION ITEMS');
  console.log('='.repeat(70));
  
  console.log('\n✅ KEEP (Move to proper location):');
  console.log('   • 66 BPMN files → static/img/documentation/reference/examples/bpmn/');
  console.log('   • 2 DMN files → static/img/documentation/reference/examples/dmn/');
  console.log('   • 1 ODG file → static/img/documentation/sources/ (or keep with examples)');
  
  console.log('\n❓ REVIEW & DECIDE:');
  console.log('   • 19 PNG files → Likely old/unused screenshots');
  console.log('   • 1 SVG file (dish-table.svg) → Check if referenced indirectly');
  console.log('   • 1 JS file (map.js) → Check if used by DMN documentation');
  
  console.log('\n🚫 EXCLUDE FROM MIGRATION:');
  console.log('   • versions.json → Keep in docs/ root (verify first)');
  
  console.log('\n\n💡 RECOMMENDED SCRIPT MODIFICATIONS:');
  console.log('─'.repeat(70));
  console.log('1. Exclude versions.json from migration');
  console.log('2. Change orphaned directory from "orphaned" to "examples"');
  console.log('3. Consider separate "sources" directory for .odg files');
  
  console.log('\n\n📝 NEXT STEPS:');
  console.log('─'.repeat(70));
  console.log('1. Verify versions.json is not needed (check if file exists)');
  console.log('2. Review the 19 PNG files manually to confirm they can be archived/deleted');
  console.log('3. Update migration script with exclusions');
  console.log('4. Create post-migration script to move examples to better locations');
  console.log('5. Run migration with updated settings');
  
  console.log('\n' + '='.repeat(70) + '\n');
}

// Check if versions.json exists
async function checkVersionsJson() {
  console.log('\n🔍 Checking for versions.json...\n');
  
  const locations = [
    'docs/versions.json',
    './versions.json',
    'versions.json'
  ];
  
  for (const loc of locations) {
    const exists = await fileExists(loc);
    console.log(`  ${exists ? '✅' : '❌'} ${loc}`);
  }
  
  console.log('\n');
}

async function main() {
  await checkVersionsJson();
  await analyzeOrphanedAssets();
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
