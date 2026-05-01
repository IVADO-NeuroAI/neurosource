import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link className="button button--secondary button--lg" to="/models">
            Browse the Catalog
          </Link>
        </div>
      </div>
    </header>
  );
}

const features = [
  {
    title: 'Models',
    description: 'Neural foundation models and baselines for EEG, fMRI, ECoG, and more.',
    link: '/models',
  },
  {
    title: 'Datasets',
    description: 'Curated neural datasets with metadata on modality, species, and access.',
    link: '/datasets',
  },
  {
    title: 'Repositories',
    description: 'Data hosting platforms like OpenNeuro, DANDI, and PhysioNet.',
    link: '/repositories',
  },
];

function Feature({title, description, link}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center padding-horiz--md padding-vert--lg">
        <Heading as="h3">
          <Link to={link}>{title}</Link>
        </Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title="Home"
      description="A living, open catalogue of neural foundation models, datasets, and data repositories.">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              {features.map((props, idx) => (
                <Feature key={idx} {...props} />
              ))}
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
