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
    '#lock [hidden]{display:none!important}\n'
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
    '#lock .fidbtn{width:100%;font-size:.95rem;padding:12px;margin-bottom:12px}\n'
    '#lock .or{color:var(--muted);font-size:.8rem;margin:4px 0 10px}\n'
    '#fidDlg{border:1px solid var(--line);border-radius:16px;background:var(--card);color:var(--text);padding:18px;width:min(92vw,360px);box-shadow:var(--shadow)}\n'
    '#fidDlg::backdrop{background:rgba(0,0,0,.45)}\n'
    '#fidDlg input{width:100%;border:1px solid var(--line);background:var(--bg);color:var(--text);border-radius:10px;padding:10px;font-size:1rem;margin-top:8px}\n'
    '#fidDlg .user{position:absolute;left:-9999px;width:1px;height:1px;opacity:0}\n'
    '#fidDlg .acts{display:flex;gap:8px;margin-top:14px}#fidDlg .acts .btn{flex:1}\n'
    '.secrow{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}\n'
    'footer{color:var(--muted)')

rep('<body>\n<div class="wrap" id="app">',
    '<body>\n'
    '<div id="lock"><form class="box" id="lockForm" autocomplete="on">\n'
    '  <img class="logo" src="icon-180.png" alt="">\n'
    '  <h1>Finanzen</h1>\n'
    '  <p id="lockInfo">Gib dein App-Passwort ein. Die Daten werden erst hier auf dem iPhone entschlüsselt.</p>\n'
    '  <div id="fidBox" hidden><button class="btn go fidbtn" id="fidUnlock" type="button">Mit Face ID entsperren</button><div class="or">oder mit Passwort</div></div>\n'
    '  <input class="user" type="text" name="username" autocomplete="username" value="alex" tabindex="-1" aria-hidden="true">\n'
    '  <input type="password" id="pw" name="password" autocomplete="current-password" placeholder="App-Passwort" required>\n'
    '  <label class="chk" id="rememberL"><input type="checkbox" id="remember" checked> Auf diesem Gerät angemeldet bleiben</label>\n'
    '  <button class="btn go" id="unlockBtn" type="submit">Entsperren</button>\n'
    '  <div class="err" id="lockErr" role="alert"></div>\n'
    '</form></div>\n'
    '<div class="wrap" id="app" hidden>')

rep('<button class="btn" id="hideBtn" type="button">Beträge ausblenden</button>',
    '<button class="btn" id="hideBtn" type="button">Beträge ausblenden</button>\n'
    '      <button class="btn" id="logoutBtn" type="button">Sperren</button>')

rep('<footer>Alle Daten stehen nur in dieser Datei und in deinem Browser. Nichts wird hochgeladen.</footer>',
    '<section id="secSec"><div class="secrow"><div><h2 style="margin:0">Face ID beim Öffnen</h2>'
    '<div class="note" id="fidState" style="margin-top:4px"></div></div>'
    '<button type="button" class="btn" id="fidToggle">Einschalten</button></div>'
    '<div class="note" id="fidMsg"></div></section>\n'
    '  <dialog id="fidDlg"><form method="dialog" id="fidForm" autocomplete="on">'
    '<h3 style="margin:0 0 4px;font-size:1.02rem">Face ID einschalten</h3>'
    '<div class="note" style="margin-top:0">Bitte einmal dein App-Passwort eingeben. Danach entsperrt Face ID die App.</div>'
    '<input class="user" type="text" name="username" autocomplete="username" value="alex" tabindex="-1" aria-hidden="true">'
    '<input type="password" id="fidPw" name="password" autocomplete="current-password" placeholder="App-Passwort">'
    '<div class="note" id="fidErr" style="color:var(--bad)"></div>'
    '<div class="acts"><button type="button" class="btn" id="fidCancel">Abbrechen</button><button type="submit" class="btn go" id="fidOk" style="background:var(--accent);color:#fff;border-color:var(--accent)">Weiter</button></div>'
    '</form></dialog>\n'
    '<footer id="foot">Die Daten liegen verschlüsselt im Netz und werden nur auf diesem Gerät entschlüsselt.</footer>')

rep('const RAW=/*RAWDATA*/[];\nconst BALANCES=/*BALANCES*/{};', 'let RAW=[];\nlet BALANCES={};')

