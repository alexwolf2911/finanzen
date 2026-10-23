"""Baut aus template.html die iPhone-Web-App (index.html): Sperrbildschirm, Entschlüsselung, PWA."""
import sys
src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b):
    global s
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)

rep('<meta name="viewport" content="width=device-width, initial-scale=1">',
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    '<meta name="apple-mobile-web-app-capable" content="yes">\n'
    '<meta name="mobile-web-app-capable" content="yes">\n'
    '<meta name="apple-mobile-web-app-status-bar-style" content="default">\n'
    '<meta name="apple-mobile-web-app-title" content="Finanzen">\n'
    '<meta name="robots" content="noindex,nofollow">\n'
    '<meta name="theme-color" content="#f4f6fa" media="(prefers-color-scheme: light)">\n'
    '<meta name="theme-color" content="#0f141d" media="(prefers-color-scheme: dark)">\n'
    '<link rel="manifest" href="manifest.webmanifest">\n'
    '<link rel="apple-touch-icon" href="icon-180.png">\n'
    '<link rel="icon" href="icon-192.png">')
rep('<title>Finanzübersicht</title>', '<title>Finanzen</title>')

# Sicherheitsbereich (Notch) und Sperrbildschirm
rep('footer{color:var(--muted)',
    '.wrap{padding-top:max(20px,env(safe-area-inset-top));padding-bottom:max(56px,env(safe-area-inset-bottom))}\n'
    '#importBtn{display:none}\n'
    '#lock{position:fixed;inset:0;z-index:50;background:var(--bg);display:flex;align-items:center;justify-content:center;padding:24px 16px}\n'
    '#lock[hidden]{display:none}\n'
    '#lock .box{width:min(100%,360px);background:var(--card);border-radius:20px;padding:24px 20px;box-shadow:var(--shadow);text-align:center}\n'
    '#lock .logo{width:64px;height:64px;border-radius:16px;margin:0 auto 12px;display:block}\n'
    '#lock h1{font-size:1.3rem;margin:0 0 4px}\n'
    '#lock p{color:var(--muted);font-size:.86rem;margin:0 0 16px}\n'
    '#lock input[type=password],#lock input[type=text]{width:100%;border:1px solid var(--line);background:var(--bg);color:var(--text);border-radius:12px;padding:12px;font-size:1rem}\n'
    '#lock .user{position:absolute;left:-9999px;width:1px;height:1px;opacity:0}\n'
    '#lock label.chk{display:flex;align-items:center;gap:8px;justify-content:center;font-size:.85rem;color:var(--muted);margin:12px 0}\n'
    '#lock .go{width:100%;background:var(--accent);border-color:var(--accent);color:#fff;font-size:.95rem;padding:12px}\n'
    '#lock .err{color:var(--bad);font-size:.85rem;min-height:1.2em;margin-top:10px}\n'
    '.lockbar{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin-top:8px}\n'
    'footer{color:var(--muted)')

rep('<body>\n<div class="wrap" id="app">',
    '<body>\n'
    '<div id="lock"><form class="box" id="lockForm" autocomplete="on">\n'
    '  <img class="logo" src="icon-180.png" alt="">\n'
    '  <h1>Finanzen</h1>\n'
    '  <p id="lockInfo">Gib dein App-Passwort ein. Die Daten werden erst hier auf dem iPhone entschlüsselt.</p>\n'
    '  <input class="user" type="text" name="username" autocomplete="username" value="alex" tabindex="-1" aria-hidden="true">\n'
    '  <input type="password" id="pw" name="password" autocomplete="current-password" placeholder="App-Passwort" required>\n'
    '  <label class="chk"><input type="checkbox" id="remember" checked> Auf diesem Gerät angemeldet bleiben</label>\n'
    '  <button class="btn go" id="unlockBtn" type="submit">Entsperren</button>\n'
    '  <div class="err" id="lockErr" role="alert"></div>\n'
    '</form></div>\n'
    '<div class="wrap" id="app" hidden>')

rep('<button class="btn" id="hideBtn" type="button">Beträge ausblenden</button>',
    '<button class="btn" id="hideBtn" type="button">Beträge ausblenden</button>\n'
    '      <button class="btn" id="logoutBtn" type="button">Sperren</button>')

rep('<footer>Alle Daten stehen nur in dieser Datei und in deinem Browser. Nichts wird hochgeladen.</footer>',
    '<footer id="foot">Die Daten liegen verschlüsselt im Netz und werden nur auf diesem Gerät entschlüsselt.</footer>')

