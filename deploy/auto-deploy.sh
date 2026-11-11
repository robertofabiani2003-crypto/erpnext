#!/bin/bash
set -Eeuo pipefail
umask 077
ROOT=/opt/erpnext
SOURCE=$ROOT/source
SITE=wms.admin-svoyo.shop
exec 9>$ROOT/auto-deploy.lock
flock -n 9 || exit 0
cd "$SOURCE"
test -z "$(git status --porcelain --untracked-files=normal)" || { echo 'Checkout has local changes; refusing deployment'; exit 1; }
git fetch origin refs/heads/develop:refs/remotes/origin/develop
TARGET=$(git rev-parse origin/develop)
CURRENT=$(cat "$ROOT/deployed-revision" 2>/dev/null || true)
[ "$TARGET" != "$CURRENT" ] || exit 0
[ "$TARGET" != "$(cat "$ROOT/failed-revision" 2>/dev/null || true)" ] || { echo "Deployment $TARGET previously failed; manual review required"; exit 1; }
git merge --ff-only "$TARGET"
# Existing Frappe base and Python dependencies stay pinned. Dependency upgrades require review.
if [ -n "$CURRENT" ]; then
  if ! git diff --quiet "$CURRENT" "$TARGET" -- pyproject.toml package.json yarn.lock; then
    echo 'Dependency changes require a reviewed base image update'; exit 1
  fi
fi
CONTEXT=$(mktemp -d "$ROOT/build-context.XXXXXX")
trap 'rm -rf -- "$CONTEXT"' EXIT
mkdir "$CONTEXT/app"
git archive "$TARGET" | tar -x -C "$CONTEXT/app"
IMAGE=local/erpnext-fork:$TARGET
docker build --label org.opencontainers.image.revision="$TARGET" --build-arg REVISION="$TARGET" -t "$IMAGE" -f deploy/Auto.Containerfile "$CONTEXT"
cat > "$CONTEXT/image.yaml" <<EOF
services:
  configurator: {image: $IMAGE}
  backend: {image: $IMAGE}
  frontend: {image: $IMAGE}
  websocket: {image: $IMAGE}
  queue-short: {image: $IMAGE}
  queue-long: {image: $IMAGE}
  scheduler: {image: $IMAGE}
EOF
cd "$ROOT"
compose() { docker compose -f "$ROOT/compose.yaml" -f "$ROOT/runtime-image.yaml" "$@"; }
if [ ! -f runtime-image.yaml ]; then printf 'services: {}\n' > runtime-image.yaml; fi
maintenance=0
failed() {
  echo "$TARGET" > "$ROOT/failed-revision"
  echo "Deployment failed at line $1. Maintenance=$maintenance; inspect journalctl -u erpnext-auto-deploy. Backups are in the sites volume."
}
trap 'failed $LINENO' ERR
compose exec -T backend bench --site "$SITE" set-maintenance-mode on
maintenance=1
compose stop scheduler queue-short queue-long
compose exec -T backend bench --site "$SITE" backup --with-files
cp runtime-image.yaml previous-image.yaml
cp "$CONTEXT/image.yaml" runtime-image.yaml
# Keep the old backend alive for backup until the new image is ready.
compose run --rm --no-deps backend bench --site "$SITE" migrate
compose up -d --no-deps --force-recreate configurator
compose up -d --no-deps --force-recreate backend frontend websocket queue-short queue-long scheduler
compose exec -T backend bench --site "$SITE" set-maintenance-mode off
maintenance=0
for attempt in $(seq 1 30); do
  if curl --fail --silent -H "Host: $SITE" http://127.0.0.1:18090/api/method/ping | grep -q pong; then
    printf '%s\n' "$TARGET" > "$ROOT/deployed-revision"
    rm -f "$ROOT/failed-revision"
    echo "Successfully deployed $TARGET"
    exit 0
  fi
  sleep 2
done
false
