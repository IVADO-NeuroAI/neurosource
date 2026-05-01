import React from 'react';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import CatalogTable from '@site/src/components/CatalogTable';
import repositories from '@site/src/data/repositories.json';
import taxonomies from '@site/src/data/taxonomies.json';

function LinkCell(url) {
  if (!url) return '—';
  return (
    <a href={url} target="_blank" rel="noopener noreferrer">
      Link
    </a>
  );
}

const columns = [
  {field: 'repository_name', label: 'Repository'},
  {field: 'description', label: 'Description'},
  {field: 'modalities', label: 'Modalities'},
  {field: 'access_type', label: 'Access'},
  {field: 'num_datasets', label: 'Datasets'},
  {field: 'data_formats', label: 'Formats'},
  {field: 'url', label: 'URL', render: LinkCell},
];

const filters = [
  {field: 'modalities', label: 'Modality', options: taxonomies.modalities},
  {field: 'access_type', label: 'Access', options: taxonomies.access_types},
];

export default function RepositoriesPage() {
  return (
    <Layout title="Repositories" description="Catalog of data repositories">
      <div className="container margin-vert--lg">
        <Heading as="h1">Repositories</Heading>
        <p>Data hosting platforms for neural data.</p>
        <CatalogTable data={repositories} columns={columns} filters={filters} />
      </div>
    </Layout>
  );
}
