import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Operaton Documentation',
  tagline: 'BPMN-Process Automation for Everyone',
  favicon: 'img/favicon.png',

  // Set the production url of your site here
  url: 'https://your-docusaurus-site.example.com',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'Operaton', // Usually your GitHub org/user name.
  projectName: 'Operaton', // Usually your repo name.

  onBrokenLinks: 'warn', //'throw',
  onBrokenMarkdownLinks: 'warn',//'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          exclude: ['docs/documentation/introduction/third-party-libraries/camunda-bpm-platform-license-book.md'],
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/operaton/documentation/blob/main/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/operaton-logo.svg',
    navbar: {
      title: 'Operaton',
      logo: {
        alt: 'Operaton Logo',
        src: 'img/operaton-logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'getStarted',
          position: 'left',
          label: 'Get started',
        },
        {
          type: 'docSidebar',
          sidebarId: 'documentation',
          position: 'left',
          label: 'Documentation',
        },
        {
          type: 'docSidebar',
          sidebarId: 'security',
          position: 'left',
          label: 'Security',
        },
        // {to: '/blog', label: 'Blog', position: 'left'},
        {
          href: 'https://github.com/operaton',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Get Started',
              to: '/docs/get-started',
            },
            {
              label: 'Documentation',
              to: '/docs/documentation',
            },
            {
              label: 'Security',
              to: '/docs/security',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Forum',
              href: 'https://forum.operaton.org',
            },
            {
              label: 'Slack',
              href: 'https://operaton.org/chat',
            },
            {
              label: 'LinkedIn',
              href: 'https://www.linkedin.com/company/operaton',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/operaton',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Operaton. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
