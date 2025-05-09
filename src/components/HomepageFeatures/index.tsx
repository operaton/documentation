import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Easy to Use',
    description: (
      <>
        Operaton as fork of Camunda 7 was designed from the ground up to be easily installed and used, helping you get your business processes up and running quickly.
      </>
    ),
  },
  {
    title: 'Developer Docs',
    description: (
      <>
        Welcome to the Operaton documentation. Here you'll find everything you need to install, configure, and start using Operaton.
      </>
    ),
  },
  {
    title: 'Java API',
    description: (
      <>
        Operaton provides a powerful and flexible Java API that allows developers to model, deploy, and manage business processes programmatically.
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
