FROM local/erpnext-fork:approved
USER frappe
RUN rm -rf /home/frappe/frappe-bench/apps/erpnext && ln -s /home/frappe/frappe-bench/assets /home/frappe/frappe-bench/sites/assets
COPY --chown=frappe:frappe app/ /home/frappe/frappe-bench/apps/erpnext/
WORKDIR /home/frappe/frappe-bench
RUN /home/frappe/frappe-bench/env/bin/pip install --no-deps -e apps/erpnext && bench build --app erpnext && cp -a sites/assets/. assets/
ARG REVISION
RUN printf '%s\n' "$REVISION" > ERPNext_REVISION
