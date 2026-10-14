# -*- coding: utf-8 -*-
# 生成 UE API 单文件索引页：数据内嵌、零依赖、可搜索/筛选/排序；stdout 输出由 shell 重定向落盘
import json, sys
sys.path.insert(0, '.')
sys.stdout.reconfigure(encoding='utf-8')

from doc_data import DOMAIN_MODULES, EDITOR_DOMAINS, DEV_DOMAINS

mods = json.load(open('engine_modules_merged.json', encoding='utf-8'))
bp = json.load(open('bp_categories_full.json', encoding='utf-8'))
plugs = json.load(open('local_uplugins.json', encoding='utf-8'))
cpp_leaf = json.load(open('cpp_leaf_summary.json', encoding='utf-8'))
py_leaf = json.load(open('py_leaf.json', encoding='utf-8'))
bp_nodes = json.load(open('bp_node_leaf.json', encoding='utf-8'))
py_sweep = json.load(open('py_sweep_full.json', encoding='utf-8'))
bp_nodes_all = json.load(open('bp_nodes_all.json', encoding='utf-8'))

name2dom = {}
for dom, names in list(DOMAIN_MODULES.items()) + list(EDITOR_DOMAINS.items()) + list(DEV_DOMAINS.items()):
    for n in names:
        name2dom[n] = dom

eng_rows = []
for m in mods:
    g, n = m['slug'].split('/', 1)
    s = m.get('sections', {})
    eng_rows.append({
        'n': n, 'g': g, 'd': name2dom.get(n, ''),
        'cls': len(s.get('Classes', []) or []), 'st': len(s.get('Structs', []) or []),
        'en': len(s.get('Enums', []) or []), 'fn': len(s.get('Functions', []) or []),
        'tot': sum(len(v) for v in s.values()),
        'loc': (m.get('loc') or '').replace(chr(92), '/'),
        'url': 'https://dev.epicgames.com/documentation/unreal-engine/API/' + g + '/' + n
    })

bp_rows = []
for b in sorted(bp, key=lambda x: x['slug']):
    ch = b.get('n_dirs', 0) + b.get('n_actions', 0)
    bp_rows.append({
        'n': b['slug'], 'ch': ch if not b.get('status') else -1,
        'url': 'https://dev.epicgames.com/documentation/unreal-engine/BlueprintAPI/' + b['slug']
    })

plug_rows = []
for p in plugs:
    plug_rows.append({
        'n': p['docs_name'], 'cat': p['cat'] or '(未标注)', 'exp': 1 if p['is_experimental_dir'] else 0,
        'desc': (p['desc'] or '').strip()[:220], 'mods': len(p['modules']),
        'url': 'https://dev.epicgames.com/documentation/unreal-engine/API/PluginIndex/' + p['docs_name']
    })

node_rows = []
for x in bp_nodes:
    if x.get('status') or x.get('err'):
        continue
    node_rows.append({'n': x['node'], 'desc': (x.get('desc') or [''])[0][:150]})

node2_rows = []
for r in bp_nodes_all:
    if r.get('dir'):
        continue
    parts = r['s'].split('/')
    node2_rows.append({'c': parts[0], 'n': '/'.join(parts[1:]), 'd': r.get('d', ''), 't': r.get('t', ''),
                       'url': 'https://dev.epicgames.com/documentation/unreal-engine/BlueprintAPI/' + r['s']})

data = {'eng': eng_rows, 'bp': bp_rows, 'plug': plug_rows, 'sweep': py_sweep, 'nodes2': node2_rows,
        'cppLeaf': cpp_leaf, 'pyLeaf': py_leaf, 'nodes': node_rows}
data_json = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

groups_js = json.dumps(sorted(set(r['g'] for r in eng_rows)), ensure_ascii=False)
domains_js = json.dumps(sorted(set(r['d'] for r in eng_rows)), ensure_ascii=False)
cats_js = json.dumps(sorted(set(r['cat'] for r in plug_rows)), ensure_ascii=False)

