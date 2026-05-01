// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'NeuroSource',
  tagline: 'A living, open catalogue of neural foundation models, datasets, and data repositories.',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://ghazalehran.github.io',
  baseUrl: '/neurosource/',

  organizationName: 'ghazalehran',
  projectName: 'neurosource',

  onBrokenLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: false,
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      colorMode: {
        respectPrefersColorScheme: true,
      },
      navbar: {
        title: 'NeuroSource',
        items: [
          {to: '/models', label: 'Models', position: 'left'},
          {to: '/datasets', label: 'Datasets', position: 'left'},
          {to: '/repositories', label: 'Repositories', position: 'left'},
          {
            href: 'https://github.com/ghazalehran/neurosource',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Catalog',
            items: [
              {label: 'Models', to: '/models'},
              {label: 'Datasets', to: '/datasets'},
              {label: 'Repositories', to: '/repositories'},
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/ghazalehran/neurosource',
              },
              {
                label: 'Contributing',
                href: 'https://github.com/ghazalehran/neurosource/blob/main/CONTRIBUTING.md',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} NeuroSource Contributors. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
