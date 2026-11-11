#!/bin/bash
set -euo pipefail
cd /opt/erpnext
nice -n 10 docker buildx build --builder erpnext-builder --load --progress plain --build-arg FRAPPE_BRANCH=v16.56.0 --secret id=apps_json,src=apps.json --label org.opencontainers.image.source=https://github.com/robertofabiani2003-crypto/erpnext --label org.opencontainers.image.revision=495380b59c8701629f25089bd3807e6ddf7f26c6 --tag local/erpnext-fork:approved --file Containerfile frappe_docker
