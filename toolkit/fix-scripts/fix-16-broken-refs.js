#!/usr/bin/env node

/**
 * Fix 16 Broken Asset References After Migration
 * 
 * Updates paths to match actual file locations in static/img/
 */

const fs = require('fs').promises;

const fixes = [
  {
    file: 'docs/documentation/reference/bpmn20/index.md',
    description: 'Fix 12 SVG event symbol paths (remove symbols/events subdirectory)',
    replacements: [
      {
        find: './img/symbols/events/message_start_event.svg',
        replace: '/img/documentation/reference/bpmn20/message_start_event.svg'
      },
      {
        find: './img/symbols/events/message_intermediate_catch_event.svg',
        replace: '/img/documentation/reference/bpmn20/message_intermediate_catch_event.svg'
      },
      {
        find: './img/symbols/events/timer_start_event.svg',
        replace: '/img/documentation/reference/bpmn20/timer_start_event.svg'
      },
      {
        find: './img/symbols/events/timer_intermediate_event.svg',
        replace: '/img/documentation/reference/bpmn20/timer_intermediate_event.svg'
      },
      {
        find: './img/symbols/events/conditional_start_event.svg',
        replace: '/img/documentation/reference/bpmn20/conditional_start_event.svg'
      },
      {
        find: './img/symbols/events/conditional_intermediate_catch_event.svg',
        replace: '/img/documentation/reference/bpmn20/conditional_intermediate_catch_event.svg'
      },
      {
        find: './img/symbols/events/signal_start_event.svg',
        replace: '/img/documentation/reference/bpmn20/signal_start_event.svg'
      },
      {
        find: './img/symbols/events/signal_intermediate_catch_event.svg',
        replace: '/img/documentation/reference/bpmn20/signal_intermediate_catch_event.svg'
      },
      {
        find: './img/symbols/events/multiple_start_event.svg',
        replace: '/img/documentation/reference/bpmn20/multiple_start_event.svg'
      },
      {
        find: './img/symbols/events/multiple_intermediate_catch_event.svg',
        replace: '/img/documentation/reference/bpmn20/multiple_intermediate_catch_event.svg'
      },
      {
        find: './img/symbols/events/multiple_parallel_start_event.svg',
        replace: '/img/documentation/reference/bpmn20/multiple_parallel_start_event.svg'
      },
      {
        find: './img/symbols/events/multiple_parallel_catch_event.svg',
        replace: '/img/documentation/reference/bpmn20/multiple_parallel_catch_event.svg'
      }
    ]
  },
  {
    file: 'docs/documentation/user-guide/process-engine/variables.md',
    description: 'Fix variables-3.png path',
    find: './img/variables-3.png',
    replace: '/img/documentation/user-guide/process-engine/variables-3.png'
  },
  {
    file: 'docs/documentation/webapps/cockpit/extend/plugins.md',
    description: 'Fix plugin overlay image paths',
    replacements: [
      {
        find: './../img/plugin-points/plugin-point-case-definition-diagram-overlay.png',
        replace: '/img/documentation/webapps/cockpit/extend/plugin-point-case-definition-diagram-overlay.png'
      },
      {
        find: './../img/plugin-points/plugin-point-case-instance-diagram-overlay.png',
        replace: '/img/documentation/webapps/cockpit/extend/plugin-point-case-instance-diagram-overlay.png'
      }
    ]
  },
  {
    file: 'docs/get-started/quick-start/user-task.md',
    description: 'Fix start-form-generic.png path',
    find: './img/start-form-generic.png',
    replace: '/img/get-started/quick-start/start-form-generic.png'
  }
];

async function fixFile(fix) {
  try {
    console.log(`\n📝 ${fix.file}`);
    console.log(`   ${fix.description}`);
    
    let content = await fs.readFile(fix.file, 'utf8');
    let modified = false;
    let changesCount = 0;
    
    // Handle single fix or multiple fixes
    const replacements = fix.replacements || [{ find: fix.find, replace: fix.replace }];
    
    for (const replacement of replacements) {
      if (content.includes(replacement.find)) {
        content = content.replace(new RegExp(replacement.find.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), replacement.replace);
        modified = true;
        changesCount++;
      }
    }
    
    if (modified) {
      await fs.writeFile(fix.file, content, 'utf8');
      console.log(`   ✅ Fixed ${changesCount} reference(s)`);
      return { fixed: true, changes: changesCount };
    } else {
      console.log(`   ⚠️  Pattern not found (already fixed?)`);
      return { unchanged: true };
    }
  } catch (err) {
    console.error(`   ❌ Error: ${err.message}`);
    return { error: true };
  }
}

async function main() {
  console.log('🔧 Fixing 16 Broken Asset References\n');
  console.log('='.repeat(70));
  
  const results = { fixed: 0, unchanged: 0, errors: 0, totalChanges: 0 };
  
  for (const fix of fixes) {
    const result = await fixFile(fix);
    if (result.fixed) {
      results.fixed++;
      results.totalChanges += result.changes;
    } else if (result.unchanged) {
      results.unchanged++;
    } else if (result.error) {
      results.errors++;
    }
  }
  
  console.log('\n' + '='.repeat(70));
  console.log('SUMMARY');
  console.log('='.repeat(70));
  console.log(`Files fixed: ${results.fixed}`);
  console.log(`Files unchanged: ${results.unchanged}`);
  console.log(`Errors: ${results.errors}`);
  console.log(`Total changes: ${results.totalChanges}`);
  console.log('='.repeat(70));
  
  if (results.fixed > 0) {
    console.log('\n✅ References fixed!');
    console.log('\nNext: Run check-broken-references.js to verify\n');
  }
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
