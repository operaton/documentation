/**
 * Remark plugin to transform data-bpmn-diagram tags to BpmnViewer React components
 * 
 * Handles MDX v2+ where <div> is parsed as JSX (mdxJsxFlowElement)
 * 
 * Transforms: <div data-bpmn-diagram="../bpmn/diagram"></div>
 * Into: <BpmnViewer diagramPath="/bpmn/.../diagram.bpmn" />
 */
import { visit } from 'unist-util-visit';
import path from 'path';

export default function remarkBpmnDiagram() {
  console.log('[remark-bpmn] Plugin loaded!');
  
  return (tree, file) => {
    const filePath = file.history?.[0] || 'unknown';
    console.log(`[remark-bpmn] Processing file: ${filePath}`);
    
    let transformCount = 0;
    
    visit(tree, (node) => {
      let bpmnPath = null;
      
      // Case 1: MDX JSX element (MDX v2+)
      if ((node.type === 'mdxJsxFlowElement' || node.type === 'mdxJsxTextElement') && 
          node.name === 'div') {
        
        const attr = node.attributes?.find(a => 
          a.type === 'mdxJsxAttribute' && a.name === 'data-bpmn-diagram'
        );
        
        if (attr && attr.value) {
          console.log(`[remark-bpmn] Found JSX div with data-bpmn-diagram: "${attr.value}"`);
          bpmnPath = processPath(attr.value, filePath);
        }
      }
      
      // Case 2: Raw HTML node (older MDX)
      if (node.type === 'html' && node.value?.includes('data-bpmn-diagram')) {
        const match = node.value.match(/data-bpmn-diagram\s*=\s*["']([^"']+)["']/i);
        if (match) {
          console.log(`[remark-bpmn] Found HTML with data-bpmn-diagram: "${match[1]}"`);
          bpmnPath = processPath(match[1], filePath);
        }
      }
      
      if (bpmnPath) {
        transformCount++;
        console.log(`[remark-bpmn] Transforming to: <BpmnViewer diagramPath="${bpmnPath}" />`);
        
        node.type = 'mdxJsxFlowElement';
        node.name = 'BpmnViewer';
        node.attributes = [
          {
            type: 'mdxJsxAttribute',
            name: 'diagramPath',
            value: bpmnPath
          }
        ];
        node.children = [];
      }
    });
    
    console.log(`[remark-bpmn] File complete. Transforms: ${transformCount}`);
  };
}

function processPath(relativePath, fullFilePath) {
  relativePath = relativePath.trim();
  
  // Skip external URLs
  if (relativePath.startsWith('http://') || relativePath.startsWith('https://')) {
    return null;
  }
  
  // Extract the path relative to docs/ from the full file path
  // Example: C:\Users\mail\Development\documentation\docs\documentation\reference\bpmn20\events\error-events.md
  // We want: documentation/reference/bpmn20/events/error-events.md
  
  let docRelativePath = '';
  
  // Handle both Windows and Unix paths
  const normalizedFilePath = fullFilePath.replace(/\\/g, '/');
  
  // Find the docs/ part
  const docsIndex = normalizedFilePath.indexOf('/docs/');
  if (docsIndex !== -1) {
    // Get everything after /docs/
    docRelativePath = normalizedFilePath.substring(docsIndex + 6); // +6 for '/docs/'
  } else {
    // Fallback: try to find just 'docs/'
    const altIndex = normalizedFilePath.indexOf('docs/');
    if (altIndex !== -1) {
      docRelativePath = normalizedFilePath.substring(altIndex + 5);
    }
  }
  
  console.log(`[remark-bpmn] Doc relative path: ${docRelativePath}`);
  
  // Get the directory of the markdown file (relative to docs/)
  const fileDir = path.posix.dirname(docRelativePath);
  console.log(`[remark-bpmn] File directory: ${fileDir}`);
  
  // Resolve the relative BPMN path against the file's directory
  // Example: fileDir = "documentation/reference/bpmn20/events"
  //          relativePath = "../bpmn/event-error"
  //          result should be = "documentation/reference/bpmn20/bpmn/event-error"
  
  let resolvedPath;
  if (relativePath.startsWith('/')) {
    // Absolute path (rare)
    resolvedPath = relativePath.substring(1);
  } else {
    // Relative path - join and normalize
    const joined = path.posix.join(fileDir, relativePath);
    resolvedPath = path.posix.normalize(joined);
  }
  
  console.log(`[remark-bpmn] Resolved path: ${resolvedPath}`);
  
  // Add .bpmn extension if not present
  if (!resolvedPath.endsWith('.bpmn')) {
    resolvedPath += '.bpmn';
  }
  
  // Clean up any leading ./
  if (resolvedPath.startsWith('./')) {
    resolvedPath = resolvedPath.substring(2);
  }
  
  const finalPath = `/bpmn/${resolvedPath}`;
  console.log(`[remark-bpmn] Final path: ${finalPath}`);
  
  return finalPath;
}