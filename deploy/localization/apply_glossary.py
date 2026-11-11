"""Apply a narrow warehouse glossary through Frappe's supported Translation DocType.
Run using bench env Python from sites directory; no secrets are read or printed.
"""
import json
import sys
import frappe

SITE = 'wms.admin-svoyo.shop'
GLOSSARY = {
    'Item': 'Товар',
    'Items': 'Товары',
    'Stock Entry': 'Складское движение',
    'Stock Entry Type': 'Тип складского движения',
    'Material Receipt': 'Поступление материалов',
    'Material Transfer': 'Перемещение материалов',
    'Source Warehouse': 'Склад-источник',
    'Target Warehouse': 'Склад назначения',
    'BOM': 'Спецификация',
    'Bill of Materials': 'Спецификация состава',
    'Posting Date': 'Дата проводки',
    'Posting Time': 'Время проводки',
    'Stock UOM': 'Складская единица измерения',
    'Produce Item per Operation': 'Выпускать изделие по каждой операции',
    'Tools': 'Инструменты',
    'Add attachment': 'Добавить вложение',
    'Last Edited By You': 'Последнее изменение выполнено вами',
    'All apps': 'Все приложения',
}

def main():
    site = sys.argv[1] if len(sys.argv) > 1 else SITE
    if site != SITE:
        raise SystemExit('Refusing to modify a different site; review the explicit site allowlist first.')
    frappe.init(site=site, sites_path='/home/frappe/frappe-bench/sites')
    frappe.connect()
    frappe.set_user('Administrator')
    changed = []
    try:
        for source, target in GLOSSARY.items():
            rows = frappe.get_all('Translation', filters={'language': 'ru', 'source_text': source}, fields=['name','context','translated_text'])
            rows = [r for r in rows if not r.context]
            if rows:
                if len(rows) != 1 or rows[0].translated_text != target:
                    raise RuntimeError(f'Preserving conflicting existing translation for {source!r}')
                continue
            doc = frappe.get_doc({'doctype':'Translation','language':'ru','source_text':source,'translated_text':target})
            doc.insert()
            changed.append({'name':doc.name,'source_text':source,'translated_text':target})
        frappe.db.commit()
        frappe.clear_cache()
        from frappe.translate import get_all_translations
        merged = get_all_translations('ru')
        for source, target in GLOSSARY.items():
            assert merged.get(source) == target, source
        print(json.dumps({'site':site,'created':changed,'verified':len(GLOSSARY)},ensure_ascii=False))
    except Exception:
        frappe.db.rollback()
        raise
    finally:
        frappe.destroy()

if __name__ == '__main__':
    main()
