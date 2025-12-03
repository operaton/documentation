/**
 * Custom MDX Components
 * 
 * This file extends Docusaurus's default MDX components with custom components
 * that can be used directly in markdown files.
 * 
 * @see https://docusaurus.io/docs/markdown-features/react#mdx-component-scope
 */
import React from 'react';
import MDXComponents from '@theme-original/MDXComponents';
import BpmnViewer from '@site/src/components/BpmnViewer';

export default {
  // Spread the default components
  ...MDXComponents,
  
  // Add custom components that can be used in any MDX file without importing
  BpmnViewer,
  
  // You can also add aliases for convenience
  // 'bpmn-viewer': BpmnViewer,
};
