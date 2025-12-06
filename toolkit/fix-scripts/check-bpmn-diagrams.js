#!/usr/bin/env node

/**
 * Analyze BPMN Diagram References
 * 
 * Finds all data-bpmn-diagram tags and checks if the referenced files exist
 */

const fs = require('fs').promises;
const path = require('path');
const { execSync } = require('child_process');

async function findBpmnReferences() {
  console.log('🔍 Searching for BPMN diagram references...\n');
  
  try {
    const grepResult = execSync(
      'grep -r "data-bpmn-diagram" docs/ --include="*.md" --include="*.mdx"',
      { encoding: 'utf8' }
    ).trim();
    
    const lines = grepResult.split('\n');
    
    console.log(`Found ${lines.length} BPMN diagram references\n`);
    console.log('=' .repeat(70));
    
    const issues = [];
    
    for (const line of lines) {
      const [filePath, ...rest] = line.split(':');
      const content = rest.join(':');
      
      // Extract the diagram path
      const match = content.match(/data-bpmn-diagram=["']([^"']+)["']/);
      if (!match) continue;
      
      const diagramPath = match[1];
      
      // Resolve the path
      const mdDir = path.dirname(filePath);
      let resolvedPath = path.resolve(mdDir, diagramPath);
      
      // Add .bpmn extension if not present
      if (!resolvedPath.endsWith('.bpmn')) {
        resolvedPath += '.bpmn';
      }
      
      console.log(`\n📄 ${filePath}`);
      console.log(`   References: ${diagramPath}`);
      console.log(`   Resolves to: ${resolvedPath}`);
      
      // Check if file exists at resolved path
      const existsAtResolved = await fileExists(resolvedPath);
      
      if (existsAtResolved) {
        console.log(`   ✅ File exists at resolved path`);
      } else {
        console.log(`   ❌ File NOT found at resolved path`);
        
        // Try to find it elsewhere
        const basename = path.basename(resolvedPath);
        const searchResult = execSync(
          `find . -name "${basename}" 2>/dev/null | head -5`,
          { encoding: 'utf8' }
        ).trim();
        
        if (searchResult) {
          console.log(`   🔍 Found elsewhere:`);
          searchResult.split('\n').forEach(location => {
            console.log(`      - ${location}`);
          });
          
          issues.push({
            mdFile: filePath,
            reference: diagramPath,
            expectedPath: resolvedPath,
            actualLocations: searchResult.split('\n')
          });
        } else {
          console.log(`   ⚠️  File not found anywhere!`);
          issues.push({
            mdFile: filePath,
            reference: diagramPath,
            expectedPath: resolvedPath,
            actualLocations: []
          });
        }
      }
    }
    
    if (issues.length > 0) {
      console.log('\n\n' + '=' .repeat(70));
      console.log(`⚠️  ${issues.length} BROKEN BPMN DIAGRAM REFERENCES`);
      console.log('=' .repeat(70) + '\n');
      
      for (const issue of issues) {
        console.log(`❌ ${issue.mdFile}`);
        console.log(`   Reference: ${issue.reference}`);
        console.log(`   Expected: ${issue.expectedPath}`);
        if (issue.actualLocations.length > 0) {
          console.log(`   Actual location(s):`);
          issue.actualLocations.forEach(loc => console.log(`     - ${loc}`));
        } else {
          console.log(`   ⚠️  File doesn't exist!`);
        }
        console.log('');
      }
      
      console.log('=' .repeat(70));
      console.log('RECOMMENDATIONS');
      console.log('=' .repeat(70) + '\n');
      
      console.log('Option 1: Move BPMN files back to docs/ (preferred for viewer)');
      console.log('  - BPMN viewer may expect files relative to markdown');
      console.log('  - Keep BPMN files alongside the docs that reference them\n');
      
      console.log('Option 2: Update markdown references to new locations');
      console.log('  - Change data-bpmn-diagram paths to point to static/img');
      console.log('  - May require absolute paths or viewer configuration\n');
      
      console.log('Option 3: Configure BPMN viewer to look in static/img');
      console.log('  - Update Docusaurus plugin configuration');
      console.log('  - Set base path for BPMN files\n');
    } else {
      console.log('\n\n' + '=' .repeat(70));
      console.log('✅ ALL BPMN DIAGRAM REFERENCES ARE WORKING!');
      console.log('=' .repeat(70) + '\n');
    }
    
  } catch (err) {
    if (err.status === 1 && err.stderr.includes('no matches found')) {
      console.log('✅ No BPMN diagram references found in markdown files\n');
    } else {
      console.error('Error:', err.message);
    }
  }
}

async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

findBpmnReferences();
