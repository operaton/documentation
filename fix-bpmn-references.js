/**
 * Script to fix BPMN references in Markdown and MDX files (with dry-run mode)
 * 
 * Dry-run mode logs changes without writing to files.
 * Set DRY_RUN = false to apply changes.
 * 
 * Replaces:
 *   <div data-bpmn-diagram="../bpmn/diagram"></div>
 *   <div data-bpmn-diagram="../bpmn/diagram" />
 * With:
 *   <div data-bpmn-diagram="./bpmn/diagram"></div>
 *   <div data-bpmn-diagram="./bpmn/diagram" />
 */

const fs = require('fs');
const path = require('path');
const { glob } = require('glob');

const DRY_RUN = true; // <-- set to false to actually write changes
const docsDir = path.join(__dirname, 'docs'); // Adjust if your docs folder is elsewhere

async function fixBpmnReferences() {
  // Match both .md and .mdx files
  const pattern = path.join(docsDir, '**/*.{md,mdx}').replace(/\\/g, '/');
  const files = await glob(pattern, { nodir: true });

  console.log(`[fix-bpmn] Found ${files.length} Markdown/MDX files`);

  let totalReplacements = 0;

  for (const file of files) {
    let content = fs.readFileSync(file, 'utf-8');
    let replacements = 0;

    // Regex: matches data-bpmn-diagram="../bpmn/..." in both <div></div> and <div ... />
    const newContent = content.replace(
      /(data-bpmn-diagram\s*=\s*["'])\.\.\/bpmn\//g,
      (match, p1) => {
        replacements++;
        return `${p1}./bpmn/`;
      }
    );

    if (replacements > 0) {
      totalReplacements += replacements;

      if (DRY_RUN) {
        console.log(`[dry-run] ${replacements} reference(s) WOULD be fixed in: ${file}`);
      } else {
        fs.writeFileSync(file, newContent, 'utf-8');
        console.log(`[fix-bpmn] ${replacements} reference(s) fixed in: ${file}`);
      }
    }
  }

  console.log(`[fix-bpmn] Done! Total replacements across all files: ${totalReplacements}`);
  if (DRY_RUN) {
    console.log('[dry-run] No files were modified. Set DRY_RUN = false to apply changes.');
  }
}

fixBpmnReferences().catch(err => console.error(err));
