import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function RestRef({ text, section, tag, operation, page }) {
  const { siteConfig } = useDocusaurusContext();
  const hrefBase = siteConfig.customFields.restApiDocUrl;
  const restTag = tag ?? section;
  const restOperation = operation ?? page;
  
  if (!hrefBase) {
    // Will fail loudly.
    throw new Error('RestRef: "restApiDocUrl" is missing from customFields in "docusaurus.config.js"');
  }

  if (!text) {
    // Will fail loudly.
    throw new Error('RestRef: "text" is required');
  }

  if (!restTag && restOperation) {
    // Will fail loudly.
    throw new Error('RestRef: "tag" or "section" is required when "operation" or "page" is provided');
  }

  const href = buildHref({ hrefBase, tag: restTag, operation: restOperation });
  
  return (
    <a target="_blank" rel="noreferrer" href={href}>{text}</a>
  );
}

function buildHref({ hrefBase, tag, operation }) {
  if (!tag) {
    return hrefBase;
  }

  if (!operation) {
    return `${hrefBase}/#tag/${tag}`;
  }

  return `${hrefBase}/#tag/${tag}/operation/${operation}`;
}
