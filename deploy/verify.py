import json, pathlib, urllib.request, urllib.parse, http.cookiejar, sys
secret=json.loads(pathlib.Path('/opt/erpnext/secrets.json').read_text())
jar=http.cookiejar.CookieJar()
opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
base=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:18090'
data=urllib.parse.urlencode({'usr':secret.get('administrator_username','Administrator'),'pwd':secret['administrator_password']}).encode()
req=urllib.request.Request(base+'/api/method/login',data=data,headers={'Host':'wms.admin-svoyo.shop'})
with opener.open(req) as r:
    result=json.load(r)
assert result['message']=='Logged In', 'Login failed'
req=urllib.request.Request(base+'/api/method/frappe.auth.get_logged_user',headers={'Host':'wms.admin-svoyo.shop'})
with opener.open(req) as r:
    assert json.load(r)['message']=='Administrator'
print('Administrator login and authenticated session verified')
req=urllib.request.Request(base+'/api/method/ping',headers={'Host':'wms.admin-svoyo.shop'})
with opener.open(req) as r: assert json.load(r)['message']=='pong'
print('API ping verified')
