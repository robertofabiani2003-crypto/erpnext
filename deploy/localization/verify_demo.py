"""Read-only acceptance checks for the dedicated TEST-RU demonstration."""
import json
import frappe
from erpnext.stock.report.stock_balance.stock_balance import execute

frappe.init(site='wms.admin-svoyo.shop',sites_path='/home/frappe/frappe-bench/sites')
frappe.connect()
frappe.set_user('Administrator')
try:
    settings = frappe.get_single('System Settings')
    expected_settings = dict(language='ru',time_zone='Europe/Moscow',date_format='dd.mm.yyyy',number_format='# ###,##',currency='RUB',currency_precision='2',first_day_of_the_week='Monday')
    for key, value in expected_settings.items():
        assert settings.get(key) == value, key
    assert settings.setup_complete == 1
    assert frappe.db.get_value('User','Administrator','language') == 'ru'
    assert frappe.db.get_value('User','Administrator','time_zone') == 'Europe/Moscow'
    expected = {('TEST-RU-COMP','TEST-RU Приёмка - TRU'):(4,400),('TEST-RU-COMP','TEST-RU Сборка - TRU'):(2,200),('TEST-RU-KIT','TEST-RU Сборка - TRU'):(2,400)}
    bins = frappe.get_all('Bin',filters={'item_code':['in',['TEST-RU-COMP','TEST-RU-KIT']]},fields=['item_code','warehouse','actual_qty','stock_value'])
    assert {(b.item_code,b.warehouse):(b.actual_qty,b.stock_value) for b in bins} == expected
    ledger = frappe.get_all('Stock Ledger Entry',filters={'item_code':['in',['TEST-RU-COMP','TEST-RU-KIT']],'is_cancelled':0},fields=['item_code','warehouse','actual_qty','stock_value_difference'])
    sums = {}
    for row in ledger:
        pair = (row.item_code,row.warehouse)
        qty, val = sums.get(pair,(0,0))
        sums[pair] = (qty+row.actual_qty,val+row.stock_value_difference)
    assert sums == expected
    report = execute(frappe._dict(company='TEST-RU Демонстрационная компания',from_date='2026-11-11',to_date='2026-11-11',item_code=['TEST-RU-COMP','TEST-RU-KIT']))[1]
    assert {(r['item_code'],r['warehouse']):(r['bal_qty'],r['bal_val']) for r in report} == expected
    docs = [frappe.get_doc('Stock Entry',name) for name in ['MAT-STE-2026-00001','MAT-STE-2026-00002','MAT-STE-2026-00003']]
    assert all(d.docstatus == 1 for d in docs)
    bom = frappe.get_doc('BOM','BOM-TEST-RU-KIT-001')
    assert bom.docstatus == 1 and bom.quantity == 1 and len(bom.items) == 1 and bom.items[0].qty == 2
    assert len(ledger) == 5
    assert frappe.db.count('Translation',{'language':'ru'}) == 18
    print(json.dumps({'result':'PASS','settings':expected_settings,'bins':bins,'ledger_rows':len(ledger),'documents':[{'name':d.name,'docstatus':d.docstatus,'purpose':d.purpose} for d in docs],'bom':bom.name,'translation_count':18},ensure_ascii=False,default=str))
finally:
    frappe.destroy()
