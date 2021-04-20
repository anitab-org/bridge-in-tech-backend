module.exports = {
  title: 'Bridge-In-Tech Backend',
  tagline: 'Documentation for Bridge-In-Tech backend',
  url: 'https://bit-backend-docs.surge.sh',
  baseUrl: '/',
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'AnitaB.org',
  projectName: 'bridge-in-tech-backend',
  themeConfig: {
    navbar: {
      title: 'Bridge-In-Tech Backend',
      hideOnScroll: true,
      logo: {
        alt: 'AnitaB.org logo',
        src: 'img/logo.png',
      },
      items: [
        {
          to: 'docs/',
          activeBasePath: 'docs',
          label: 'Docs',
          position: 'left',
        },
        {
          href:'https://www.anitab.org',
          label: 'AnitaB.org',
          position: 'right',
        },
        {
          href:'https://anitab-org.zulipchat.com/#narrow/stream/237630-bridge-in-tech',
          label: 'Zulip',
          position: 'right',
        },
        {
          href: 'https://github.com/anitab-org/bridge-in-tech-backend',
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
              label: 'Bridge-In-Tech-Web Docs',
              href: 'https://github.com/anitab-org/bridge-in-tech-web/wiki',
            }
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Zulip',
              href: 'https://anitab-org.zulipchat.com/#narrow/stream/237630-bridge-in-tech',
            },
            {
              label: 'Twitter',
              href: 'https://twitter.com/anitab_org',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/anitab-org/bridge-in-tech-backend',
            },
            {
              label: 'Blog',
              href:'https://medium.com/anitab-org-open-source'
            }
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} AnitaB.org`,
    },
  },
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl:
            'https://github.com/anitab-org/bridge-in-tech-backend/edit/develop/docs',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
};