tot_entries = sum(r['tot'] for r in eng_rows)
bp_children = sum(r['ch'] for r in bp_rows if r['ch'] > 0)

CSS = """
:root { --bg:#111418; --panel:#1a1f26; --line:#2a323c; --fg:#dde3ea; --dim:#8b96a3; --acc:#5aa9e6; --th:#7ec8e3; }
* { box-sizing:border-box; margin:0; padding:0; }
body { background:var(--bg); color:var(--fg); font:14px/1.6 "Segoe UI",system-ui,sans-serif; padding:24px; }
h1 { font-size:20px; margin-bottom:4px; }
.sub { color:var(--dim); font-size:12.5px; margin-bottom:16px; }
.sub a { color:var(--acc); text-decoration:none; }
.stats { display:flex; gap:12px; flex-wrap:wrap; margin-bottom:16px; }
.stat { background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:8px 14px; font-size:12.5px; color:var(--dim); }
.stat b { color:var(--fg); font-size:16px; margin-right:4px; }
.bar { display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-bottom:14px; }
.tabs { display:flex; gap:6px; }
.tab { background:var(--panel); border:1px solid var(--line); color:var(--dim); border-radius:8px; padding:6px 14px; cursor:pointer; font-size:13px; }
.tab.on { color:#fff; border-color:var(--acc); background:#20303f; }
input[type=text], select { background:var(--panel); border:1px solid var(--line); color:var(--fg); border-radius:8px; padding:6px 10px; font-size:13px; }
input[type=text] { width:260px; }
.count { color:var(--dim); font-size:12.5px; margin-left:auto; }
table { width:100%; border-collapse:collapse; background:var(--panel); }
th, td { padding:6px 10px; text-align:left; border-bottom:1px solid var(--line); font-size:13px; white-space:nowrap; }
th { color:var(--th); cursor:pointer; user-select:none; position:sticky; top:0; background:#141920; font-weight:600; }
th:hover { color:#fff; }
td.wrap { white-space:normal; max-width:480px; }
td.num, th.num { text-align:right; font-variant-numeric:tabular-nums; }
tr:hover td { background:#1f2630; }
a.lk { color:var(--acc); text-decoration:none; }
a.lk:hover { text-decoration:underline; }
.tag { display:inline-block; border-radius:4px; padding:0 6px; font-size:11.5px; line-height:1.7; }
.g-Runtime { background:#1d3a2a; color:#7ed9a0; } .g-Editor { background:#3a2e1d; color:#e3b97e; } .g-Developer { background:#2b2340; color:#b79ee3; }
.exp { background:#3d1f1f; color:#e39a9a; }
.z { color:var(--dim); font-size:11.5px; }
.wrapbox { max-height:calc(100vh - 220px); overflow:auto; border-radius:10px; border:1px solid var(--line); }
.hide { display:none; }
footer { margin-top:14px; color:var(--dim); font-size:12px; }
h3.leaf { margin:14px 0 6px; font-size:15px; }
"""

