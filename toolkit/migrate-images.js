#!/usr/bin/env node

/**
 * Docusaurus Image Migration Script
 * 
 * This script:
 * 1. Scans all markdown/mdx files for image references
 * 2. Identifies which sidebar section each file belongs to
 * 3. Reorganizes images into structured folders
 * 4. Updates all image references in markdown files
 * 5. Generates a report of changes
 */

const fs = require('fs').promises;
const path = require('path');

// Configuration
const CONFIG = {
  docsPath: './docs',
  staticPath: './static/img',
  backupPath: './backup-images',
  dryRun: false, // Set to true to see what would happen without making changes
  
  // Define your sidebar structure - images will be organized to match
  sidebarSections: {
    'get-started': ['docs/get-started'],
    'documentation': ['docs/documentation'],
    'security': ['docs/security']
  }
};

// Track all changes for reporting
const report = {
  filesScanned: 0,
  imagesFound: 0,
  imagesMoved: 0,
  filesUpdated: 0,
  errors: [],
  warnings: []
};

/**
 * Determine which sidebar section a file belongs to
 */
function getSidebarSection(filePath) {
  // Normalize path separators for cross-platform compatibility
  const normalizedPath = filePath.replace(/\\/g, '/');
  
  // Check if path contains any of the sidebar section names
  if (normalizedPath.includes('docs/get-started')) {
    return 'get-started';
  }
  if (normalizedPath.includes('docs/documentation')) {
    return 'documentation';
  }
  if (normalizedPath.includes('docs/security')) {
    return 'security';
  }
  
  return 'shared'; // Default for images not in a specific section
}

/**
 * Extract all image references from markdown content
 */
function extractImageReferences(content, filePath) {
  const images = [];
  
  // Match markdown image syntax: ![alt](path)
  const mdImageRegex = /!\[([^\]]*)\]\(([^)]+)\)/g;
  let match;
  
  while ((match = mdImageRegex.exec(content)) !== null) {
    images.push({
      fullMatch: match[0],
      alt: match[1],
      path: match[2],
      type: 'markdown'
    });
  }
  
  // Match HTML img tags: <img src="path" />
  const htmlImageRegex = /<img[^>]+src=["']([^"']+)["'][^>]*>/g;
  
  while ((match = htmlImageRegex.exec(content)) !== null) {
    images.push({
      fullMatch: match[0],
      path: match[1],
      type: 'html'
    });
  }
  
  // Match JSX/MDX imports: import ImageName from './image.png'
  const importRegex = /import\s+(\w+)\s+from\s+['"]([^'"]+\.(?:png|jpg|jpeg|gif|svg|webp))['"];?/g;
  
  while ((match = importRegex.exec(content)) !== null) {
    images.push({
      fullMatch: match[0],
      importName: match[1],
      path: match[2],
      type: 'import'
    });
  }
  
  return images;
}

/**
 * Resolve relative image path to absolute filesystem path
 */
function resolveImagePath(imagePath, mdFilePath) {
  // Already absolute path from /img/
  if (imagePath.startsWith('/img/')) {
    return path.join(CONFIG.staticPath, imagePath.replace('/img/', ''));
  }
  
  // Relative path with explicit ./  or ../
  if (imagePath.startsWith('./') || imagePath.startsWith('../')) {
    const mdDir = path.dirname(mdFilePath);
    return path.resolve(mdDir, imagePath);
  }
  
  // Relative path without ./ (e.g., "img/file.png")
  // This should be resolved relative to the markdown file's directory
  if (!path.isAbsolute(imagePath)) {
    const mdDir = path.dirname(mdFilePath);
    const resolvedPath = path.resolve(mdDir, imagePath);
    return resolvedPath;
  }
  
  // Check if it's in static folder (fallback)
  const staticPath = path.join(CONFIG.staticPath, imagePath);
  return staticPath;
}

/**
 * Generate new organized path for an image
 */
