import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function RestRef({ text, tag, operation }) {
  const { siteConfig } = useDocusaurusContext();
  const restApiDocSiteUrl =  siteConfig.customFields.restApiDocSiteUrl || "";
  const restApiDocBasePath =  siteConfig.customFields.restApiDocBasePath || "/";

  if (!text) {
    // Will fail loudly.
    throw new Error('RestRef: "text" is required');
  }

  if (!tag && operation) {
    // Will fail loudly.
    throw new Error('RestRef: "tag" is required when "operation" is provided');
  }

  const href = buildHref({ restApiDocSiteUrl, restApiDocBasePath, tag, operation });

  return (
    <a target="_blank" rel="noreferrer" href={href}>{text}</a>
  );
}

function buildHref({ restApiDocSiteUrl, restApiDocBasePath, tag, operation }) {
  const siteUrl = stripTrailingSlashes(restApiDocSiteUrl);
  const basePath = stripLeadingSlashes(restApiDocBasePath);
  const hrefBase = stripTrailingSlashes(`${siteUrl}/${basePath}`);

  if (!tag) {
    return hrefBase;
  }

  if (!operation) {
    return `${hrefBase}/#tag/${tag}`;
  }

  return `${hrefBase}/#tag/${tag}/operation/${operation}`;
}

function stripTrailingSlashes(input) {
  return input.replace(/\/+$/, "");
}

function stripLeadingSlashes(input) {
  return input.replace(/^\/+/, "");
}
