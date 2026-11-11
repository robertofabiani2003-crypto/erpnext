# Deployment handoff
Status: READY_FOR_LOCALIZATION

## Address and identity
- Public site: https://wms.admin-svoyo.shop/login
- Site: wms.admin-svoyo.shop
- Administrator account: Administrator
- Server: ssh svoyo-server (132.243.118.215), Ubuntu 24.04.5 LTS.
- ERPNext v16.54.0 from real fork https://github.com/robertofabiani2003-crypto/erpnext, commit 495380b59c8701629f25089bd3807e6ddf7f26c6.
- Frappe v16.56.0 from upstream frappe/frappe, commit 49789a1711d4dde2be9c6888efe35651465f4b64.
- Image: local/erpnext-fork:approved, sha256:3c66e250bea0734f7f645fa49fba03e25dc0f4791c99a2381b961bc55b876b59.
- This is a custom source build from the fork, not an upstream ERPNext runtime image. Build verifies both Git hashes before removing .git and stores SOURCE_PROVENANCE.txt inside /home/frappe/frappe-bench.
- bench list-apps reports UNVERSIONED because official image construction removes .git; versions and provenance above are independently checked.

## Server paths and isolation
- Root directory /opt/erpnext (root:root, mode 700).
- Compose /opt/erpnext/compose.yaml; project name erpnext.
- Containers: erpnext-db-1, erpnext-redis-cache-1, erpnext-redis-queue-1, erpnext-backend-1, erpnext-frontend-1, erpnext-websocket-1, erpnext-queue-short-1, erpnext-queue-long-1, erpnext-scheduler-1. erpnext-configurator-1 exits successfully after configuration.
- Persistent named volumes: erpnext_sites, erpnext_logs, erpnext_db-data, erpnext_redis-queue-data.
- Private project Docker network erpnext_default; DB/Redis have no host bindings. Frontend binds only 127.0.0.1:18090.
- Existing Caddy svoyo-caddy-1 has one added route wms.admin-svoyo.shop -> 127.0.0.1:18090 in /opt/svoyo/deploy/server/Caddyfile. Existing routes preserved. Config validated and hot-reloaded, no existing service stopped.
- Protected proxy backup: /opt/erpnext/Caddyfile.before-erpnext.
- DNS A wms.admin-svoyo.shop -> 132.243.118.215 added in REG.RU with explicit user authorization. Authoritative and Cloudflare DNS verified.
- Let's Encrypt HTTPS certificate issued, hostname verified; expires 2027-02-09, automatic renewal managed by existing Caddy.

## Credentials: never place values in reports or local handoff
- Protected server secret: /opt/erpnext/secrets.json (root:root 600). Keys: administrator_password, db_root_password.
- MariaDB root password file: /opt/erpnext/db-password (root:root 600), mounted as Docker secret.
- Read secrets only within an SSH-side script and pass directly to the request/process. Do not cat/print the file or put values in command output/chat/Git.
- /opt/erpnext/verify.py demonstrates authenticated HTTP checks by reading this file on the server without printing credentials.
- Site DB credentials and encryption key remain in the private sites volume's site_config.json. Never print or copy them to handoff.

## Safe access/check commands
Run after ssh svoyo-server:
```sh
cd /opt/erpnext
docker compose ps
python3 verify.py https://wms.admin-svoyo.shop
docker compose exec -T backend bench --site wms.admin-svoyo.shop list-apps </dev/null
docker compose exec -T backend bench doctor </dev/null
curl -s -o /dev/null -w '%{http_code}\n' https://wms.admin-svoyo.shop/login
```
For application commands:
```sh
cd /opt/erpnext
docker compose exec -T backend bench --site wms.admin-svoyo.shop <command> </dev/null
```
For scripts importing frappe directly: use working directory /home/frappe/frappe-bench/sites and the bench env Python. Set sites_path explicitly; run as frappe (uid1000). Avoid altering infra/DB/proxy from localization chat.
SSH-only fallback from local computer: ssh -L 18090:127.0.0.1:18090 svoyo-server, then http://127.0.0.1:18090/login (fixed site header).

## Verified
- Site created with ERPNext installed. ERPNext16.54.0 and Frappe16.56.0 confirmed by list-apps.
- Administrator login, cookie session and authenticated get_logged_user verified. API ping returns pong.
- HTTPS login HTTP200, certificate validation successful both on VPS and user's Windows computer.
- Engine.IO/WebSocket polling handshake HTTP200 through public HTTPS and local nginx.
- Scheduler enabled; bench doctor sees 2 workers with no inactive-scheduler warning.
- Actual queued test jobs completed in both short and long queues.
- Restarted only erpnext DB/Redis/app/worker/scheduler/frontend/websocket containers. Repeated HTTPS login, API, jobs and WebSocket checks passed; persistent site and DB survived.
- Websocket had one transient Redis DNS EAI_AGAIN during simultaneous project restart and recovered automatically. Current process listening, public handshake passes; no OOM kills.
- Restart policies unless-stopped for persistent services; Docker enabled at boot. Full VPS reboot intentionally not performed because other projects share the host.
- Initial bench backup --with-files completed; stored in sites/wms.admin-svoyo.shop/private/backups on persistent erpnext_sites. Log /opt/erpnext/initial-backup.log (protected). Restore not tested; off-server backup schedule not configured.
- All pre-existing SVOYO/Bormostats containers remain running/healthy. Existing domains HTTP statuses after proxy reload: admin 200, history200, positions200, stats307.
- Runtime currently below1GiB for ERPNext idle; host available RAM around3.4GiB and free disk32GiB after build. Services have explicit memory limits. Build container stopped after completion.

## Build reproducibility and limits
Official frappe_docker source /opt/erpnext/frappe_docker at adb65c3e6bea083095bb88dc45f589ab37ead072, unmodified.
Build inputs outside that repository: /opt/erpnext/Containerfile, apps.json, build.sh, build.log, base-digests.txt. apps.json points to fork tag v16.54.0, Frappe tag v16.56.0; exact hashes enforced during build.
Builder erpnext-builder is isolated, limit2CPUs/3GiBRAM; not global/default builder. Base images frappe/build:version-16 and frappe/base:version-16 (digests recorded in base-digests.txt); Python3.14.10/Node24.22.2. DB MariaDB11.8, Redis8.6-alpine. Image tag approved is local only, not pushed to registry.
No repository checkout/branch/remotes were changed by infrastructure chat.

## Ownership transfer
Infrastructure ready. Only localization chat should now modify ERPNext localization settings, setup wizard/company settings and test warehouse/business data. Infrastructure chat has not configured company, warehouses, Russian locale or sample transactions. Do not recreate site or reset DB. Apply setup to existing site through authenticated APIs/bench using protected credentials.