JS = """
var D = %DATA%;
var cur = 'eng';
var sortK = {eng:'tot', bp:'ch', plug:'mods', nodes2:'t'}, sortDesc = true;
var COLS = {
  eng: [['n','模块',0],['g','组',0],['d','功能域',0],['tot','总条目',1],['cls','Classes',1],['st','Structs',1],['en','Enums',1],['fn','Functions',1],['loc','源码位置',0],['#','文档',0]],
  bp:  [['n','分类',0],['ch','子条目',1],['#','文档',0]],
  plug:[['n','插件',0],['cat','官方分类',0],['exp','状态',0],['mods','模块数',1],['desc','描述',0],['#','文档',0]],
  nodes2:[['n','节点',0],['c','分类',0],['t','Target 宿主',0],['d','描述',0],['#','↗',0]]
};
function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;');}
function isNumCol(t,k){for(var i=0;i<COLS[t].length;i++)if(COLS[t][i][0]===k)return !!COLS[t][i][2];return false;}
function cellHtml(k, r, t) {
  if (k === '#') return '<a class="lk" href="'+r.url+'" target="_blank">↗</a>';
  if (k === 'g') return '<span class="tag g-'+esc(r.g)+'">'+esc(r.g)+'</span>';
  if (k === 'exp') return r.exp ? '<span class="tag exp">EXP</span>' : '<span class="z">稳定</span>';
  if (k === 'ch') return r.ch < 0 ? '<span class="z">未取回</span>' : r.ch;
  return esc(r[k]);
}
function drawHead(t) {
  var tr = '<tr>';
  COLS[t].forEach(function(c){
    var arrow = (sortK[t]===c[0]) ? (sortDesc?' ↓':' ↑') : '';
    tr += '<th data-k="'+c[0]+'" class="'+(c[2]?'num':'')+'">'+c[1]+arrow+'</th>';
  });
  document.querySelector('#tb thead').innerHTML = tr + '</tr>';
  document.querySelectorAll('#tb th').forEach(function(th){
    th.onclick = function(){
      var k = th.dataset.k;
      if (k==='#') return;
      if (sortK[cur]===k) sortDesc = !sortDesc; else { sortK[cur]=k; sortDesc = true; }
      render();
    };
  });
}
function rows(t) {
  var q = document.getElementById('q').value.trim().toLowerCase();
  var f1 = document.getElementById('f1').value, f2 = document.getElementById('f2').value, f3 = document.getElementById('f3').value;
  var src = D[t];
  if (t==='eng') src = src.filter(function(r){ return (!f1||r.g===f1)&&(!f2||r.d===f2); });
  if (t==='plug') src = src.filter(function(r){ return (!f3||r.cat===f3); });
  if (t==='nodes2') { var f4 = document.getElementById('f4').value; src = src.filter(function(r){ return (!f4||r.c===f4); }); }
  if (q) src = src.filter(function(r){
    if ((r.n||'').toLowerCase().indexOf(q)>=0) return true;
    if (r.d && r.d.toLowerCase().indexOf(q)>=0) return true;
    if (r.desc && r.desc.toLowerCase().indexOf(q)>=0) return true;
    if (r.loc && r.loc.toLowerCase().indexOf(q)>=0) return true;
    if (r.t && r.t.toLowerCase().indexOf(q)>=0) return true;
    if (r.c && r.c.toLowerCase().indexOf(q)>=0) return true;
    return false;
  });
  var k = sortK[t];
  src = src.slice().sort(function(a,b){
    var x=a[k],y=b[k];
    if (typeof x==='number') return sortDesc? y-x : x-y;
    return sortDesc? String(y).localeCompare(x) : String(x).localeCompare(y);
  });
  return src;
}
function render() {
  var rs = rows(cur);
  drawHead(cur);
  var html = '';
  rs.forEach(function(r){
    html += '<tr>';
    COLS[cur].forEach(function(c){
      html += '<td class="'+(c[2]?'num':(c[0]==='desc'?'wrap':''))+'">'+cellHtml(c[0], r, cur)+'</td>';
    });
    html += '</tr>';
  });
  document.querySelector('#tb tbody').innerHTML = html;
  document.getElementById('cnt').textContent = rs.length + ' 行';
}
function restoreTable() {
  var box = document.getElementById('leafbox');
  if (box) box.outerHTML = '<div class="wrapbox"><table id="tb"><thead></thead><tbody></tbody></table></div>';
}
function showLeaf() {
  restoreTable();
  var h = '';
  h += '<h3 class="leaf">C++ 核心类成员面（32 类抽样）</h3><table><thead><tr><th>类</th><th>模块</th><th class="num">函数</th><th class="num">变量</th><th class="num">派生类</th></tr></thead><tbody>';
  D.cppLeaf.forEach(function(r){ h += '<tr><td>'+esc(r.name)+'</td><td>'+esc(r.mod)+'</td><td class="num">'+r.funcs+'</td><td class="num">'+r.vars+'</td><td class="num">'+r.derived+'</td></tr>'; });
  h += '</tbody></table>';
  h += '<h3 class="leaf">Python 主力类成员数（28 类抽样）</h3><table><thead><tr><th>unreal 类</th><th class="num">成员数</th><th>基类</th><th>备注</th></tr></thead><tbody>';
  D.pyLeaf.forEach(function(r){ h += '<tr><td>'+esc(r.name)+'</td><td class="num">'+r.members+'</td><td>'+esc(r.bases)+'</td><td class="wrap">'+esc(r.note)+'</td></tr>'; });
  h += '</tbody></table>';
  h += '<h3 class="leaf">Python 动作类普查（250 个 Library/Subsystem，按成员数）</h3><table><thead><tr><th>unreal 类</th><th class="num">成员</th><th>unreal 类</th><th class="num">成员</th><th>unreal 类</th><th class="num">成员</th></tr></thead><tbody>';
  var sw = D.sweep.filter(function(r){return r.m>0;});
  for (var i = 0; i < sw.length; i += 3) {
    h += '<tr>';
    for (var j = 0; j < 3; j++) { var rr = sw[i+j]; h += rr ? '<td>'+esc(rr.name)+'</td><td class="num">'+rr.m+'</td>' : '<td></td><td></td>'; }
    h += '</tr>';
  }
  h += '</tbody></table>';
  h += '<h3 class="leaf">蓝图节点页抽样（含 Target is 溯源）</h3><table><thead><tr><th>节点</th><th>描述 / Target</th></tr></thead><tbody>';
  D.nodes.forEach(function(r){ h += '<tr><td>'+esc(r.n)+'</td><td class="wrap">'+esc(r.desc)+'</td></tr>'; });
  h += '</tbody></table>';
  var hosts = {};
  D.nodes2.forEach(function(r){ if (r.t) hosts[r.t] = (hosts[r.t]||0)+1; });
  var hl = Object.keys(hosts).map(function(k){return [k, hosts[k]];}).sort(function(a,b){return b[1]-a[1];});
  h += '<h3 class="leaf">蓝图节点宿主分布（Target is 统计，样本 ' + D.nodes2.length + ' 节点）</h3><table><thead><tr><th>C++ 宿主</th><th class="num">节点数</th><th>C++ 宿主</th><th class="num">节点数</th></tr></thead><tbody>';
  for (var i = 0; i < hl.length; i += 2) {
    h += '<tr><td>'+esc(hl[i][0])+'</td><td class="num">'+hl[i][1]+'</td>' + (hl[i+1] ? '<td>'+esc(hl[i+1][0])+'</td><td class="num">'+hl[i+1][1]+'</td>' : '<td></td><td></td>') + '</tr>';
  }
  h += '</tbody></table>';
  document.getElementById('cnt').textContent = (D.cppLeaf.length + D.pyLeaf.length + D.nodes.length + D.sweep.filter(function(r){return r.m>0;}).length) + ' 行';
  var w = document.querySelector('.wrapbox');
  w.id = 'leafbox';
  w.innerHTML = h;
  document.querySelector('#tb thead') && (document.querySelector('#tb thead').innerHTML = '');
}
document.querySelectorAll('.tab').forEach(function(t){
  t.onclick = function(){
    document.querySelectorAll('.tab').forEach(function(x){x.classList.remove('on');});
    t.classList.add('on');
    cur = t.dataset.t;
    var isLeaf = cur==='leaf';
    ['q','f1','f2','f3','f4'].forEach(function(id){ document.getElementById(id).style.visibility = isLeaf?'hidden':'visible'; });
    document.getElementById('f1').style.display = (cur==='eng')?'':'none';
    document.getElementById('f2').style.display = (cur==='eng')?'':'none';
    document.getElementById('f3').style.display = (cur==='plug')?'':'none';
    document.getElementById('f4').style.display = (cur==='nodes2')?'':'none';
    if (isLeaf) { showLeaf(); return; }
    restoreTable();
    render();
  };
});
(function init(){
  var s1 = document.getElementById('f1');
  %GROUPS%.forEach(function(v){ var o=document.createElement('option'); o.value=v; o.textContent=v; s1.appendChild(o); });
  var s2 = document.getElementById('f2');
  %DOMAINS%.forEach(function(v){ var o=document.createElement('option'); o.value=v; o.textContent=v; s2.appendChild(o); });
  var s3 = document.getElementById('f3');
  %CATS%.forEach(function(v){ var o=document.createElement('option'); o.value=v; o.textContent=v; s3.appendChild(o); });
  var s4 = document.getElementById('f4');
  Array.from(new Set(D.nodes2.map(function(r){return r.c;}))).sort().forEach(function(v){ var o=document.createElement('option'); o.value=v; o.textContent=v; s4.appendChild(o); });
  document.getElementById('q').oninput = render;
  ['f1','f2','f3','f4'].forEach(function(id){ document.getElementById(id).onchange = render; });
  render();
})();
"""

