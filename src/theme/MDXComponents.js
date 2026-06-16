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
import useBrokenLinks from '@docusaurus/useBrokenLinks';
import {useAnchorTargetClassName} from '@docusaurus/theme-common';
import clsx from 'clsx';
import BpmnViewer from '@site/src/components/BpmnViewer';

function AnchorAwareElement({as: Component, id, className, ...props}) {
  const brokenLinks = useBrokenLinks();
  const anchorTargetClassName = useAnchorTargetClassName(id);

  if (id) {
    brokenLinks.collectAnchor(id);
  }

  return (
    <Component
      id={id}
      className={clsx(anchorTargetClassName, className)}
      {...props}
    />
  );
}

function RegisterAnchors({ids = []}) {
  const brokenLinks = useBrokenLinks();

  ids.forEach((id) => brokenLinks.collectAnchor(id));

  return null;
}

export default {
  // Spread the default components
  ...MDXComponents,
  
  // Add custom components that can be used in any MDX file without importing
  BpmnViewer,
  RegisterAnchors,
  tr: (props) => <AnchorAwareElement as="tr" {...props} />,
  td: (props) => <AnchorAwareElement as="td" {...props} />,
  th: (props) => <AnchorAwareElement as="th" {...props} />,
  
  // You can also add aliases for convenience
  // 'bpmn-viewer': BpmnViewer,
};
