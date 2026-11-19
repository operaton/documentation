/**
 * Custom MDX Components
 * 
 * This file extends Docusaurus's default MDX components with custom components
 * that can be used directly in markdown files.
 * 
 * @see https://docusaurus.io/docs/markdown-features/react#mdx-component-scope
 */
import BpmnViewer from '@site/src/components/BpmnViewer';
import RestRef from '@site/src/components/RestRef';
import MDXComponents from '@theme-original/MDXComponents';

export default {
  // Spread the default components
  ...MDXComponents,

  // Add custom components that can be used in any MDX file without importing
  BpmnViewer,
  RestRef,

  // You can also add aliases for convenience
  // 'bpmn-viewer': BpmnViewer,
};
