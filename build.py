# -*- coding: utf-8 -*-
"""把 A.md / B.md 組成單頁式 index.html（分頁切換、可列印）。"""
import io
import re

import markdown

EXT = ["tables", "attr_list", "sane_lists", "nl2br"]


def render(path):
    with io.open(path, encoding="utf-8") as f:
        text = f.read()
    # 去掉第一個 H1（標題另外由頁首處理）
    lines = text.split("\n")
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
        text = "\n".join(lines[1:])
    else:
        title = path
    html = markdown.markdown(text, extensions=EXT)
    # 讓每個表格可橫向捲動
    html = html.replace("<table>", '<div class="tw"><table>').replace(
        "</table>", "</table></div>"
    )
    return title, html


def toc(html):
    items = []
    for m in re.finditer(r"<h2>(.*?)</h2>", html):
        raw = re.sub(r"<.*?>", "", m.group(1))
        slug = "s" + str(len(items))
        items.append((slug, raw))
    # 回填 id
    idx = [0]

    def add_id(m):
        slug = "s" + str(idx[0])
        idx[0] += 1
        return '<h2 id="%s">%s</h2>' % (slug, m.group(1))

    html = re.sub(r"<h2>(.*?)</h2>", add_id, html)
    nav = "".join('<a href="#%s">%s</a>' % (s, t) for s, t in items)
    return html, nav


titleA, htmlA = render("A.md")
titleB, htmlB = render("B.md")
htmlA, navA = toc(htmlA)
htmlB, navB = toc(htmlB)

PAGE = u"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive">
<meta name="color-scheme" content="light">
<title>大埔美園區三路29號｜行業別進駐法規與詢問備忘錄</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
/* 固定淺色：不隨系統深色模式變動 */
:root{
  color-scheme:light only;
  --bg:#f6f7f9; --card:#fff; --ink:#1c2430; --mute:#5d6b7e; --line:#e2e6ec;
  --accent:#0f4c81; --accent-soft:#e8f0f8; --warn:#b3541e; --warn-soft:#fdf1e6;
  --ok:#1f6f4a; --mono:ui-monospace,SFMono-Regular,Menlo,monospace;
}
html{color-scheme:light only;background:#f6f7f9}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"Noto Sans TC",-apple-system,"Segoe UI","Microsoft JhengHei",sans-serif;
  line-height:1.75;font-size:15.5px;-webkit-text-size-adjust:100%}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px 80px}