function getNewImagePath(oldPath, sidebarSection, mdFilePath) {
  const ext = path.extname(oldPath);
  const basename = path.basename(oldPath, ext);
  
  // Create a subfolder structure based on the doc's location within the section
  const normalizedMdPath = mdFilePath.replace(/\\/g, '/');
  
  // Extract the path after the sidebar section
  let subPath = '';
  if (sidebarSection !== 'shared') {
    const sectionPrefix = `docs/${sidebarSection}/`;
    const sectionIndex = normalizedMdPath.indexOf(sectionPrefix);
    
    if (sectionIndex !== -1) {
      const pathAfterSection = normalizedMdPath.substring(sectionIndex + sectionPrefix.length);
      const docParts = path.dirname(pathAfterSection).split('/').filter(p => p && p !== '.');
      subPath = docParts.join('/');
    }
  }
  
  // Build new path
  let newPath;
  if (subPath) {
    newPath = path.join(CONFIG.staticPath, sidebarSection, subPath, `${basename}${ext}`);
  } else {
    newPath = path.join(CONFIG.staticPath, sidebarSection, `${basename}${ext}`);
  }
  
  return newPath;
}

/**
 * Convert absolute filesystem path to docusaurus /img/ reference
 */
function getDocusaurusPath(absolutePath) {
  const relativePath = path.relative(CONFIG.staticPath, absolutePath);
  return '/img/' + relativePath.replace(/\\/g, '/');
}

/**
 * Check if file exists
 */
async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

/**
 * Ensure directory exists
 */
async function ensureDir(dirPath) {
  try {
    await fs.mkdir(dirPath, { recursive: true });
  } catch (err) {
    if (err.code !== 'EEXIST') throw err;
  }
}

/**
 * Recursively find all markdown files
 */
async function findMarkdownFiles(dir) {
  const files = [];
  
  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      
      if (entry.isDirectory()) {
        // Skip excluded directories
        if (entry.name.startsWith('_') || entry.name === 'node_modules') {
          continue;
        }
        files.push(...await findMarkdownFiles(fullPath));
      } else if (entry.isFile()) {
        // Skip excluded files
        if (entry.name.startsWith('_')) {
          continue;
        }
        if (entry.name.match(/\.(md|mdx)$/)) {
          files.push(fullPath);
        }
      }
    }
  } catch (err) {
    report.errors.push(`Error reading directory ${dir}: ${err.message}`);
  }
  
  return files;
}

/**
 * Process a single markdown file
 */
async function processMarkdownFile(filePath) {
  try {
    const content = await fs.readFile(filePath, 'utf8');
    const images = extractImageReferences(content, filePath);
    
    if (images.length === 0) {
      return { updated: false };
    }
    
    report.imagesFound += images.length;
    
    const sidebarSection = getSidebarSection(filePath);
    let updatedContent = content;
    const imageChanges = [];
    
    for (const image of images) {
      const oldAbsolutePath = resolveImagePath(image.path, filePath);
      
      // Check if image file exists
      if (!await fileExists(oldAbsolutePath)) {
        report.warnings.push(`Image not found: ${image.path} (referenced in ${filePath})`);
        continue;
      }
      
      // Generate new organized path
      const newAbsolutePath = getNewImagePath(oldAbsolutePath, sidebarSection, filePath);
      
      // Skip if already in correct location
      if (oldAbsolutePath === newAbsolutePath) {
        continue;
      }
      
      // Move image file
      if (!CONFIG.dryRun) {
        await ensureDir(path.dirname(newAbsolutePath));
        await fs.copyFile(oldAbsolutePath, newAbsolutePath);
        report.imagesMoved++;
      }
      
      // Update reference in content
      const newDocusaurusPath = getDocusaurusPath(newAbsolutePath);
      
      if (image.type === 'markdown') {
        const newReference = `![${image.alt}](${newDocusaurusPath})`;
        updatedContent = updatedContent.replace(image.fullMatch, newReference);
      } else if (image.type === 'html') {
        const newReference = image.fullMatch.replace(image.path, newDocusaurusPath);
        updatedContent = updatedContent.replace(image.fullMatch, newReference);
      } else if (image.type === 'import') {
        // For imports, keep as relative but update path
        const relativeNewPath = path.relative(path.dirname(filePath), newAbsolutePath);
        const newImport = `import ${image.importName} from '${relativeNewPath}';`;
        updatedContent = updatedContent.replace(image.fullMatch, newImport);
      }
      
      imageChanges.push({
        old: image.path,
        new: newDocusaurusPath
      });
    }
    
    // Write updated content
    if (updatedContent !== content && !CONFIG.dryRun) {
      await fs.writeFile(filePath, updatedContent, 'utf8');
      report.filesUpdated++;
    }
    
    return {
      updated: updatedContent !== content,
      changes: imageChanges
    };
    
  } catch (err) {
    report.errors.push(`Error processing ${filePath}: ${err.message}`);
    return { updated: false };
  }
}

