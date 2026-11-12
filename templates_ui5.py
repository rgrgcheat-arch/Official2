"""v13 templates: site background picture, simple Paytm setup (UPI ID + API token), product chips, no-balance popup."""
from templates_ui4 import TEMPLATES as T, ic  # noqa: F401


def sub(name, old, new):
    assert old in T[name], (name, old[:70])
    T[name] = T[name].replace(old, new, 1)


# ---- Admin > Logo & Theme: background picture
sub("admin_branding.html", """<div class=card><h3>{{ic('palette',20)}} Look &amp; sign-up</h3>""",
    """<div class=card><h3>{{ic('image',20)}} Background picture</h3>
<p class=mu>This picture is shown behind EVERY page: login, dashboard, key generator, admin ... PNG, JPG, WEBP or GIF, up to 12 MB. It is resized automatically. A tall (portrait) picture looks best on phones.</p>
{% if has_bg %}<div style="margin:12px 0;height:150px;border-radius:16px;border:1px solid var(--bd);background:#000 url(/bg?v={{range(1,10**9)|random}}) center/cover no-repeat"></div>{% endif %}
<form method=post enctype=multipart/form-data><input type=hidden name=action value=bg>
<input type=file name=bg accept="image/*" required style="width:100%">
<button class=g style="margin-top:12px">{{ic('plus')}} {{'Replace background' if has_bg else 'Add background'}}</button></form>
{% if has_bg %}<form method=post style="margin-top:12px"><input type=hidden name=action value=bg_dim>
<p class=mu>Picture darkness (so the text stays easy to read)</p>
<select name=dim style="width:100%"><option value=low {{'selected' if bg_dim=='low'}}>Light - picture very clear</option><option value=mid {{'selected' if bg_dim=='mid'}}>Medium</option><option value=high {{'selected' if bg_dim=='high'}}>Strong - best for reading</option></select>
<button class=g style="margin-top:10px">{{ic('save')}} Save</button></form>
<form method=post style="margin-top:10px" onsubmit="return confirm('Remove the background picture?')"><input type=hidden name=action value=bg_remove><button class=r>{{ic('trash',16)}} Remove background</button></form>{% endif %}</div>
<div class=card><h3>{{ic('palette',20)}} Look &amp; sign-up</h3>""")

# ---- Admin > Gateway: Paytm = UPI ID + API token only
a = T["admin_gateway.html"]
i = a.index("<div class=card><h3>Paytm gateway")
j = a.index("<div class=card><h3>Fampay gateway")
T["admin_gateway.html"] = a[:i] + """<div class=card><h3>Paytm gateway {% if active=='paytm' %}<span class="pill a">ON</span>{% endif %}</h3>
<form method=post><input type=hidden name=action value=save_zy>
<p class=mu>UPI ID (your receiving UPI ID)</p>
<input name=zy_upi value="{{zy_upi}}" placeholder="yourname@paytm" autocomplete=off style="width:100%">
<p class=mu>API Token (from your ZYVO PAY dashboard){% if zy_tail %} &mdash; saved (ends with <code>{{zy_tail}}</code>). Leave empty to keep it.{% endif %}</p>
<input name=zy_key type=password autocomplete=off placeholder="paste the full token" style="width:100%">
<button class=g style="margin-top:12px">{{ic('save')}} Save &amp; connect Paytm</button>
<p class=hint>Just these two. When you press the button a Rs.1 test QR is made automatically; if it works, Paytm turns ON by itself (Fampay turns OFF).</p>
<details style="margin-top:10px"><summary class=mu style="cursor:pointer">Advanced (optional)</summary>
<p class=mu>Webhook secret{% if zy_wh %} &mdash; saved. Leave empty to keep it.{% endif %} (not needed: payments are checked automatically every few seconds)</p><input name=zy_whsec type=password autocomplete=off style="width:100%">
<p class=mu>API URL</p><input name=zy_base value="{{zy_base}}" style="width:100%">
<p class=hint>Webhook URL (only if you want instant confirmation): <code>{{hook}}</code></p></details></form>
<form method=post style="margin-top:10px"><input type=hidden name=action value=test_zy><button {{'disabled' if not zy_ok}}>{{ic('qr')}} Generate Paytm test QR ({{CURRENCY}}1)</button></form></div>
""" + a[j:]
sub("admin_gateway.html", """{% if test.ok %}<div class="flash ok">QR created successfully. Order {{test.order}}</div>""",
    """{% if test.ok %}<div class="flash ok">{{test.note or 'QR created successfully.'}} Order {{test.order}}</div>""")

