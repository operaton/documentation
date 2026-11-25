/**
 * Docusaurus Plugin: Copy BPMN Files
 * 
 * Copies BPMN files from docs/ to the build output, making them accessible
 * at /bpmn/... URLs while keeping source files in docs/ for easy editing.
 * 
 * Installation:
 *   Add to docusaurus.config.ts plugins array:
 *   plugins: [
 *     './src/plugins/plugin-copy-bpmn',
 *   ],
 */

const path = require('path');
const fs = require('fs').promises;
const { glob } = require('glob');

async function copyFile(src, dest) {
  await fs.mkdir(path.dirname(dest), { recursive: true });
  await fs.copyFile(src, dest);
}

async function findBpmnFiles(dir) {
  try {
    // Use glob to find all .bpmn files
    const pattern = path.join(dir, '**/*.bpmn').replace(/\\/g, '/');
    const files = await glob(pattern, { nodir: true });
    return files;
  } catch (err) {
    console.error('[copy-bpmn] Error finding BPMN files:', err);
    return [];
  }
}

module.exports = function pluginCopyBpmn(context) {
  const docsDir = path.join(context.siteDir, 'docs');
  // Versioned docs live in versioned_docs/version-<x>/ and are served at /bpmn/version-<x>/
  const versionedDocsDir = path.join(context.siteDir, 'versioned_docs');
  const sourceDirs = [docsDir, versionedDocsDir];
  
  return {
    name: 'docusaurus-plugin-copy-bpmn',

    // Copy BPMN files after build
    async postBuild({ outDir }) {
      let copied = 0;
      for (const sourceDir of sourceDirs) {
        const bpmnFiles = await findBpmnFiles(sourceDir);

        for (const srcFile of bpmnFiles) {
          const relativePath = path.relative(sourceDir, srcFile);
          const destFile = path.join(outDir, 'bpmn', relativePath);

          try {
            await copyFile(srcFile, destFile);
            copied++;
          } catch (err) {
            console.error(`[copy-bpmn] Failed to copy ${relativePath}:`, err.message);
          }
        }
      }
      
      if (copied > 0) {
        console.log(`[copy-bpmn] Copied ${copied} BPMN files to /bpmn/`);
      }
    },

    // Configure webpack to serve BPMN files during development
    configureWebpack(config, isServer) {
      if (isServer) return {};
      
      return {
        devServer: {
          setupMiddlewares: (middlewares, devServer) => {
            // Serve BPMN files from docs/ and versioned_docs/ at /bpmn/ path during dev
            devServer.app.get('/bpmn/*', async (req, res, next) => {
              const requestedPath = req.path.replace('/bpmn/', '');

              for (const sourceDir of sourceDirs) {
                const filePath = path.join(sourceDir, requestedPath);
                try {
                  const stat = await fs.stat(filePath);
                  if (stat.isFile() && filePath.endsWith('.bpmn')) {
                    res.type('application/xml');
                    res.sendFile(filePath);
                    return;
                  }
                } catch (err) {
                  // File not found, try the next source directory
                }
              }
              next();
            });
            
            return middlewares;
          },
        },
      };
    },
  };
};
