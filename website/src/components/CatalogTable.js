import React, {useState, useMemo} from 'react';
import styles from './CatalogTable.module.css';

function FilterDropdown({label, value, options, onChange}) {
  return (
    <div className={styles.filterGroup}>
      <label className={styles.filterLabel}>{label}</label>
      <select
        className={styles.filterSelect}
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        <option value="">All</option>
        {options.map((opt) => (
          <option key={opt} value={opt}>
            {opt}
          </option>
        ))}
      </select>
    </div>
  );
}

export default function CatalogTable({data, columns, filters}) {
  const [activeFilters, setActiveFilters] = useState(
    Object.fromEntries(filters.map((f) => [f.field, '']))
  );
  const [searchQuery, setSearchQuery] = useState('');

  const filteredData = useMemo(() => {
    return data.filter((entry) => {
      for (const filter of filters) {
        const filterValue = activeFilters[filter.field];
        if (!filterValue) continue;
        const entryValue = entry[filter.field];
        if (Array.isArray(entryValue)) {
          if (!entryValue.includes(filterValue)) return false;
        } else {
          if (entryValue !== filterValue) return false;
        }
      }
      if (searchQuery) {
        const query = searchQuery.toLowerCase();
        const searchable = columns
          .map((col) => {
            const val = entry[col.field];
            return Array.isArray(val) ? val.join(' ') : String(val ?? '');
          })
          .join(' ')
          .toLowerCase();
        if (!searchable.includes(query)) return false;
      }
      return true;
    });
  }, [data, activeFilters, searchQuery, columns, filters]);

  const updateFilter = (field, value) => {
    setActiveFilters((prev) => ({...prev, [field]: value}));
  };

  return (
    <div>
      <div className={styles.toolbar}>
        <input
          type="text"
          className={styles.searchInput}
          placeholder="Search..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <div className={styles.filters}>
          {filters.map((filter) => (
            <FilterDropdown
              key={filter.field}
              label={filter.label}
              value={activeFilters[filter.field]}
              options={filter.options}
              onChange={(value) => updateFilter(filter.field, value)}
            />
          ))}
        </div>
      </div>
      <div className={styles.resultCount}>
        {filteredData.length} of {data.length} entries
      </div>
      <div className={styles.tableWrapper}>
        <table className={styles.table}>
          <thead>
            <tr>
              {columns.map((col) => (
                <th key={col.field}>{col.label}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filteredData.map((entry, idx) => (
              <tr key={idx}>
                {columns.map((col) => (
                  <td key={col.field}>
                    {col.render
                      ? col.render(entry[col.field], entry)
                      : renderValue(entry[col.field])}
                  </td>
                ))}
              </tr>
            ))}
            {filteredData.length === 0 && (
              <tr>
                <td colSpan={columns.length} className={styles.emptyRow}>
                  No entries match the current filters.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function renderValue(value) {
  if (value == null) return '—';
  if (typeof value === 'boolean') return value ? 'Yes' : 'No';
  if (Array.isArray(value)) return value.join(', ');
  return String(value);
}
