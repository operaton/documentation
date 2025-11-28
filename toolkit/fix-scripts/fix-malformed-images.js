#!/usr/bin/env node

/**
 * Fix Malformed Image References
 * 
 * This script fixes various malformed image references found in the documentation:
 * 1. Images with trailing quotes and extra attributes
 * 2. HTML img tags that should be markdown
 * 3. Missing closing parentheses
 */

const fs = require('fs').promises;

const fixes = [
  {
    file: 'docs/documentation/reference/forms/embedded-forms/javascript/examples.md',
    description: 'Angular template - leave as-is (not a real image reference)',
    action: 'skip' // This is actually Angular template syntax, not a broken image
  },
  {
    file: 'docs/documentation/user-guide/process-engine/external-tasks.md',
    description: 'Fix unclosed markdown image with extra quote',
    find: '![Example img](./img/external-task-long-polling.png" alt="Long polling to fetch and lock external tasks',
    replace: '![Long polling to fetch and lock external tasks](./img/external-task-long-polling.png)'
  },
  {
    file: 'docs/documentation/user-guide/process-engine/transactions-in-processes.md',
    description: 'Convert HTML img to markdown (already handled by migration script)',
    action: 'skip' // Migration script handles this correctly
  },
  {
    file: 'docs/documentation/user-guide/spring-framework-integration/transactions.md',
    description: 'Code example - leave as-is (not an image reference)',
    action: 'skip' // This is Java code, not an image reference
  },
  {
    file: 'docs/documentation/user-guide/testing/index.md',
    description: 'Convert HTML img tags to markdown',
    fixes: [
      {
        find: '<img src="img/api-test-debug-breakpoint.png" title="API Test Debugging"/>',
        replace: '![API Test Debugging](img/api-test-debug-breakpoint.png)'
      },
      {
        find: '<img src="img/api-test-debug-view.png" title="API Test Debugging"/>',
        replace: '![API Test Debugging](img/api-test-debug-view.png)'
      },
      {
        find: '<img src="img/api-test-debug-start-h2-server.png" title="API Test Debugging"/>',
        replace: '![API Test Debugging](img/api-test-debug-start-h2-server.png)'
      },
      {
        find: '<img src="img/api-test-debug-start-h2-server-2.png" title="API Test Debugging"/>',
        replace: '![API Test Debugging](img/api-test-debug-start-h2-server-2.png)'
      },
      {
        find: '<img src="img/api-test-debug-h2-login.png" title="API Test Debugging"/>',
        replace: '![API Test Debugging](img/api-test-debug-h2-login.png)'
      },
      {
        find: '<img src="img/api-test-debug-h2-tables.png" title="API Test Debugging"/>',
        replace: '![API Test Debugging](img/api-test-debug-h2-tables.png)'
      },
      {
        find: '<img src="img/test-scopes.png" title="Testing Scopes"/>',
        replace: '![Testing Scopes](img/test-scopes.png)'
      }
    ]
  },
  {
    file: 'docs/documentation/webapps/cockpit/batch/batch-operation.md',
    description: 'Fix markdown images with extra quotes and attributes',
    fixes: [
      {
        find: '![Example img](./../img/batch/batch_operation_confirmation.png" alt="Batch Operation Confirmation" caption="',
        replace: '![Batch Operation Confirmation](./../img/batch/batch_operation_confirmation.png)'
      },
      {
        find: '![Example img](./../img/batch/batch_operation_result.png" alt="Batch Operation Result" caption="',
        replace: '![Batch Operation Result](./../img/batch/batch_operation_result.png)'
      }
    ]
  },
  {
    file: 'docs/documentation/webapps/cockpit/bpmn/correlate-message.md',
    description: 'Fix markdown images with extra quotes and attributes',
    fixes: [
      {
        find: '![Example img](./../img/correlate-message/batch-operation.png" alt="Correlate Message Batch Operation" caption="',
        replace: '![Correlate Message Batch Operation](./../img/correlate-message/batch-operation.png)'
      },
      {
        find: '![Example img](./../img/correlate-message/process-action.png" alt="Process action to correlate a message" caption="Process action to correlate a message',
        replace: '![Process action to correlate a message](./../img/correlate-message/process-action.png)'
      },
      {
        find: '![Example img](./../img/correlate-message/modal-dialog.png" alt="Modal dialog to correlate a message" caption="Modal dialog to correlate a message',
        replace: '![Modal dialog to correlate a message](./../img/correlate-message/modal-dialog.png)'
      },
      {
        find: '![Example img](./../img/correlate-message/diagram-overlay-button.png" alt="Diagram overlay button" caption="Diagram overlay button',
        replace: '![Diagram overlay button](./../img/correlate-message/diagram-overlay-button.png)'
      }
    ]
  }
];

async function fixFile(fix) {
  if (fix.action === 'skip') {
    console.log(`⊘ Skipping ${fix.file}: ${fix.description}`);
    return { skipped: true };
  }

  try {
    let content = await fs.readFile(fix.file, 'utf8');
    let modified = false;
    let changesCount = 0;

    if (fix.fixes) {
      // Multiple fixes in one file
      for (const subFix of fix.fixes) {
        if (content.includes(subFix.find)) {
          content = content.replace(subFix.find, subFix.replace);
          modified = true;
          changesCount++;
        }
      }
    } else if (fix.find && fix.replace) {
      // Single fix
      if (content.includes(fix.find)) {
        content = content.replace(fix.find, fix.replace);
        modified = true;
        changesCount = 1;
      }
    }

    if (modified) {
      await fs.writeFile(fix.file, content, 'utf8');
      console.log(`✓ Fixed ${fix.file}: ${fix.description} (${changesCount} changes)`);
      return { fixed: true, changes: changesCount };
    } else {
      console.log(`⚠ No changes needed for ${fix.file}: pattern not found`);
      return { unchanged: true };
    }
  } catch (err) {
    console.error(`✗ Error processing ${fix.file}: ${err.message}`);
    return { error: true, message: err.message };
  }
}

async function main() {
  console.log('🔧 Fixing malformed image references...\n');

  const results = {
    fixed: 0,
    skipped: 0,
    unchanged: 0,
    errors: 0,
    totalChanges: 0
  };

  for (const fix of fixes) {
    const result = await fixFile(fix);
    
    if (result.fixed) {
      results.fixed++;
      results.totalChanges += result.changes;
    } else if (result.skipped) {
      results.skipped++;
    } else if (result.unchanged) {
      results.unchanged++;
    } else if (result.error) {
      results.errors++;
    }
  }

  console.log('\n' + '='.repeat(60));
  console.log('SUMMARY');
  console.log('='.repeat(60));
  console.log(`Files fixed: ${results.fixed}`);
  console.log(`Files skipped: ${results.skipped}`);
  console.log(`Files unchanged: ${results.unchanged}`);
  console.log(`Errors: ${results.errors}`);
  console.log(`Total changes made: ${results.totalChanges}`);
  console.log('='.repeat(60) + '\n');

  if (results.fixed > 0) {
    console.log('✅ Image references have been fixed!');
    console.log('Next steps:');
    console.log('1. Review the changes with git diff');
    console.log('2. Run the migration script again in dry-run mode');
    console.log('3. If everything looks good, run the actual migration\n');
  }
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
