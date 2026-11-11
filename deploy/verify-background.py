import frappe, time, sys
frappe.init(site='wms.admin-svoyo.shop', sites_path='/home/frappe/frappe-bench/sites')
frappe.connect()
job=frappe.enqueue('frappe.utils.now', queue=sys.argv[1] if len(sys.argv)>1 else 'short', job_name='deployment-check', enqueue_after_commit=False)
for _ in range(30):
    status=job.get_status(refresh=True)
    if status=='finished':
        print('Background queue job finished successfully')
        break
    if status=='failed': raise RuntimeError('Background test job failed')
    time.sleep(1)
else: raise RuntimeError('Background job timed out')
assert frappe.utils.cint(frappe.db.get_single_value('System Settings','enable_scheduler')) or not frappe.conf.pause_scheduler
print('Scheduler configuration permits execution')
frappe.destroy()
