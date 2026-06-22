#!/bin/bash
# publish-rollup.sh
# Run this when all 3 have confirmed the weekly rollup.
# Usage: ./scripts/publish-rollup.sh
# Reads pending-confirm.json, adds entries to changelog.json, deploys.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SITE_DIR="$(dirname "$SCRIPT_DIR")"
STATE_FILE="$SITE_DIR/state/pending-confirm.json"
CHANGELOG="$SITE_DIR/changelog.json"

echo "Reading pending rollup..."
PENDING=$(cat "$STATE_FILE")

# Check all 3 confirmed
ETHAN=$(echo "$PENDING" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['confirmations']['ethan'])")
ERIK=$(echo "$PENDING" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['confirmations']['erik'])")
RAYMOND=$(echo "$PENDING" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['confirmations']['raymond'])")

if [[ "$ETHAN" != "True" || "$ERIK" != "True" || "$RAYMOND" != "True" ]]; then
  echo "Not all confirmed yet:"
  echo "  Ethan: $ETHAN"
  echo "  Erik: $ERIK"
  echo "  Raymond: $RAYMOND"
  exit 1
fi

echo "All 3 confirmed. Adding to changelog..."

# Merge entries from pending into changelog.json
python3 << PYEOF
import json, sys

with open("$STATE_FILE") as f:
    pending = json.load(f)

with open("$CHANGELOG") as f:
    changelog = json.load(f)

new_entries = pending.get("entries", [])
if not new_entries:
    print("No entries to publish.")
    sys.exit(1)

changelog["entries"] = new_entries + changelog.get("entries", [])

with open("$CHANGELOG", "w") as f:
    json.dump(changelog, f, indent=2)

print(f"Added {len(new_entries)} entries to changelog.")
PYEOF

# Mark as published
python3 -c "
import json
with open('$STATE_FILE') as f: d = json.load(f)
d['published'] = True
with open('$STATE_FILE', 'w') as f: json.dump(d, f, indent=2)
"

# Git commit + push
cd "$SITE_DIR"
git add changelog.json state/pending-confirm.json
WEEK=$(python3 -c "import json; d=json.load(open('$STATE_FILE')); print(d.get('week',''))")
git commit -m "Changelog update: week $WEEK"
git push

# Deploy to Cloudflare Pages
echo "Deploying..."
CF_TOKEN=$(cat /Users/user/.openclaw/workspace/.secrets/credentials.md | grep -A2 "Cloudflare" | grep "API Token" | awk -F'`' '{print $2}')
CLOUDFLARE_API_TOKEN="$CF_TOKEN" CLOUDFLARE_ACCOUNT_ID="5be6c3f5708d2839c641541b0ce2530c" \
  npx wrangler pages deploy "$SITE_DIR" \
  --project-name abillionrobots \
  --branch main \
  --commit-message "Weekly changelog: $WEEK"

echo "Done. Site updated."
