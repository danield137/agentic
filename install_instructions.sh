#!/usr/bin/env bash
#
# Links only this repo's instructions into the Copilot CLI home directory.
#
# For anyone who wants the personal instruction files without the skills.
# Accepts the same options as install.sh (--dry-run, --force).
#
set -euo pipefail

exec "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/install.sh" instructions "$@"
