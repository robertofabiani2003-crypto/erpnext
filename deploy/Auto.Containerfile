FROM local/erpnext-fork:approved
USER frappe
RUN mv /home/frappe/frappe-bench/apps/erpnext/node_modules /tmp/erpnext-node_modules && rm -rf /home/frappe/frappe-bench/apps/erpnext && ln -s /home/frappe/frappe-bench/assets /home/frappe/frappe-bench/sites/assets
COPY --chown=frappe:frappe app/ /home/frappe/frappe-bench/apps/erpnext/
WORKDIR /home/frappe/frappe-bench
RUN mv /tmp/erpnext-node_modules apps/erpnext/node_modules && /home/frappe/frappe-bench/env/bin/pip install --no-deps -e apps/erpnext && bench build --app erpnext
ARG REVISION
RUN printf '%s\n' "$REVISION" > ERPNext_REVISION
