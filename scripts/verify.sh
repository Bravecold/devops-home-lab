#!/usr/bin/env bash
set -euo pipefail
base_url="${1:-http://localhost:8088}"
printf 'Checking %s\n' "$base_url"
curl --fail --silent --show-error "$base_url/health" | grep -q alive
curl --fail --silent --show-error "$base_url/ready" | grep -q ready
curl --fail --silent --show-error "$base_url/metrics" | grep -q http_requests_total
printf 'All application checks passed.\n'

