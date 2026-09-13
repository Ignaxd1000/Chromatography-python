# Chromatography-python

## CLI usage

Run directory scan and store results in the database:

```bash
chroma --scan "directory"
```

Fetch and print all stored records:

```bash
chroma --fetch
```

Optional database override (useful for tests/headless workflows):

```bash
chroma --scan "directory" --db /path/to/chromatography.db
chroma --fetch --db /path/to/chromatography.db
```