# ---- Generate page: product chips with logos + "no balance" popup
sub("generate.html", "<select id=sp></select>",
    "<select id=sp></select><div id=chips style=\"display:none;gap:8px;overflow-x:auto;padding:10px 0 2px;white-space:nowrap\"></div>")
sub("generate.html", "sp.onchange=()=>{fill();pic()};",
    "sp.onchange=()=>{fill();pic();chipOn()};")
sub("generate.html", " if(n>=10&&!confirm(",
    " const need=Math.round(x.price*n*100)/100;if(bal+0.0001<need){noBal(need);return}\n if(n>=10&&!confirm(")
sub("generate.html", "if(!j.ok){err=j.error;break}",
    "if(!j.ok){err=j.error;if(/insufficient/i.test(err||''))noBal(x.price);break}")
sub("generate.html", "fill();\n</script>{% endblock %}", """function chipOn(){document.querySelectorAll('#chips .chip').forEach(c=>{const on=c.dataset.i==sp.value;c.style.borderColor=on?'var(--ac)':'var(--bd)';c.style.boxShadow=on?'0 0 14px rgba(var(--acrgb),.45)':'none'})}
(function(){const box=$('chips');if(!C.some(p=>p.icon))return;box.style.display='flex';
 C.forEach((p,i)=>{const b=document.createElement('button');b.type='button';b.className='chip';b.dataset.i=i;
  b.style.cssText='display:inline-flex;align-items:center;gap:7px;flex:none;padding:7px 12px;border-radius:14px;background:transparent;border:1px solid var(--bd);color:var(--tx);box-shadow:none;font-size:13px';
  if(p.icon){const m=new Image();m.src=p.icon;m.style.cssText='width:22px;height:22px;border-radius:6px;object-fit:cover';m.onerror=()=>m.remove();b.appendChild(m)}
  b.appendChild(document.createTextNode(p.name));b.onclick=()=>{sp.value=i;sp.onchange()};box.appendChild(b)});chipOn()})();
function noBal(need){$('nbNeed').textContent=CU+(Math.round(need*100)/100);$('nbBal').textContent=CU+(Math.round(bal*100)/100);$('nbPop').style.display='flex'}
fill();
</script>
<div id=nbPop style="display:none;position:fixed;inset:0;z-index:99;background:rgba(0,0,0,.65);align-items:center;justify-content:center;padding:18px" onclick="if(event.target===this)this.style.display='none'">
<div style="width:100%;max-width:340px;border-radius:22px;background:var(--card);backdrop-filter:blur(14px);border:1px solid var(--bd);padding:22px;text-align:center;box-shadow:0 10px 40px rgba(0,0,0,.45)">
<div style="font-size:42px;line-height:1">&#9888;&#65039;</div>
<h3 style="margin:10px 0 6px">Not enough balance</h3>
<p class=mu style="margin:0 0 4px">Your account does not have enough balance for this purchase.</p>
<p style="margin:8px 0 16px;font-size:14px">Needed <b id=nbNeed></b> &middot; You have <b id=nbBal style="color:#f87171"></b></p>
<a class=btn href="/wallet" style="display:block;text-align:center;margin-bottom:8px">Add balance</a>
<button type=button class=o style="width:100%" onclick="document.getElementById('nbPop').style.display='none'">Close</button></div></div>{% endblock %}""")

TEMPLATES = T


