---

title: 'JavaDoc'
sidebar_position: 15

---

import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export function JavaDocLink() {
    const { siteConfig } = useDocusaurusContext();

    return <a href={siteConfig.customFields.javaDocUrl}>here</a>
}

You can find the JavaDoc <JavaDocLink/>.