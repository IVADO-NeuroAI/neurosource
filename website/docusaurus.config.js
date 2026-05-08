// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'NeuroSource',
  tagline: 'A living, open catalogue of neural foundation models, datasets, and data repositories.',
  favicon: 'img/ivado_R1_logo.png',

  future: {
    v4: true,
  },

  url: 'https://ivado-neuroai.github.io',
  baseUrl: '/neurosource/',

  organizationName: 'IVADO-NeuroAI',
  projectName: 'neurosource',

  onBrokenLinks: 'throw',
  // onBrokenMarkdownLinks: "warn",

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
        logo: {
          alt: 'IVADO logo',
          src: 'img/ivado_logo.png',
          href: '/',
        },
        items: [
          {to: '/models', label: 'Models', position: 'left'},
          {to: '/datasets', label: 'Datasets', position: 'left'},
          {to: '/repositories', label: 'Repositories', position: 'left'},
        ],
      },
      footer: {
        style: 'dark',
        logo: {
          alt: 'IVADO logo',
          src: 'img/ivado_logo.png',
        },
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
                href: 'https://github.com/IVADO-NeuroAI/neurosource',
              },
              {
                label: 'Contributing',
                href: 'https://github.com/IVADO-NeuroAI/neurosource/blob/main/CONTRIBUTING.md',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} NeuroSource Contributors.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
