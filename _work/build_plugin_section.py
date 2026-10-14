# -*- coding: utf-8 -*-
# 插件模块面积分析：读取 plugin_mods_dump*.json（插件模块页提取），产出 doc_data_deep6.py 所需的分析段
# 由 build_doc.py 在存在数据文件时动态调用；本文件也可独立运行打印摘要
import json, glob, sys
from collections import Counter, defaultdict

def load():
    best = {}
    for f in sorted(glob.glob('plugin_mods_dump_*.json')):
        try:
            d = json.load(open(f, encoding='utf-8'))
        except Exception:
            continue
        for it in d.get('newItems', []):
            s = it['slug']
            if s not in best or ('sections' in it and not best[s].get('sections')):
                best[s] = it
    return best

def summarize():
    best = load()
    if not best:
        print('NO DATA'); return None
    plugs = json.load(open('local_uplugins.json', encoding='utf-8'))
    mod2plug = {}
    for p in plugs:
        for m in p['modules']:
            mod2plug[m] = p['docs_name']
    exp = set(p['docs_name'] for p in plugs if p['is_experimental_dir'])

    rows = []
    for s, it in best.items():
        name = s.split('/', 1)[1]
        if it.get('status'): continue
        secs = it.get('sections', {})
        total = sum(len(v) if isinstance(v, list) else 0 for v in secs.values())
        rows.append({'name': name, 'plug': mod2plug.get(name, '?'), 'exp': mod2plug.get(name, '?') in exp,
                     'total': total, 'cls': len(secs.get('Classes', []) or []),
                     'type': it.get('type', ''), 'desc': (it.get('desc') or [''])[0][:160]})
    return rows

if __name__ == '__main__':
    rows = summarize()
    if rows:
        print('模块数:', len(rows))
        top = sorted(rows, key=lambda r: -r['total'])[:25]
        for r in top:
            print(f"  {r['name']:28s} [{r['plug']}] {'EXP' if r['exp'] else '   '} total={r['total']:4d} cls={r['cls']:4d} {r['desc'][:70]}")
        by_plug = defaultdict(lambda: [0, 0])
        for r in rows:
            by_plug[r['plug']][0] += r['total']; by_plug[r['plug']][1] += 1
        print()
        print('最重插件 Top12（按 API 条目合计）:')
        for p, (t, n) in sorted(by_plug.items(), key=lambda kv: -kv[1][0])[:12]:
            print(f'  {p}: {t} 条 / {n} 模块')
        et = [r['total'] for r in rows if r['exp']]; st = [r['total'] for r in rows if not r['exp']]
        print()
        print(f'实验插件模块 {len(et)} 个均值 {sum(et)//max(len(et),1)} 条 vs 稳定 {len(st)} 个均值 {sum(st)//max(len(st),1)} 条')
        tc = Counter(r['type'] for r in rows if r['type'])
        print('模块 Type 分布:', dict(tc.most_common(6)))