rep('const RAW=/*RAWDATA*/[];\nconst BALANCES=/*BALANCES*/{};', 'let RAW=[];\nlet BALANCES={};')

rep('renderCatSel();\nrenderAll();\n</script>', r'''// ---------- Entsperren & Laden ----------
const DB="fin_app",STORE="k";
function idb(){ return new Promise((res,rej)=>{ const r=indexedDB.open(DB,1); r.onupgradeneeded=()=>r.result.createObjectStore(STORE); r.onsuccess=()=>res(r.result); r.onerror=()=>rej(r.error); }); }
async function keyGet(){ try{ const d=await idb(); return await new Promise(res=>{ const q=d.transaction(STORE).objectStore(STORE).get("key"); q.onsuccess=()=>res(q.result||null); q.onerror=()=>res(null); }); }catch(e){ return null; } }
async function keySet(k){ try{ const d=await idb(); d.transaction(STORE,"readwrite").objectStore(STORE).put(k,"key"); }catch(e){} }
async function keyDel(){ try{ const d=await idb(); d.transaction(STORE,"readwrite").objectStore(STORE).delete("key"); }catch(e){} }
const b64=s=>Uint8Array.from(atob(s.trim()),c=>c.charCodeAt(0));
async function fetchText(u){ const r=await fetch(u,{cache:"no-cache"}); if(!r.ok) throw new Error("http"); return r.text(); }
let INDEX=null;
async function loadIndex(){ INDEX=JSON.parse(await fetchText("data/index.json")); return INDEX; }
async function deriveKey(pw){
  const base=await crypto.subtle.importKey("raw",new TextEncoder().encode(pw),"PBKDF2",false,["deriveKey"]);
  return crypto.subtle.deriveKey({name:"PBKDF2",salt:b64(INDEX.salt),iterations:INDEX.iter,hash:"SHA-256"},base,{name:"AES-GCM",length:256},false,["decrypt"]);
}
async function decryptMonth(key,txt){
  const all=b64(txt), iv=all.slice(0,12), ct=all.slice(12);
  const gz=await crypto.subtle.decrypt({name:"AES-GCM",iv},key,ct);
  const stream=new Blob([gz]).stream().pipeThrough(new DecompressionStream("gzip"));
  return JSON.parse(await new Response(stream).text());
}
async function loadAll(key){
  const ms=Object.keys(INDEX.months).sort();
  const parts=await Promise.all(ms.map(async m=>decryptMonth(key,await fetchText("data/"+INDEX.months[m].file))));
  RAW=[]; BALANCES={};
  parts.forEach(p=>{ RAW=RAW.concat(p.rows); if(p.bal!=null) BALANCES[p.m]=p.bal; });
  ALL=buildAll(); sel="all"; shown=60;
  $("foot").textContent="Stand der Daten: "+(INDEX.updated||"").split("-").reverse().join(".")+". Verschlüsselt gespeichert, nur auf diesem Gerät lesbar.";
  $("lock").hidden=true; $("app").hidden=false;
  renderCatSel(); renderAll();
}
function showLock(msg){ $("app").hidden=true; $("lock").hidden=false; $("lockErr").textContent=msg||""; }
$("lockForm").addEventListener("submit",async e=>{
  e.preventDefault();
  const pw=$("pw").value; if(!pw) return;
  $("unlockBtn").disabled=true; $("unlockBtn").textContent="Entsperre …"; $("lockErr").textContent="";
  try{
    if(!INDEX) await loadIndex();
    const key=await deriveKey(pw);
    await loadAll(key);
    if($("remember").checked) await keySet(key); else await keyDel();
    $("pw").value="";
  }catch(err){
    showLock(err&&err.name==="OperationError"?"Das Passwort stimmt nicht.":"Die Daten konnten nicht geladen werden. Bist du online?");
  }
  $("unlockBtn").disabled=false; $("unlockBtn").textContent="Entsperren";
});
$("logoutBtn").addEventListener("click",async()=>{ await keyDel(); RAW=[]; BALANCES={}; ALL=[]; $("list").innerHTML=""; showLock(""); });
(async()=>{
  if("serviceWorker" in navigator){ try{ navigator.serviceWorker.register("sw.js"); }catch(e){} }
  try{
    await loadIndex();
    const k=await keyGet();
    if(k){ try{ await loadAll(k); return; }catch(e){ await keyDel(); } }
    showLock("");
  }catch(e){ showLock("Die Daten konnten nicht geladen werden. Bist du online?"); }
})();
</script>''')

open(out, "w", encoding="utf-8").write(s)
print("ok", out, len(s))
