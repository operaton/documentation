import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function RestRef({ text, section, operation }) {
  const { siteConfig } = useDocusaurusContext();
  const hrefBase = siteConfig.customFields.restApiDocUrl;
  
  if (!hrefBase) {
    // Will fail loudly.
    throw new Error('RestRef: "restApiDocUrl" is missing from customFields in "docusaurus.config.js"');
  }

  if (!text) {
    // Will fail loudly.
    throw new Error('RestRef: "text" is required');
  }

  if (!section && operation) {
    // Will fail loudly.
    throw new Error('RestRef: "section" is required when "operation" is provided');
  }

  const href = buildHref({ hrefBase, section, operation });
  
  return (
    <a target="_blank" href={href}>{text}</a>
  );
}

function buildHref({hrefBase, section, operation}) {
  if (!section) {
    return hrefBase;
  }

  if (!operation) {
    return `${hrefBase}/#tag/${section}`;
  }

  return `${hrefBase}/#tag/${section}/operation/${operation}`;
}
