#!/usr/bin/env node

/**
 * Fix Broken References - Correct Paths Edition
 * 
 * Updates markdown references to match where files actually are after migration.
 * Files were moved to static/img/documentation/reference/bpmn20/ (without symbols/events subdirs)
 */

const fs = require('fs').promises;

const fixes = [
  // Fix 1: variables-3.png
  {
    file: 'docs/documentation/user-guide/process-engine/variables.md',
    description: 'Fix variables-3.png reference',
    replacements: [
      {
        find: './img/variables-3.png',
        replace: '/img/documentation/user-guide/process-engine/variables-3.png'
      }
    ]
  },
  
  // Fix 2-3: Plugin overlay images
  {
    file: 'docs/documentation/webapps/cockpit/extend/plugins.md',
    description: 'Fix plugin-point overlay image references',
    replacements: [
      {
        find: './../img/plugin-points/plugin-point-case-definition-diagram-overlay.png',
        replace: '/img/documentation/webapps/cockpit/plugin-points/plugin-point-case-definition-diagram-overlay.png'
      },
      {
        find: './../img/plugin-points/plugin-point-case-instance-diagram-overlay.png',
        replace: '/img/documentation/webapps/cockpit/plugin-points/plugin-point-case-instance-diagram-overlay.png'
      }
    ]
  },
  
  // Fix 4: start-form-generic.png
  {
    file: 'docs/get-started/quick-start/user-task.md',
    description: 'Fix start-form-generic.png reference',
    replacements: [
      {
        find: './img/start-form-generic.png',
        replace: '/img/get-started/quick-start/start-form-generic.png'
      }
    ]
  },
  
  // Fix 5-16: All 12 event symbol SVGs - NOTE: NO symbols/events/ in path!
  {
    file: 'docs/documentation/reference/bpmn20/index.md',
    description: 'Fix 12 event symbol SVG references (files are at bpmn20/ root, not in symbols/events/)',
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
  }
];

async function fixFile(fix) {
  try {
    console.log(`\n📝 Processing: ${fix.file}`);
    console.log(`   ${fix.description}`);
    
    let content = await fs.readFile(fix.file, 'utf8');
    let modified = false;
    let changesCount = 0;
    
    for (const replacement of fix.replacements) {
      const findRegex = new RegExp(
        replacement.find.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'),
        'g'
      );
      
      if (content.includes(replacement.find)) {
        content = content.replace(findRegex, replacement.replace);
        modified = true;
        changesCount++;
        console.log(`   ✅ ${replacement.find.substring(0, 40)}...`);
      }
    }
    
    if (modified) {
      await fs.writeFile(fix.file, content, 'utf8');
      console.log(`   ✨ Saved ${changesCount} change(s)`);
      return { fixed: true, changes: changesCount };
    } else {
      console.log(`   ⚠️  No changes needed`);
      return { unchanged: true };
    }
  } catch (err) {
    console.error(`   ❌ Error: ${err.message}`);
    return { error: true, message: err.message };
  }
}

async function main() {
  console.log('🔧 Fix Broken References - Correct Paths');
  console.log('=' .repeat(70));
  console.log('Updating markdown to match actual file locations...\n');

  const results = {
    fixed: 0,
    unchanged: 0,
    errors: 0,
    totalChanges: 0
  };

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
    console.log('\n✅ All references fixed!');
    console.log('\nNext steps:');
    console.log('1. Run: node check-broken-references.js');
    console.log('2. Test: npm start');
    console.log('3. Should build with 0 errors!\n');
  }
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