rep('renderCatSel();\nrenderAll();\n</script>', r'''// ---------- Entsperren, Face ID & Laden ----------
const DB="fin_app",STORE="k",enc=new TextEncoder();
const PRF_SALT=enc.encode("finanzen-app-faceid-v1");
const RELOCK_MS=60000;
function idb(){ return new Promise((res,rej)=>{ const r=indexedDB.open(DB,1); r.onupgradeneeded=()=>r.result.createObjectStore(STORE); r.onsuccess=()=>res(r.result); r.onerror=()=>rej(r.error); }); }
async function dbGet(k){ try{ const d=await idb(); return await new Promise(res=>{ const q=d.transaction(STORE).objectStore(STORE).get(k); q.onsuccess=()=>res(q.result||null); q.onerror=()=>res(null); }); }catch(e){ return null; } }
async function dbSet(k,v){ try{ const d=await idb(); await new Promise(res=>{ const t=d.transaction(STORE,"readwrite"); t.objectStore(STORE).put(v,k); t.oncomplete=res; t.onerror=res; }); }catch(e){} }
async function dbDel(k){ try{ const d=await idb(); await new Promise(res=>{ const t=d.transaction(STORE,"readwrite"); t.objectStore(STORE).delete(k); t.oncomplete=res; t.onerror=res; }); }catch(e){} }
const b64=s=>Uint8Array.from(atob(s.trim()),c=>c.charCodeAt(0));
const rnd=n=>crypto.getRandomValues(new Uint8Array(n));
async function fetchText(u){ const r=await fetch(u,{cache:"no-cache"}); if(!r.ok) throw new Error("http"); return r.text(); }
let INDEX=null, CURKEY=null, hiddenAt=0;
async function loadIndex(){ INDEX=JSON.parse(await fetchText("data/index.json")); return INDEX; }
async function rawFromPw(pw){
  const base=await crypto.subtle.importKey("raw",enc.encode(pw),"PBKDF2",false,["deriveBits"]);
  return new Uint8Array(await crypto.subtle.deriveBits({name:"PBKDF2",salt:b64(INDEX.salt),iterations:INDEX.iter,hash:"SHA-256"},base,256));
}
const keyFromRaw=raw=>crypto.subtle.importKey("raw",raw,{name:"AES-GCM"},false,["decrypt"]);
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
  ALL=buildAll(); sel="all"; shown=60; CURKEY=key;
  $("foot").textContent="Stand der Daten: "+(INDEX.updated||"").split("-").reverse().join(".")+". Verschlüsselt gespeichert, nur auf diesem Gerät lesbar.";
  $("lock").hidden=true; $("app").hidden=false;
  renderCatSel(); renderAll(); renderSec();
}
function wipe(){ RAW=[]; BALANCES={}; ALL=[]; CURKEY=null; $("list").innerHTML=""; }
async function showLock(msg){
  const fid=await dbGet("fid");
  $("fidBox").hidden=!fid; $("rememberL").hidden=!!fid;
  $("app").hidden=true; $("lock").hidden=false; $("lockErr").textContent=msg||"";
}
// --- Face ID (WebAuthn-Passkey, Schlüssel per PRF verschlüsselt) ---
const fidSupported=()=>!!(window.PublicKeyCredential&&navigator.credentials&&navigator.credentials.create);
async function fidAssert(id){
  const a=await navigator.credentials.get({publicKey:{challenge:rnd(32),allowCredentials:[{type:"public-key",id:b64(id)}],userVerification:"required",timeout:60000,extensions:{prf:{eval:{first:PRF_SALT}}}}});
  const r=a.getClientExtensionResults&&a.getClientExtensionResults();
  return r&&r.prf&&r.prf.results&&r.prf.results.first?new Uint8Array(r.prf.results.first):null;
}
async function wrapKey(prf){
  const h=await crypto.subtle.importKey("raw",prf,"HKDF",false,["deriveKey"]);
  return crypto.subtle.deriveKey({name:"HKDF",hash:"SHA-256",salt:new Uint8Array(32),info:enc.encode("finanzen-wrap")},h,{name:"AES-GCM",length:256},false,["encrypt","decrypt"]);
}
const toB64=u=>btoa(String.fromCharCode(...new Uint8Array(u)));
async function unlockFid(){
  const fid=await dbGet("fid"); if(!fid) return false;
  const prf=await fidAssert(fid.id);
  if(fid.mode==="prf"){
    if(!prf) throw new Error("noprf");
    const w=await wrapKey(prf);
    const raw=new Uint8Array(await crypto.subtle.decrypt({name:"AES-GCM",iv:b64(fid.iv)},w,b64(fid.ct)));
    await loadAll(await keyFromRaw(raw)); return true;
  }
  const k=await dbGet("key"); if(!k) throw new Error("nokey");
  await loadAll(k); return true;
}
async function tryFid(auto){
  try{ $("lockErr").textContent=""; await unlockFid(); }
  catch(e){ if(!auto) $("lockErr").textContent="Face ID hat nicht geklappt. Nochmal tippen oder Passwort nutzen."; }
}
$("fidUnlock").addEventListener("click",()=>tryFid(false));
async function renderSec(){
  const fid=await dbGet("fid");
  if(!fidSupported()){ $("fidState").textContent="Auf diesem Gerät nicht verfügbar."; $("fidToggle").hidden=true; return; }
  $("fidToggle").hidden=false;
  $("fidToggle").textContent=fid?"Ausschalten":"Einschalten";
  $("fidState").textContent=fid?("Eingeschaltet. Die App sperrt sich beim Öffnen und nach 1 Minute im Hintergrund."+(fid.mode==="gate"?" (Einfacher Modus: dein iPhone unterstützt die verschlüsselte Variante nicht.)":"")):"Ausgeschaltet. Die App öffnet sich ohne Abfrage, solange du angemeldet bleibst.";
}
$("fidToggle").addEventListener("click",async()=>{
  $("fidMsg").textContent="";
  const fid=await dbGet("fid");
  if(fid){ await dbDel("fid"); if(CURKEY) await dbSet("key",CURKEY); renderSec(); $("fidMsg").textContent="Face ID ist aus."; return; }
  $("fidPw").value=""; $("fidErr").textContent="";
  const d=$("fidDlg"); if(d.showModal) d.showModal(); else d.setAttribute("open","");
});
$("fidCancel").addEventListener("click",()=>{ const d=$("fidDlg"); if(d.close) d.close(); else d.removeAttribute("open"); });
$("fidForm").addEventListener("submit",async e=>{
  e.preventDefault();
  const pw=$("fidPw").value; if(!pw) return;
  $("fidOk").disabled=true; $("fidErr").textContent="";
  try{
    const raw=await rawFromPw(pw); const key=await keyFromRaw(raw);
    const m0=Object.keys(INDEX.months).sort()[0];
    try{ await decryptMonth(key,await fetchText("data/"+INDEX.months[m0].file)); }catch(err){ $("fidErr").textContent="Das Passwort stimmt nicht."; $("fidOk").disabled=false; return; }
    const cred=await navigator.credentials.create({publicKey:{rp:{name:"Finanzen"},user:{id:rnd(16),name:"alex",displayName:"Finanzen-App"},challenge:rnd(32),
      pubKeyCredParams:[{type:"public-key",alg:-7},{type:"public-key",alg:-257}],timeout:60000,
      authenticatorSelection:{authenticatorAttachment:"platform",residentKey:"preferred",userVerification:"required"},
      extensions:{prf:{eval:{first:PRF_SALT}}}}});
    const id=toB64(cred.rawId);
    const ext=cred.getClientExtensionResults?cred.getClientExtensionResults():{};
    let prf=ext.prf&&ext.prf.results&&ext.prf.results.first?new Uint8Array(ext.prf.results.first):null;
    if(!prf&&ext.prf&&ext.prf.enabled!==false){ try{ prf=await fidAssert(id); }catch(err){ prf=null; } }
    if(prf){
      const w=await wrapKey(prf), iv=rnd(12);
      const ct=await crypto.subtle.encrypt({name:"AES-GCM",iv},w,raw);
      await dbSet("fid",{mode:"prf",id,iv:toB64(iv),ct:toB64(ct)});
      await dbDel("key");
    }else{
      await dbSet("fid",{mode:"gate",id}); await dbSet("key",key);
    }
    const d=$("fidDlg"); if(d.close) d.close(); else d.removeAttribute("open");
    renderSec(); $("fidMsg").textContent="Face ID ist eingeschaltet.";
  }catch(err){ $("fidErr").textContent="Face ID konnte nicht eingerichtet werden."; }
  $("fidOk").disabled=false;
});
// --- Passwort ---
$("lockForm").addEventListener("submit",async e=>{
  e.preventDefault();
  const pw=$("pw").value; if(!pw) return;
  $("unlockBtn").disabled=true; $("unlockBtn").textContent="Entsperre …"; $("lockErr").textContent="";
  try{
    if(!INDEX) await loadIndex();
    const key=await keyFromRaw(await rawFromPw(pw));
    await loadAll(key);
    const fid=await dbGet("fid");
    if(!fid){ if($("remember").checked) await dbSet("key",key); else await dbDel("key"); }
    else if(fid.mode==="gate") await dbSet("key",key);
    $("pw").value="";
  }catch(err){
    await showLock(err&&err.name==="OperationError"?"Das Passwort stimmt nicht.":"Die Daten konnten nicht geladen werden. Bist du online?");
  }
  $("unlockBtn").disabled=false; $("unlockBtn").textContent="Entsperren";
});
$("logoutBtn").addEventListener("click",async()=>{ if(!(await dbGet("fid"))) await dbDel("key"); wipe(); showLock(""); });
document.addEventListener("visibilitychange",async()=>{
  if(document.hidden){ hiddenAt=Date.now(); return; }
  if(hiddenAt&&Date.now()-hiddenAt>RELOCK_MS&&!$("app").hidden&&(await dbGet("fid"))){ wipe(); await showLock(""); tryFid(true); }
  hiddenAt=0;
});
(async()=>{
  if("serviceWorker" in navigator){ try{ navigator.serviceWorker.register("sw.js"); }catch(e){} }
  try{
    await loadIndex();
    const fid=await dbGet("fid");
    if(fid){ await showLock(""); tryFid(true); return; }
    const k=await dbGet("key");
    if(k){ try{ await loadAll(k); return; }catch(e){ await dbDel("key"); } }
    showLock("");
  }catch(e){ showLock("Die Daten konnten nicht geladen werden. Bist du online?"); }
})();
</script>''')


open(out, "w", encoding="utf-8").write(s)
print("ok", out, len(s))
