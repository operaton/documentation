---

title: 'REST API specification'
sidebar_position: 20

---

import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export function RestApiDocLink() {
    const { siteConfig } = useDocusaurusContext();

    return <a href={siteConfig.customFields.restApiDocUrl}>here</a>
}

You can find the RestApi Specification <RestApiDocLink/>.