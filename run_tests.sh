#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python -m venv "${ROOT_DIR}/.venv-test"
source "${ROOT_DIR}/.venv-test/bin/activate"
pip install --upgrade pip
pip install -r "${ROOT_DIR}/backend/requirements.txt"

pytest "${ROOT_DIR}/backend/tests"

pushd "${ROOT_DIR}/frontend" > /dev/null
if [[ -f package-lock.json ]]; then
  npm ci
else
  npm install
fi
npm run build
popd > /dev/null

node "${ROOT_DIR}/frontend/tests/smoke.test.js"