header{background:var(--accent);color:#fff;padding:26px 0 22px;margin-bottom:22px}
header .wrap{padding-bottom:0}
.kicker{font-size:12.5px;letter-spacing:.14em;opacity:.8;margin:0 0 6px}
h1{font-size:23px;margin:0 0 10px;line-height:1.35;font-weight:700}
.meta{font-size:13.5px;opacity:.9;margin:0}
.tabs{display:flex;gap:8px;margin:18px 0 0;flex-wrap:wrap}
.tabs button{appearance:none;border:0;cursor:pointer;font:inherit;font-weight:500;
  padding:9px 16px;border-radius:8px 8px 0 0;background:rgba(255,255,255,.16);color:#fff}
.tabs button[aria-selected="true"]{background:var(--bg);color:var(--accent);font-weight:700}
.note{background:var(--warn-soft);border-left:4px solid var(--warn);color:var(--ink);
  padding:12px 16px;border-radius:0 8px 8px 0;margin:0 0 20px;font-size:13.5px}
nav.toc{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 20px}
nav.toc a{font-size:12.5px;text-decoration:none;color:var(--mute);border:1px solid var(--line);
  padding:5px 10px;border-radius:99px;background:var(--card)}
nav.toc a:hover{color:var(--accent);border-color:var(--accent)}
article{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:28px 30px}
article h2{font-size:19px;margin:34px 0 12px;padding-bottom:8px;border-bottom:2px solid var(--accent);
  scroll-margin-top:16px}
article h2:first-child{margin-top:0}
article h3{font-size:16px;margin:24px 0 8px;color:var(--accent)}
article h4{font-size:14.5px;margin:18px 0 6px}
article p{margin:0 0 12px}
article ul,article ol{margin:0 0 14px;padding-left:22px}
article li{margin:3px 0}
article strong{font-weight:700}
article hr{border:0;border-top:1px solid var(--line);margin:30px 0}
article blockquote{margin:0 0 16px;padding:12px 18px;background:var(--accent-soft);
  border-left:4px solid var(--accent);border-radius:0 8px 8px 0;font-size:14.5px}
article blockquote p:last-child{margin-bottom:0}
article code{font-family:var(--mono);font-size:.9em;background:var(--accent-soft);
  padding:1px 5px;border-radius:4px}
.tw{overflow-x:auto;margin:0 0 18px;border:1px solid var(--line);border-radius:8px}
table{border-collapse:collapse;width:100%;font-size:13.8px;min-width:460px}
th,td{padding:8px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{background:var(--accent-soft);font-weight:700;white-space:nowrap}
tr:last-child td{border-bottom:0}
footer{margin-top:34px;font-size:12.5px;color:var(--mute);text-align:center}
[hidden]{display:none!important}
@media print{
  header{background:#fff;color:#000;border-bottom:2px solid #000}
  .tabs,nav.toc,footer,.note{display:none}
  article{border:0;padding:0}
  [hidden]{display:block!important}
  body{font-size:11pt;background:#fff}
}
@media (max-width:640px){
  .wrap{padding:0 14px 60px} article{padding:20px 16px} h1{font-size:19px}
}
</style>
</head>
<body>
<header><div class="wrap">
  <p class="kicker">RUEI.HE REAL ESTATE ｜ 內部作業文件</p>
  <h1>大埔美精密機械園區．園區三路29號（大工一段91地號）<br>行業別進駐法規依據與管理處詢問備忘錄</h1>
  <p class="meta">瑞禾不動產經紀股份有限公司　張現傑 業務總監　｜　2026-09-02</p>
  <div class="tabs" role="tablist">
    <button role="tab" aria-selected="true" data-t="A">A．法規依據與預審程序</button>
    <button role="tab" aria-selected="false" data-t="B">B．管理處詢問備忘錄（匿名版）</button>
  </div>
</div></header>

<div class="wrap">
  <p class="note"><strong>機密：</strong>本頁為內部作業文件，含買方評估資料與議價策略，僅供專案成員使用，請勿轉發或公開連結。</p>

  <section data-p="A">
    <nav class="toc">__NAVA__</nav>
    <article>__A__</article>
  </section>

  <section data-p="B" hidden>
    <nav class="toc">__NAVB__</nav>
    <article>__B__</article>
  </section>

  <footer>瑞禾不動產經紀股份有限公司　｜　臺中市南屯區益豐路四段91號　｜　TEL 04-23803560</footer>
</div>

<script>
var btns=document.querySelectorAll('.tabs button');
var secs=document.querySelectorAll('section[data-p]');
function show(k){
  btns.forEach(function(b){b.setAttribute('aria-selected',b.dataset.t===k);});
  secs.forEach(function(s){s.hidden=(s.dataset.p!==k);});
  try{localStorage.setItem('dpm91tab',k);}catch(e){}
  window.scrollTo(0,0);
}
btns.forEach(function(b){b.addEventListener('click',function(){show(b.dataset.t);});});
try{var k=localStorage.getItem('dpm91tab'); if(k){show(k);}}catch(e){}
</script>
</body>
</html>
"""

out = (
    PAGE.replace("__A__", htmlA)
    .replace("__B__", htmlB)
    .replace("__NAVA__", navA)
    .replace("__NAVB__", navB)
)
with io.open("index.html", "w", encoding="utf-8") as f:
    f.write(out)
print("index.html written:", len(out), "chars")