/**
 * Create backup of static/img folder
 */
async function createBackup() {
  if (CONFIG.dryRun) return;
  
  try {
    console.log('Creating backup...');
    await ensureDir(CONFIG.backupPath);
    
    // Copy entire img directory
    const cpCommand = require('child_process').execSync;
    cpCommand(`cp -r "${CONFIG.staticPath}" "${CONFIG.backupPath}/"`);
    
    console.log(`✓ Backup created at ${CONFIG.backupPath}`);
  } catch (err) {
    console.error('Failed to create backup:', err.message);
    throw err;
  }
}

/**
 * Print final report
 */
function printReport() {
  console.log('\n' + '='.repeat(60));
  console.log('MIGRATION REPORT');
  console.log('='.repeat(60));
  console.log(`Mode: ${CONFIG.dryRun ? 'DRY RUN (no changes made)' : 'LIVE'}`);
  console.log(`Files scanned: ${report.filesScanned}`);
  console.log(`Images found: ${report.imagesFound}`);
  console.log(`Images moved: ${report.imagesMoved}`);
  console.log(`Files updated: ${report.filesUpdated}`);
  
  if (report.warnings.length > 0) {
    console.log(`\n⚠ Warnings: ${report.warnings.length}`);
    report.warnings.forEach(w => console.log(`  - ${w}`));
  }
  
  if (report.errors.length > 0) {
    console.log(`\n❌ Errors: ${report.errors.length}`);
    report.errors.forEach(e => console.log(`  - ${e}`));
  }
  
  console.log('='.repeat(60) + '\n');
}

/**
 * Main execution
 */
async function main() {
  console.log('🚀 Starting Docusaurus image migration...\n');
  
  // Validate paths exist
  try {
    await fs.access(CONFIG.docsPath);
    await fs.access(CONFIG.staticPath);
  } catch (err) {
    console.error('Error: Could not find docs or static/img directory');
    console.error('Please run this script from your Docusaurus project root');
    process.exit(1);
  }
  
  // Create backup before making changes
  if (!CONFIG.dryRun) {
    await createBackup();
  }
  
  // Find all markdown files
  console.log('Scanning for markdown files...');
  const mdFiles = await findMarkdownFiles(CONFIG.docsPath);
  console.log(`Found ${mdFiles.length} markdown files\n`);
  
  report.filesScanned = mdFiles.length;
  
  // Process each file
  console.log('Processing files...');
  for (const file of mdFiles) {
    const result = await processMarkdownFile(file);
    if (result.updated) {
      console.log(`✓ Updated: ${path.relative(CONFIG.docsPath, file)}`);
      if (result.changes.length > 0) {
        result.changes.forEach(c => {
          console.log(`    ${c.old} → ${c.new}`);
        });
      }
    }
  }
  
  // Print final report
  printReport();
  
  if (CONFIG.dryRun) {
    console.log('💡 This was a dry run. To apply changes, set dryRun: false in the script.\n');
  } else {
    console.log('✅ Migration complete!\n');
    console.log('Next steps:');
    console.log('1. Review the changes');
    console.log('2. Test your documentation locally');
    console.log('3. Remove old image files if everything looks good');
    console.log(`4. Backup is available at ${CONFIG.backupPath}\n`);
  }
}

// Run the script
main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