# ---- v14: automatic 12-hour backup card
sub("admin_backup.html", "<div class=card><h3>Download Backup</h3>", """<div class=card><h3>{{ic('save',20)}} Auto Backup (every {{ab_hours}} hours)</h3>
<p class=mu>The panel makes a full backup by itself (users, products, plans, keys, stock, settings - no music) and <b>sends the file to your Telegram admin chat</b>. Keep the files you receive; the last 10 are also kept on the server.</p>
<p class=mu>Status: <b>{{ 'ON' if ab_on else 'OFF' }}</b>{% if ab_last %} &middot; last backup: <b>{{ab_last}}</b>{% endif %}{% if ab_status %} &middot; {{ab_status}}{% endif %}</p>
<form method=post action=\"/admin/backup/auto\" style=\"margin-top:10px\"><input type=hidden name=action value=save>
<label class=mu><input type=checkbox name=on value=1 {{'checked' if ab_on}}> Auto backup ON</label>
<p class=mu style=\"margin-top:8px\">Every <input type=number name=hours min=1 max=168 value=\"{{ab_hours}}\" style=\"width:80px\"> hours</p>
<button class=g style=\"margin-top:8px\">{{ic('save')}} Save</button></form>
<form method=post action=\"/admin/backup/auto\" style=\"margin-top:8px\"><input type=hidden name=action value=now><button class=btn>{{ic('download')}} Backup now &amp; send to Telegram</button></form>
{% if ab_files %}<p class=mu style=\"margin-top:12px\">Saved on server:</p>{% for f in ab_files %}<div><a href=\"/admin/backup/file/{{f}}\">{{f}}</a></div>{% endfor %}{% endif %}</div>
<div class=card><h3>Download Backup</h3>""")


# ---- v14: TAHIR API SYSTEM replaces the old Main API (token only)
for _k in list(T):
    if _k in ("admin_mapi.html", "admin_mapi_products.html"):
        continue
    T[_k] = T[_k].replace("Main API", "Tahir API System")
T["admin_mapi.html"] = """{% extends 'abase.html' %}{% block c %}{% set page2='c' %}<h2>{{ic('code',24)}} Tahir API System</h2><div style="display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 4px">
<a class=btn href="/admin/main-api" style="{{'' if page2=='c' else 'background:transparent;border:1px solid var(--bd);box-shadow:none'}}">{{ic('key',16)}}Connection</a>
<a class=btn href="/admin/main-api/products" style="{{'' if page2=='p' else 'background:transparent;border:1px solid var(--bd);box-shadow:none'}}">{{ic('box',16)}}All Products</a></div>
<div class=card><h3>{{ic('key',20)}} Connect</h3>
<p class=mu>Just paste your API token and press <b>Connect</b>. Nothing else is needed.</p>
<form method=post><input type=hidden name=action value=save>
<p class=mu>API Token{% if tail %} &mdash; saved (ends with <code>{{tail}}</code>). Leave empty to keep it.{% endif %}</p>
<input name=token type=password autocomplete=off placeholder="Paste your API token" style="width:100%" {{'' if tail else 'required'}}>
<button class=g style="margin-top:12px">{{ic('check')}} Connect</button></form></div>
<div class=card><h3>{{ic('wallet',20)}} Status &amp; Balance</h3>
{% if st %}{% if st.ok %}<span class="pill a">Connect successful</span>
<div style="font-size:30px;font-weight:800;color:#34d399;margin:8px 0 2px">{{st.balance|cur}}</div>
<div class=mu>USD {{'%g'|format(st.balance_usd or 0)}}</div>
{% else %}<span class="pill e">Not connected</span><div class=mu style="margin:8px 0">{{st.msg}}</div>{% endif %}
<div class=mu style="margin-top:6px">Last checked: {{st.ts|dt}}</div>
{% else %}<div class=mu>Not checked yet. Paste your token and press Connect.</div>{% endif %}
<form method=post style="margin-top:12px"><input type=hidden name=action value=check><button>{{ic('wallet')}} Check Balance</button></form></div>
{% if st and st.ok %}<a class=btn href="/admin/main-api/products">{{ic('box',16)}} Open All Products &rarr;</a>{% endif %}
{% endblock %}"""
T["admin_mapi_products.html"] = T["admin_mapi_products.html"].replace("Buying is done live from the main API.", "Buying is done live from the Tahir API. Cost = USD price x 30.").replace("Import ALL products from the main API?", "Import ALL products from the Tahir API?")
