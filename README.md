# abillionrobots.com

Living changelog for the "Towards 1B Robots" thesis by Ethan Aldrich, Erikson Kuebler, and Raymond Xu.

## Structure

- `index.html` — landing page
- `updates/index.html` — changelog timeline (main page)
- `changelog.json` — data source for entries

## Adding entries

Entries in `changelog.json` follow this schema:

```json
{
  "entries": [
    {
      "date": "2026-06-22",
      "author": "Ethan",
      "body": "Your insight here.",
      "badge": "v1.1"   // optional — omit if not a version bump
    }
  ]
}
```

Entries are sorted newest-first automatically.

## Deployment

Deployed via Cloudflare Pages. Push to `main` → auto-deploys.