js = JS.replace('%DATA%', data_json).replace('%GROUPS%', groups_js).replace('%DOMAINS%', domains_js).replace('%CATS%', cats_js)

P = print
P('<!DOCTYPE html>')
P('<html lang="zh-CN">')
P('<head>')
P('<meta charset="utf-8">')
P('<meta name="viewport" content="width=device-width, initial-scale=1">')
P('<title>UE 5.8 官方 API 索引</title>')
P('<style>' + CSS + '</style>')
P('</head>')
P('<body>')
P('<h1>Unreal Engine 5.8 官方 API 索引</h1>')
P('<div class="sub">数据源：dev.epicgames.com 三套 API 参考体系全量提取（2026-10-08~10）· 引擎模块页 494/494 · 蓝图分类页 889/889 · 插件采用本机 UE_5.8 安装版 .uplugin（与文档页抽样 8/8 一致）· 分析详见 <a href="UE官方API文档分类总览.md">UE官方API文档分类总览.md</a></div>')
P('<div class="stats">')
P('<div class="stat"><b>494</b>引擎模块</div>')
P('<div class="stat"><b>%s</b>API 条目</div>' % format(tot_entries, ','))
P('<div class="stat"><b>889</b>蓝图分类 / <b>%s</b>子条目</div>' % format(bp_children, ','))
P('<div class="stat"><b>%d</b>插件（.uplugin）</div>' % len(plug_rows))
P('<div class="stat"><b>%d</b>实验/测试位</div>' % sum(r['exp'] for r in plug_rows))
P('</div>')
P('<div class="bar">')
P('<div class="tabs">')
P('<button class="tab on" data-t="eng">引擎模块 494</button>')
P('<button class="tab" data-t="bp">蓝图分类 889</button>')
P('<button class="tab" data-t="plug">插件 893</button>')
P('<button class="tab" data-t="nodes2">节点样本 600</button>')
P('<button class="tab" data-t="leaf">叶级与普查</button>')
P('</div>')
P('<input type="text" id="q" placeholder="搜索…（名称/域/位置/描述）">')
P('<select id="f1"><option value="">全部组</option></select>')
P('<select id="f2"><option value="">全部功能域</option></select>')
P('<select id="f3"><option value="">全部插件分类</option></select>')
P('<select id="f4" style="display:none"><option value="">全部分类</option></select>')
P('<span class="count" id="cnt"></span>')
P('</div>')
P('<div class="wrapbox"><table id="tb"><thead></thead><tbody></tbody></table></div>')
P('<footer>单文件零依赖 · 数据内嵌于本页（约 %d KB）· 生成器 _work/build_index.py 可重跑 · 行内 ↗ 直链官方文档页</footer>' % (len(data_json) // 1024))
P('<script>')
P(js)
P('</script>')
P('</body>')
P('</html>')
