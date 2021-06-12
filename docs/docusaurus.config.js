module.exports = {
  title: 'Bridge-In-Tech Backend',
  tagline: 'Documentation for Bridge-In-Tech backend',
  url: 'https://anitab-org.github.io',
  baseUrl: '/bridge-in-tech-backend/',
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'AnitaB.org',
  projectName: 'bridge-in-tech-backend',
  themeConfig: {
     announcementBar: {
      id: 'support_us',
      content:
        '⭐️ If you like Bridge-In-Tech-Backend, give it a star on <a href="https://github.com/anitab-org/bridge-in-tech-backend" rel="noopener noreferrer" target="_blank">GitHub!</a> ⭐️',
      backgroundColor: '#fafbfc',
      textColor: '#091E42',
    },
    colorMode: {
      defaultMode: "light",
    },
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
      copyright: `
        <div>
            <a href="https://www.facebook.com/AnitaB.0rg/" rel="noopener noreferrer" target="_blank"><i id="social-fb" class="fa fa-facebook-square fa-3x social"></i></a>
            <a href="https://twitter.com/anitab_org" rel="noopener noreferrer" target="_blank"><i id="social-tw" class="fa fa-twitter-square fa-3x social"></i></a>
            <a href="https://www.linkedin.com/company/anitab-org/" rel="noopener noreferrer" target="_blank"><i id="fa fa-linkedin-square fa-3x social" class="fa fa-linkedin-square fa-3x social"></i></a>
            <a href="https://www.instagram.com/anitab_org/" rel="noopener noreferrer" target="_blank"><i id="fa fa-instagram-square fa-2x social" class="fa fa-instagram fa-3x social"></i></a>
        </div>
        <b>Copyright © ${new Date().getFullYear()} AnitaB.org</b>
        <link href="//maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css" rel="stylesheet">
      `,
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
