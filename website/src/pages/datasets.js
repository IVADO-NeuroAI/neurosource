import React from 'react';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import CatalogTable from '@site/src/components/CatalogTable';
import datasets from '@site/src/data/datasets.json';
import taxonomies from '@site/src/data/taxonomies.json';

function LinkCell(url) {
  if (!url) return '—';
  return (
    <a href={url} target="_blank" rel="noopener noreferrer">
      Link
    </a>
  );
}

function DatasetNameCell(name, entry) {
  if (!name) return '—';
  if (!entry?.url) return name;
  return (
    <a href={entry.url} target="_blank" rel="noopener noreferrer">
      {name}
    </a>
  );
}

const columns = [
  {field: 'dataset_name', label: 'Dataset', render: DatasetNameCell},
  {field: 'modalities', label: 'Modalities'},
  {field: 'species', label: 'Species'},
  {field: 'recording_task', label: 'Recording Task'},
  {field: 'access_type', label: 'Access'},
  {field: 'num_subjects', label: 'Subjects'},
  {field: 'year', label: 'Year'},
  {field: 'repository', label: 'Repository'},
  {field: 'license', label: 'License'},
  {field: 'paper_url', label: 'Paper', render: LinkCell},
];

const filters = [
  {field: 'modalities', label: 'Modality', options: taxonomies.modalities},
  {field: 'species', label: 'Species', options: taxonomies.species},
  {field: 'recording_task', label: 'Recording Task', options: taxonomies.recording_tasks},
  {field: 'access_type', label: 'Access', options: taxonomies.access_types},
];

export default function DatasetsPage() {
  return (
    <Layout title="Datasets" description="Catalog of neural datasets">
      <div className="container margin-vert--lg">
        <Heading as="h1">Datasets</Heading>
        <p>Curated neural datasets with metadata on modality, species, and access.</p>
        <CatalogTable data={datasets} columns={columns} filters={filters} />
      </div>
    </Layout>
  );
}
