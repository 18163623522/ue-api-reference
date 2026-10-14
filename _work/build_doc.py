# -*- coding: utf-8 -*-
# 生成 UE 官方 API 文档深度解读：分析为主体，清单为参考；结果打印到 stdout 由 shell 重定向落盘
import json, sys
from collections import Counter
from doc_data import DOMAIN_ORDER, DOMAIN_ABILITY, DOMAIN_MODULES, EDITOR_DOMAINS, DEV_DOMAINS, FEATURED, PLUGIN_HIGHLIGHTS, BP_RULES
from doc_data_deep import DEEP, EDITOR_ANALYSIS, DEV_ANALYSIS, PLUGIN_CAT_NOTES, BP_WORKFLOWS, PY_RECIPES
from doc_data_deep2 import DEEP2, EDITOR_SUB, DEV_SUB, API_SHAPE, BP_WORKFLOWS2, PY_SNIPPETS
from doc_data_deep3 import SUBSYS, ROLE_TAXONOMY, ANATOMY, ANATOMY_NOTE, EVOLUTION, LEARN_PATH
from doc_data_deep4 import SECTION_TYPES, PY_SURFACE, MODULE_GUIDE, XREF
from doc_data_deep5 import TIMELINE, COVERAGE, MATRIX
from doc_data_deep6 import PLUGIN_MOD_SURFACE
from doc_data_deep7 import CPP_LEAF, PY_LEAF
from doc_data_deep8 import BP_NODE_LEAF
from doc_data_deep9 import PY_CENSUS
from doc_data_deep10 import BP_VERBS
from doc_data_deep11 import BP_STRUCTS
from doc_data_deep12 import IFACE_ENUM

sys.stdout.reconfigure(encoding='utf-8')
NL = chr(10)
fmt = lambda x: format(x, ',')

mods = json.load(open('engine_modules_merged.json', encoding='utf-8'))
plugs = json.load(open('local_uplugins.json', encoding='utf-8'))
bp = json.load(open('bp_categories_full.json', encoding='utf-8'))
py = json.load(open('python_sections.json', encoding='utf-8'))

name2group = {}
for m in mods:
    g, n = m['slug'].split('/', 1)
    name2group[n] = g

assigned = {}
problems = []
for dom, names in list(DOMAIN_MODULES.items()) + list(EDITOR_DOMAINS.items()) + list(DEV_DOMAINS.items()):
    for n in names:
        if n not in name2group:
            problems.append(('unknown', dom, n)); continue
        if n in assigned:
            problems.append(('dup', n, assigned[n], dom)); continue
        assigned[n] = dom
unassigned = [n for n in name2group if n not in assigned]
if problems or unassigned:
    print('PROBLEMS:', problems[:10]); print('unassigned:', unassigned); raise SystemExit(1)
print('mapping OK:', len(assigned), 'modules mapped exactly once', file=sys.stderr)

sec_total = lambda m: sum(len(v) for v in m.get('sections', {}).values())
section_totals = Counter(); entry_total = 0
for m in mods:
    for k, v in m.get('sections', {}).items():
        section_totals[k] += len(v); entry_total += len(v)

plug_by_cat = Counter(p['cat'] or '(未标注)' for p in plugs)
exp_count = sum(1 for p in plugs if p['is_experimental_dir'])
bp_ok = [b for b in bp if not b.get('status')]
bp_children = sum(b.get('n_dirs', 0) + b.get('n_actions', 0) for b in bp_ok)
bp_top = sorted(bp_ok, key=lambda b: -(b.get('n_dirs', 0) + b.get('n_actions', 0)))[:20]
bp_by_slug = {b['slug']: b for b in bp_ok}
py_counts = {k: len(v) for k, v in py.items()}
py_total = sum(n for k, n in py_counts.items() if k.endswith('Types'))
plug_by_name = {p['docs_name']: p for p in plugs}

L = []; add = L.append
add('# Unreal Engine 官方 API 深度解读（分门别类 · 分析版）')
add('')
add('> **版本口径**：Epic Developer Community 文档站当前默认的 **Unreal Engine 5.8**（同站可切换 4.27 ~ 5.8）  ')
add('> **数据来源**：C++ API / Blueprint API / Python API 三套官方参考体系，494 个模块页 + 842 插件 + 889 蓝图分类 + Python 全部类型页逐页提取（2026-10-08）  ')
add('> **读法**：引号内为官方文档原文（英文原句 + 中文释义），全部来自提取数据；"机制/能做什么"为基于类清单与 Remarks 的综合归纳。第一章讲透机制与逐域分析，速查清单在 1.6 与附录。')
add('')
add('## 0. 三套 API 体系与它们的关系')
add('')
add('| 参考体系 | 入口路径 | 内容形态 | 面向场景 |')
add('|---|---|---|---|')
add('| **C++ API Reference** | `documentation/unreal-engine/API` | 按模块分组的类/结构体/枚举/函数参考，自动从引擎源码生成 | 引擎与游戏底层开发 |')
add('| **Blueprint API Reference** | `documentation/unreal-engine/BlueprintAPI` | 按分类目录组织的全部蓝图节点（889 个分类） | 无代码可视化脚本 |')
add('| **Python API Documentation** | `documentation/unreal-engine/python-api` | unreal 模块全部暴露类型（%d 个类型页，官方标注 Experimental） | 编辑器自动化脚本 |' % py_total)
add('')
add('三者的真实关系是一棵暴露树：**C++ 模块实现功能**（源头，494 个引擎模块 + 842 插件），引擎通过反射（UFUNCTION/USTRUCT/UPROPERTY）把其中设计师需要的部分**暴露成蓝图节点**（889 个分类就是这些节点的目录），又把编辑器侧对象**绑定成 Python 类**（11,675 个类型页）。所以：找"某功能有没有"查 C++ 模块；找"蓝图里怎么调"查 Blueprint 分类；找"怎么批量自动化"查 Python。同一功能三处同名或近名（如 StaticMesh → UStaticMeshComponent / BP 的 Static Mesh 分类 / unreal.StaticMesh）。')
add('')
add('## 一、C++ API：引擎的骨架（494 模块 / %s 条 API 条目）' % fmt(entry_total))
add('')
add('官方定位（根页原文）：*"This is an automatically generated reference manual from the Unreal Engine Source code."*（从 Unreal Engine 源码自动生成的参考手册。）每个模块页固定为：头部元信息（模块名/类型/源码位置/Build.cs）+ Classes、Structs、Enums、Interfaces、Functions、Delegates、Typedefs、Variables、Constants 分节表，每行"名称 + Remarks 一行官方说明"。')
add('')
add('四大模块组（官方定义）：**Runtime**（246 个，*"contains functionality necessary to run Unreal Engine"*——所有构建配置都编译）；**Editor**（139 个，编辑器内代码，仅编辑器目标）；**Developer**（109 个，*"only in non-shipping build configurations"*——不进发行包的开发工具）；**Plugins**（842 个插件/1375 插件模块，按项目启停）。合计 %s 条条目：Classes %s、Structs %s、Enums %s、Functions %s、Interfaces %s、Typedefs %s。' % (fmt(entry_total), fmt(section_totals['Classes']), fmt(section_totals['Structs']), fmt(section_totals['Enums']), fmt(section_totals['Functions']), fmt(section_totals['Interfaces']), fmt(section_totals['Typedefs'])))
add('')
add('### 1.1 先读懂四个机制（理解一切模块的钥匙）')
add('')
add('**① UObject 反射是所有 API 形态的共同前提。** UObject 是"所有 UE 对象的基类"（官方 Remarks 原文），其反射数据 UFunction 的官方说明一语道破用途：*"Reflection data for a replicated or Kismet callable function."*（描述一个可复制或蓝图可调用的函数）——即属性/函数一旦反射，就同时获得了序列化、编辑器可见、网络复制、蓝图可调四种能力。软引用 FSoftObjectPath（*"a string reference to an object, either a package, a top level asset or a subobject"*）则支撑异步加载与流送。看懂这一点，模块页里大量 U 前缀类的设计就自明了。')
add('')
add('**② Actor-Component 组合模型是玩法层的语法。** Engine 模块（全引擎最大，8,796 条）的定义链：AActor（*"can be placed or spawned in a level"*）→ UActorComponent（*"define reusable behavior that can be added to different types of Actors"*，官方明确把组件定位为跨 Actor 复用的行为单元）→ USceneComponent（*"has a transform and supports attachment, but has no rendering or collision capabilities"*）→ UPrimitiveComponent（*"contain or generate some sort of geometry, generally to be rendered or used as collision"*）。规则归属 AGameModeBase（*"defines the game being played"*），操纵归属 APlayerController → APawn → ACharacter（*"Pawns that have a mesh, collision, and built-in movement logic"*）。')
add('')
add('**③ 渲染是三层栈，扩展点在中层。** RHI 做跨 API 抽象（FDynamicRHI：*"The interface which is implemented by the dynamically bound RHI"*，其下 D3D12RHI/VulkanRHI/OpenGLDrv 为后端）；RenderCore 是公共层，顶点工厂 FVertexFactory 的官方定义（*"Encapsulates a vertex data source which can be linked into a vertex shader"*）说明它是自定义几何渲染的标准挂点；Renderer 实现场景渲染器，FCachedMeshDrawCommandInfo（*"a mesh draw command which is cached in the scene"*）体现了绘制命令缓存复用架构。日常扩展（自定义网格/后处理/插件式调试）几乎都落在 RenderCore/Renderer 层。')
add('')
add('**④ 资产管线三件套贯穿编辑器与运行时。** AssetRegistry（元数据缓存 FAssetRegistryState：*"used internally by IAssetRegistry to represent the disk cache"*）让"不加载资产就能查询资产"；Interchange 统一导入框架以节点图为核心（UInterchangeBaseNodeContainer：*"a format used to feed factories and writers when they import, reimport, and export"*）；打包分发由 PakFile/IoStore/BuildPatchServices 完成。内容浏览器、Python 资产 API、按需流送都建在这三件套上。')
add('')
add('### 1.2 API 形态：数据驱动的观察')
add('')
add('对 49,168 条条目做整体统计，能看到文档清单本身看不出来的结构规律。**类名前缀分布**（11,933 个类）：')
add('')
add('| 前缀 | 类数 | 占比 | 说明 |')
add('|---|---|---|---|')
for name, n, pct, note in API_SHAPE[0][1]:
    pct_s = ('%d%%' % pct) if pct else '另计'
    add('| %s | %s | %s | %s |' % (name, fmt(n), pct_s, note))
add('')
for line in API_SHAPE[1][1]:
    add('- %s' % line)
add('')
add('#### 1.2.1 角色分类学：后缀即职能')
add('')
add('类名后缀是第二层索引（统计口径：11,933 个类）：')
add('')
add('| 后缀/角色 | 类数 | 职能与用法 |')
add('|---|---|---|')
for name, n, note in ROLE_TAXONOMY:
    add('| %s | %s | %s |' % (name, fmt(n), note))
add('')
add('#### 1.2.2 Subsystem：按生命周期自动管理的服务（85 个）')
add('')
add(SUBSYS['intro'])
add('')
add('| 家族 | 生命周期 | 适用场景 |')
add('|---|---|---|')
for fam, scope, use in SUBSYS['families']:
    add('| **%s** | %s | %s |' % (fam, scope, use))
add('')
add('数据面：%s' % SUBSYS['stats'])
add('')
for mod, name, en, zh in SUBSYS['quotes']:
    add('- `%s`（%s）：*"%s"*——%s' % (name, mod, en, zh))
add('')
add('**怎么用**：%s' % '；'.join(SUBSYS['uses']))
add('')
add('#### 1.2.3 Top 模块解剖：反射密度谱')
add('')
add(ANATOMY_NOTE)
add('')
add('| 模块 | 类数 | 反射类(U/A)% | F 类% | S 类% | 解读 |')
add('|---|---|---|---|---|---|')
for name, n, r, f, s, note in ANATOMY:
    add('| %s | %s | %d%% | %d%% | %d%% | %s |' % (name, fmt(n), r, f, s, note))
add('')
add('#### 1.2.4 条目类型分布：数据重的模块与行为重的模块')
add('')
add(SECTION_TYPES['intro'])
add('')
add('| 模块 | Structs | Classes | 比值 | 模块性格 |')
add('|---|---|---|---|---|')
for name, s, c, ratio, note in SECTION_TYPES['struct_heavy']:
    add('| %s | %s | %s | %.1f | %s |' % (name, fmt(s), fmt(c), ratio, note))
add('')
add(SECTION_TYPES['iface_dense'])
add('')
add('#### 1.2.5 文档自身的覆盖质量（元分析）')
add('')
add('这套数据还能反过来度量**官方文档本身**：每条 Classes/Structs/Functions 条目在模块页上是否带 Remarks 说明文字。全引擎口径：')
add('')
for name, val, note in COVERAGE['headline']:
    add('- **%s：%s**——%s' % (name, val, note))
add('')
add(COVERAGE['domain_note'])
add('')
dom_cov = {}
for dom, names in DOMAIN_MODULES.items():
    tot = 0; has = 0
    for n in names:
        for grp in ('Runtime', 'Editor', 'Developer'):
            m = next((x for x in mods if x['slug'] == grp + '/' + n), None)
            if m:
                rows = m.get('sections', {}).get('Classes', [])
                tot += len(rows); has += sum(1 for _, r in rows if r.strip())
                break
    dom_cov[dom] = (has, tot, has * 100 // max(tot, 1))
add('| 功能域 | Classes Remarks 覆盖 | 功能域 | Classes Remarks 覆盖 |')
add('|---|---|---|---|')
cov_sorted = sorted(dom_cov.items(), key=lambda kv: -kv[1][2])
half_c = (len(cov_sorted) + 1) // 2
for i in range(half_c):
    d1, v1 = cov_sorted[i]
    d2, v2 = cov_sorted[i + half_c] if i + half_c < len(cov_sorted) else (None, None)
    if d2: add('| %s | %d%% (%s/%s) | %s | %d%% (%s/%s) |' % (d1, v1[2], fmt(v1[0]), fmt(v1[1]), d2, v2[2], fmt(v2[0]), fmt(v2[1])))
    else: add('| %s | %d%% (%s/%s) | | |' % (d1, v1[2], fmt(v1[0]), fmt(v1[1])))
add('')
add(COVERAGE['advice'])
add('')
add('### 1.3 十九个功能域逐域分析')
add('')
add('> 域划分为本文归纳（官方无此维度）；每域给出机制 → 代表 API（官方引文）→ 能做什么。模块数 (R/E/D) 标注构建组分布。')
add('')
for dom in DOMAIN_ORDER:
    names = DOMAIN_MODULES[dom]
    groups = Counter(name2group[n] for n in names)
    g = '%d/%d/%d' % (groups.get('Runtime', 0), groups.get('Editor', 0), groups.get('Developer', 0))
    d = DEEP.get(dom, {})
    add('#### %s（%d 个模块，R/E/D=%s）' % (dom, len(names), g))
    add('')
    add('**机制**：%s' % d.get('mech', ''))
    add('')
    qs = [q for q in d.get('quotes', []) if q[2]] + [q for q in DEEP2.get(dom, {}).get('quotes', []) if q[2]]
    if qs:
        add('**代表 API（官方 Remarks 原文）**：')
        add('')
        for mod, name, en, zh in qs:
            add('- `%s`（%s）：*"%s"*——%s' % (name, mod, en, zh))
        add('')
    us = d.get('uses', [])
    if us:
        add('**能做什么**：' + '；'.join(us) + '。')
        add('')
add('### 1.4 Editor 组逐子域分析（139 个模块，8 个子域）')
add('')
for name, n, mech, quotes, uses in EDITOR_SUB:
    add('#### %s（%d 个模块）' % (name, n))
    add('')
    add('**机制**：%s' % mech)
    add('')
    if quotes:
        for mod, cname, en, zh in quotes:
            add('- `%s`（%s）：*"%s"*——%s' % (cname, mod, en, zh))
        add('')
    add('**能做什么**：' + '；'.join(uses) + '。')
    add('')
add('### 1.5 Developer 组逐子域分析（109 个模块，8 个子域）')
add('')
for name, n, mech, quotes, uses in DEV_SUB:
    add('#### %s（%d 个模块）' % (name, n))
    add('')
    add('**机制**：%s' % mech)
    add('')
    if quotes:
        for mod, cname, en, zh in quotes:
            add('- `%s`（%s）：*"%s"*——%s' % (cname, mod, en, zh))
        add('')
    add('**能做什么**：' + '；'.join(uses) + '。')
    add('')
add('### 1.6 速查：域总表与模块全清单')
add('')
add('#### 1.6.1 功能域总表')
add('')
add('| 功能域 | 模块数 | 代表模块 | 一句话能力 |')
add('|---|---|---|---|')
for dom in DOMAIN_ORDER:
    names = DOMAIN_MODULES[dom]
    reps = ', '.join(names[:5]) + ('…' if len(names) > 5 else '')
    add('| **%s** | %d | %s | %s |' % (dom, len(names), reps, DOMAIN_ABILITY[dom]))
add('')
add('#### 1.6.2 API 面积 Top 25 模块')
add('')
add('| # | 模块 | 组 | 总条目 | Classes | Structs | Enums | Functions |')
add('|---|---|---|---|---|---|---|---|')
for i, m in enumerate(sorted(mods, key=lambda m: -sec_total(m))[:25], 1):
    s = m.get('sections', {})
    add('| %d | %s | %s | %s | %s | %s | %s | %s |' % (i, m['slug'].split('/')[1], m['slug'].split('/')[0], fmt(sec_total(m)), fmt(len(s.get('Classes', []))), fmt(len(s.get('Structs', []))), fmt(len(s.get('Enums', []))), fmt(len(s.get('Functions', [])))))
add('')
add('解读（综合判断）：Engine/Core/CoreUObject 三巨头贡献约 1.7 万条条目，是游戏框架与对象系统的绝对核心；Chaos（物理）与 RenderCore/RHI（渲染）的体量说明二者仍是 5.x 的扩张主战场；VerseCompiler 进入前 11，反映 Verse 语言在引擎内的权重。')
add('')
add('#### 1.6.3 重点模块速览')
add('')
for name, related, desc in FEATURED:
    extra = '（关联：%s）' % ', '.join(related) if related else ''
    add('- **%s**%s——%s' % (name, extra, desc))
add('')
add('<details><summary>各域完整模块清单（点开展开）</summary>')
add('')
for dom in DOMAIN_ORDER:
    names = DOMAIN_MODULES[dom]
    add('- **%s**（%d）：%s' % (dom, len(names), ', '.join(names)))
add('')
add('</details>')
add('')
add('#### 1.6.4 各域学习路径（先读哪三个类）')
add('')
add('| 域 | 模块 | 阅读顺序 |')
add('|---|---|---|')
for dom, mod, path in LEARN_PATH:
    add('| %s | %s | %s |' % (dom, mod, path))
add('')
add('#### 1.6.5 核心模块内部导览（类与官方 Remarks）')
add('')
for mod, entries in MODULE_GUIDE:
    add('**%s**' % mod)
    add('')
    for cname, en, zh in entries:
        add('- `%s`：*"%s"*——%s' % (cname, en, zh))
    add('')
try:
    cpp_leaf = json.load(open('cpp_leaf_summary.json', encoding='utf-8'))
    add('#### 1.6.6 核心类成员面（叶级抽样，32 类）')
    add('')
    add(CPP_LEAF['intro'])
    add('')
    add('| 类 | 模块 | 函数 | 变量 | 派生类 | 类 | 模块 | 函数 | 变量 | 派生类 |')
    add('|---|---|---|---|---|---|---|---|---|---|')
    half = (len(cpp_leaf) + 1) // 2
    for i in range(half):
        a = cpp_leaf[i]
        b = cpp_leaf[i + half] if i + half < len(cpp_leaf) else None
        if b:
            add('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (a['name'], a['mod'], fmt(a['funcs']), fmt(a['vars']), fmt(a['derived']), b['name'], b['mod'], fmt(b['funcs']), fmt(b['vars']), fmt(b['derived'])))
        else:
            add('| %s | %s | %s | %s | %s | | | | | |' % (a['name'], a['mod'], fmt(a['funcs']), fmt(a['vars']), fmt(a['derived'])))
    add('')
    for line in CPP_LEAF['findings']:
        add('- %s' % line)
    add('')
    add(CPP_LEAF['quote_note'])
    add('')
except FileNotFoundError:
    pass

add('### 1.7 官方插件生态：842 个插件按类能给什么能力')
add('')
add('文档站 PluginIndex 收录 842 个官方插件（1375 个插件模块）；本机 5.8 安装版实测 893 个 `.uplugin`（抽 8 个与文档页逐字节比对一致，见附录）。287 个位于 Experimental/Beta 目录（约三分之一，选用需评估）。主要分类的能力画像（描述为官方原文）：')
add('')
for cat, n, note in PLUGIN_CAT_NOTES:
    add('**%s（%d 个）**——%s' % (cat, n, note))
    add('')
add('其余分类：Messaging 15、Insights 13、Platform 9、Codecs 6、Mobile 6、Blueprints 5、Performance 5、Device Profile Selectors 5、Augmented Reality 5、Content Browser 4、Build Distribution 4、Database 4、Examples 3、Accessibility 3、Compression 2、Localization 2、Learning 2、Dataprep 2、Telemetry 2、2D 1（Paper2D "tools and assets to help create 2D games"）等。全量计数表见附录数据文件。')
add('')
try:
    pm_rows = json.load(open('plugin_mods_local.json', encoding='utf-8'))
    pm_rows.sort(key=lambda r: -r['total'])
    add('#### 1.7.1 插件模块反射面排行（本地源码口径）')
    add('')
    add(PLUGIN_MOD_SURFACE['intro'])
    add('')
    add(PLUGIN_MOD_SURFACE['anchor'])
    add('')
    add('| 插件模块 | 所属插件 | 实验位 | UCLASS | USTRUCT | UENUM | UINTERFACE | 合计 |')
    add('|---|---|---|---|---|---|---|---|')
    for r in pm_rows[:20]:
        add('| %s | %s | %s | %d | %d | %d | %d | **%d** |' % (r['name'], r['plug'], 'EXP' if r['exp'] else '', r['uclass'], r['ustruct'], r['uenum'], r['uinterface'], r['total']))
    add('')
    for line in PLUGIN_MOD_SURFACE['findings']:
        add('- %s' % line)
    add('')
except FileNotFoundError:
    pass
add('')
add('## 二、Blueprint API：设计师看到的那一面（889 个分类）')
add('')
add('蓝图 API 参考是全部蓝图节点的目录树。根页官方声明：*"The Blueprint API reference is an early work in progress — it strives to reflect all available nodes, but it is not guaranteed to be an exhaustive list."*（仍在早期建设，力求全量但不保证穷尽。）规模：889 个分类页**已全量抓取**，合计 %s 个子条目（子分类+节点页）。子条目最多的分类：' % fmt(bp_children))
add('')
add('| 分类 | 子条目 | 分类 | 子条目 |')
add('|---|---|---|---|')
for i in range(0, 20, 2):
    a = bp_top[i]; b = bp_top[i + 1] if i + 1 < 20 else None
    an = a.get('n_dirs', 0) + a.get('n_actions', 0)
    if b: add('| %s | %d | %s | %d |' % (a['slug'], an, b['slug'], b.get('n_dirs', 0) + b.get('n_actions', 0)))
    else: add('| %s | %d | | |' % (a['slug'], an))
add('')
add('### 2.1 十六个典型工作流（节点名均取自抓取数据）')
add('')
for title, cat, desc in BP_WORKFLOWS2:
    add('**%s**（%s）——%s' % (title, cat, desc))
    add('')
add('### 2.2 全分类的功能域覆盖（关键词归纳）')
add('')
allnames = [b['slug'] for b in bp]
import re as _re
_tok = lambda n: [t.lower() for t in _re.findall('[A-Z]+(?![a-z])|[A-Z][a-z]+|[a-z]+', n.replace('_', ' '))]
for cname, kws in BP_RULES:
    ks = [k.lower() for k in kws]
    hit = sorted(set(n for n in allnames if any(any(t == k or (len(k) >= 3 and t.startswith(k)) for t in _tok(n)) for k in ks)))
    add('- **%s**：%d 个分类，如 %s%s' % (cname, len(hit), ', '.join(hit[:8]), '…' if len(hit) > 8 else ''))
add('')
try:
    bp_nodes = json.load(open('bp_node_leaf.json', encoding='utf-8'))
    add('### 2.3 节点详情页抽样（叶级，18 个）')
    add('')
    add(BP_NODE_LEAF['intro'])
    add('')
    for line in BP_NODE_LEAF['findings']:
        add('- %s' % line)
    add('')
except FileNotFoundError:
    pass

try:
    bn = json.load(open('bp_nodes_all.json', encoding='utf-8'))
    from collections import Counter as _C
    _hosts = _C(r['t'] for r in bn if r.get('t'))
    _cats = _C(r['s'].split('/')[0] for r in bn)
    _dirs = sum(1 for r in bn if r.get('dir'))
    add('### 2.4 节点宿主分布（Target is 统计）')
    add('')
    add('用节点页的 "Target is X" 行做宿主普查（BP→C++ 暴露树的量化）。当前样本 %d 个节点页（覆盖分类：%s；其中 %d 个为目录页无宿主，%d 个带 Target 声明）：' % (len(bn), '、'.join('%s %d' % kv for kv in _cats.most_common()), _dirs, sum(_hosts.values())))
    add('')
    add('| C++ 宿主 | 节点数 | C++ 宿主 | 节点数 |')
    add('|---|---|---|---|')
    hl = _hosts.most_common()
    half_h = (len(hl) + 1) // 2
    for i in range(half_h):
        a = hl[i]
        b = hl[i + half_h] if i + half_h < len(hl) else None
        if b: add('| %s | %d | %s | %d |' % (a[0], a[1], b[0], b[1]))
        else: add('| %s | %d | | |' % (a[0], a[1]))
    add('')
    add('**宿主的模块归属**（把 78 个宿主类名反查回引擎模块/插件）：**Engine 仍是最大承接方**（扩容样本中约六成），插件生态承接约两成（Niagara/TakeRecorder/Mover/SmartObjects 系为主），其余分给 GameplayTags/UMG/AIModule/Splines 等专项模块。蓝图的动作面高度依赖 Engine 这个“万能门户”+ 各域自己的插件。')
    add('')
    add('解读（1,296 节点/28 分类样本）：**两种宿主形态平分秋色——函数库与组件/对象**。库侧：Kismet System Library 84、Gameplay Statics 66、Draw Debug Library 63、Level Sequence Shot Meta Data Library 35；对象侧：Spline Component 64、Primitive Component 61、Take Recorder Subsystem 41、Static Mesh 30、Niagara Particle System Component 25。**“领域库+领域对象”配对在每个域成立**：GameplayTags=库 27+接口 6、Niagara=组件 25+库 5、Game=Game Mode Base 13+Level Streaming 6+GAS 库 5、AI=AIController 8+辅助库 11。全部 1,160 个带声明的节点仅由 179 个 C++ 宿主承接（Top3 占 18%——扩容后长尾更明显：门户类仍集中，但各域专属宿主大量涌现）——蓝图的动作面在 C++ 侧高度集中于少数“门户类”。')
    add('')
except FileNotFoundError:
    pass

try:
    verbs = json.load(open('bp_verbs.json', encoding='utf-8'))
    add('### 2.5 蓝图动词词表（零网络分析）')
    add('')
    add(BP_VERBS['intro'])
    add('')
    add('| 动词 | 节点数 | 动词 | 节点数 | 动词 | 节点数 |')
    add('|---|---|---|---|---|---|')
    vt = verbs['verb_top30']
    third = (len(vt) + 2) // 3
    for i in range(third):
        cells = '%s | %d' % (vt[i][0], vt[i][1])
        for j in (1, 2):
            k = i + j * third
            if k < len(vt): cells += ' | %s | %d' % (vt[k][0], vt[k][1])
        while cells.count('|') < 5: cells += ' | '
        add('| ' + cells + ' |')
    add('')
    for line in BP_VERBS['findings']:
        add('- %s' % line)
    add('')
except FileNotFoundError:
    pass

try:
    add('### 2.6 结构体命名模式（零网络分析）')
    add('')
    add(BP_STRUCTS['intro'])
    add('')
    for line in BP_STRUCTS['findings']:
        add('- %s' % line)
    add('')
except FileNotFoundError:
    pass

try:
    add('### 2.7 接口与枚举的命名模式（零网络分析）')
    add('')
    add(IFACE_ENUM['iface_intro'])
    add('')
    for line in IFACE_ENUM['iface_findings']:
        add('- %s' % line)
    add('')
    add(IFACE_ENUM['enum_intro'])
    add('')
    for line in IFACE_ENUM['enum_findings']:
        add('- %s' % line)
    add('')
except FileNotFoundError:
    pass

add('## 三、Python API：编辑器自动化面（unreal 模块，Experimental）')
add('')
add('整站即一个 `unreal` 模块（Sphinx 文档，标题自带 *Unreal Python 5.8 (Experimental)*）。类型面：Class %s、Struct %s、Enum %s、Delegate %s、Native %d，合计 %d 个类型页。' % (fmt(py_counts.get('Class Types', 0)), fmt(py_counts.get('Struct Types', 0)), fmt(py_counts.get('Enum Types', 0)), fmt(py_counts.get('Delegate Types', 0)), py_counts.get('Native Types', 0), py_total))
add('')
add('常用入口类（均已核验存在）：`unreal.EditorAssetLibrary`（资产增删改查）、`unreal.AssetEditorSubsystem`、`unreal.LevelEditorSubsystem`、`unreal.UnrealEditorSubsystem`、`unreal.EditorLevelLibrary`（旧入口）、`unreal.AssetRegistryHelpers`、`unreal.MaterialEditingLibrary`、`unreal.StaticMeshEditorSubsystem` / `SkeletalMeshEditorSubsystem`、`unreal.EditorUtilityLibrary`、`unreal.SystemLibrary`。')
add('')
add('### 3.1 八个典型自动化配方（代码行为示意片段，以官方类名为准）')
add('')
for title, api, desc, code in PY_SNIPPETS:
    add('**%s**（%s）——%s' % (title, api, desc))
    add('')
    add('```python')
    add(code)
    add('```')
    add('')
add('**边界**：仅编辑器进程内可用，打包后的游戏不含 Python 运行时；逐帧/实时逻辑不适用（那是 C++/蓝图的地盘）。')
add('')
add('### 3.2 Python 面的形态：数据说了什么')
add('')
add('对 5,149 个类的名字做主题前缀统计，能看出 Python 面的倾斜：')
add('')
add('| 前缀群 | 类数 | 前缀群 | 类数 |')
add('|---|---|---|---|')
th = PY_SURFACE['theme']
half2 = (len(th) + 1) // 2
for i in range(half2):
    l = th[i]; r = th[i + half2] if i + half2 < len(th) else None
    if r: add('| %s* | %d | %s* | %d |' % (l[0], l[1], r[0], r[1]))
    else: add('| %s* | %d | | |' % (l[0], l[1]))
add('')
for f in PY_SURFACE['facts']:
    add('- %s' % f)
add('')
try:
    py_leaf = json.load(open('py_leaf.json', encoding='utf-8'))
    add('### 3.3 主力类成员数排行（28 类叶级抽样）')
    add('')
    add(PY_LEAF['intro'])
    add('')
    add('| unreal 类 | 成员数* | 基类 | 备注 |')
    add('|---|---|---|---|')
    for r in py_leaf:
        add('| %s | %s | %s | %s |' % (r['name'], fmt(r['members']), r['bases'], r['note']))
    add('')
    add('（*dt 条目计数，含方法与属性；资产类以属性为主，函数库/子系统类以方法为主。）')
    add('')
    for line in PY_LEAF['findings']:
        add('- %s' % line)
    add('')
except FileNotFoundError:
    pass

try:
    census = json.load(open('py_sweep_full.json', encoding='utf-8'))
    add('### 3.4 Python 动作类全量普查（250 个 Library/Subsystem）')
    add('')
    add(PY_CENSUS['intro'])
    add('')
    add('| unreal 动作类 | 成员数 | unreal 动作类 | 成员数 | unreal 动作类 | 成员数 |')
    add('|---|---|---|---|---|---|')
    ok = [r for r in census if r['m'] > 0]
    third = (len(ok) + 2) // 3
    for i in range(third):
        a = ok[i]
        b = ok[i + third] if i + third < len(ok) else None
        c = ok[i + 2 * third] if i + 2 * third < len(ok) else None
        cells = '%s | %d' % (a['name'], a['m'])
        if b: cells += ' | %s | %d' % (b['name'], b['m'])
        if c: cells += ' | %s | %d' % (c['name'], c['m'])
        while cells.count('|') < 5:
            cells += ' | '
        add('| ' + cells + ' |')
    add('')
    for line in PY_CENSUS['findings']:
        add('- %s' % line)
    add('')
except FileNotFoundError:
    pass

add('## 四、三套 API 选型与组合')
add('')
add('| 维度 | C++ | Blueprint | Python |')
add('|---|---|---|---|')
add('| 运行环境 | 游戏+编辑器 | 游戏+编辑器 | 仅编辑器 |')
add('| 性能 | 原生 | 有 VM 开销（逐帧逻辑敏感） | 脚本级（不适合逐帧） |')
add('| 适合 | 引擎改造/底层系统/性能热点 | 玩法组装/原型/设计师协作 | 批处理/资产管线/自动化 |')
add('| 入口形态 | 模块+类 | 889 个节点分类 | unreal 模块 %d 个类型 |' % py_total)
add('| 学习曲线 | 高 | 低 | 低（会 Python 即可） |')
add('')
add('**组合模式（工程常态）**：C++ 写能力层（UFUNCTION/UPROPERTY 反射暴露）→ 蓝图组装玩法与调参 → Python 做资产管线与 CI。同一件事的三种做法——给关卡内所有 StaticMesh 设置碰撞：C++ 遍历 `UStaticMeshComponent`；蓝图用 `Static Mesh` 分类设置节点；Python 用 `unreal.LevelEditorSubsystem` 取关卡遍历设置。')
add('')
add('### 4.1 同一功能的三层对照表（20 个高频功能）')
add('')
add('| 功能 | C++ 侧 | Blueprint 侧 | Python 侧 |')
add('|---|---|---|---|')
for feat, cpp, bp_side, py_ in XREF:
    add('| **%s** | %s | %s | %s |' % (feat, cpp, bp_side, py_))
add('')
add('### 4.2 域能力矩阵：四路数据按 19 域合流')
add('')
add(MATRIX['intro'])
add('')
import re as _re2
_tok2 = lambda n: [t.lower() for t in _re2.findall('[A-Z]+(?![a-z])|[A-Z][a-z]+|[a-z]+', n.replace('_', ' '))]
BP_KEYS_M = {
 '核心与运行时基础': ['Math','Guid','String','Array','Utilities','Date Time','Random'],
 '游戏框架与玩法': ['Game','Gameplay','Actor','Level','Spawning','Pawn','Character','Controller','Save Game','Damage'],
 '输入与 XR 设备': ['Input','Enhanced Input','XR','AR','Head Mounted','Motion Controller','Eye Tracking'],
 '渲染与图形': ['Rendering','Material','Texture','Lighting','Lights','Nanite','Virtual Texture','Ray Tracing','Render'],
 '物理与碰撞': ['Physics','Collision','Constraint','Buoyancy','Chaos','Field'],
 '几何与建模': ['Geometry','Dynamic Mesh','Mesh Description','Modeling','Spline'],
 'UI 界面': ['Widget','UMG','Slate','Text','Button','Panel','Layout'],
 '动画与布料': ['Anim','Animation','Pose','Skeleton','Montage','IK','Retarget','Live Link','Cloth','Motion'],
 'Sequencer 与影视虚拟制片': ['Sequencer','Cine','Movie','Take','Camera','Virtual Production','Composure','NDisplay'],
 '音频': ['Audio','Sound','Meta Sound','Music','Submix','Synth'],
 'AI 与导航': ['AI','Blackboard','Behavior','Navigation','EQS','Crowd','Smart Object','Targeting'],
 '网络与在线服务': ['Networking','Replication','Online','Multi','Replay','Pixel Streaming'],
 '媒体播放': ['Media','Video','Image'],
 '地形与植被': ['Landscape','Foliage','Landmass','Water'],
 'Mass 实体系统': ['Mass'],
 '资产与内容管线': ['Asset','Data Table','Import','Dataprep','Interchange','Content Browser'],
 '遥测与性能分析': ['Perf','Performance','Insights','Profiling','Telemetry','Debug'],
 '自动化测试': ['Automation','Test','Assert'],
 '新兴与实验技术': ['Learning','Python','ML'],
}
PY_PREFIX_M = {
 '游戏框架与玩法': ['Gameplay','Actor','Level','Pawn','Character','GameMode','SaveGame'],
 '输入与 XR 设备': ['EnhancedInput','Input'],
 '渲染与图形': ['Material','Texture','Light'],
 '物理与碰撞': ['Physics','GeometryCollection'],
 '几何与建模': ['Mesh','DynamicMesh','Geometry'],
 'UI 界面': ['Widget','UserWidget','UMG'],
 '动画与布料': ['Anim','Animation','Control'],
 'Sequencer 与影视虚拟制片': ['LevelSequence','MovieScene','Sequencer','Cine'],
 '音频': ['Audio','Metasound','Sound','Submix'],
 'AI 与导航': ['AI','Nav'],
 '媒体播放': ['Media'],
 '地形与植被': ['Landscape','Foliage'],
 'Mass 实体系统': ['Mass'],
 '资产与内容管线': ['Asset','Data'],
 '新兴与实验技术': ['NNE','Learning'],
}
PLUG_CATS_M = {
 '游戏框架与玩法': ['Gameplay'], '输入与 XR 设备': ['Input Devices','Virtual Reality'],
 '渲染与图形': ['Rendering'], '物理与碰撞': ['Physics'], '几何与建模': ['Geometry'],
 'UI 界面': ['UI'], '动画与布料': ['Animation'], 'Sequencer 与影视虚拟制片': ['Virtual Production'],
 '音频': ['Audio'], 'AI 与导航': ['AI'], '网络与在线服务': ['Networking','Online Platform'],
 '媒体播放': ['Media Players'], '地形与植被': ['Water'], '资产与内容管线': ['Importers'],
 '遥测与性能分析': ['Insights','Performance','Telemetry'], '自动化测试': ['Testing'], '新兴与实验技术': ['ML'],
}
add('| 功能域 | C++ 模块 | C++ 条目 | BP 分类* | BP 子项* | Python 类* | 插件 |')
add('|---|---|---|---|---|---|---|')
for dom in DOMAIN_ORDER:
    names = DOMAIN_MODULES[dom]
    entries = 0
    for n in names:
        for grp in ('Runtime', 'Editor', 'Developer'):
            m = next((x for x in mods if x['slug'] == grp + '/' + n), None)
            if m:
                entries += sum(len(v) for v in m.get('sections', {}).values())
                break
    keys = BP_KEYS_M.get(dom, [])
    hits = [b for b in bp_ok for k in keys if any(t == k.lower() or (len(k) >= 4 and t.startswith(k.lower())) for t in _tok2(b['slug']))]
    nb = len(hits); cb = sum(b.get('n_dirs', 0) + b.get('n_actions', 0) for b in hits)
    prefs = PY_PREFIX_M.get(dom, [])
    np_ = sum(1 for c in py.get('Class Types', []) if any(c.startswith(p) for p in prefs))
    npl = sum(plug_by_cat.get(c, 0) for c in PLUG_CATS_M.get(dom, []))
    add('| %s | %d | %s | %d | %s | %d | %d |' % (dom, len(names), fmt(entries), nb, fmt(cb), np_, npl or 0))
add('')
add('（带 * 三列为启发式归类：BP 按分类名关键词、Python 按类名前缀、插件按官方分类映射；一个条目可计入多个域，量级可信、绝对值勿较真。C++ 两列为精确计数。）')
add('')
for line in MATRIX['reading']:
    add('- %s' % line)
add('')
add('## 五、版本口径与 4.27 → 5.8 模块演化（数据差分）')
add('')
add('文档站 all_versions 实测支持：**5.8（当前默认）/ 5.7 / 5.6 / 5.5 / 5.4 / 5.3 / 5.2 / 5.1 / 5.0 / 4.27**。本文全部数字基于 5.8。用 4.27 的组页名单与 5.8 差分（4.27 组页经 `application_version=4.27` 参数抓取，与 5.8 同接口同口径），可以量化 UE5 时代引擎模块的演化：')
add('')
add('**总量**：%s' % EVOLUTION['counts'])
add('')
add('**模块入场时间线（四快照点仲裁）**：%s' % TIMELINE['meta'])
add('')
add('| 入场窗口 | 模块数 (D/E/R) | 代表模块 | 解读 |')
add('|---|---|---|---|')
for w, n, der, mods_, note in TIMELINE['buckets']:
    add('| **%s** | %d (%s) | %s | %s |' % (w, n, der, mods_, note))
add('')
add(TIMELINE['moves'])
add('')
add('**Runtime 组 +72 个新模块，按主题成批出现**（UE5 时代的主战场）：')
add('')
for theme, mods_, note in EVOLUTION['runtime_added_themes']:
    add('- **%s**（%s）——%s' % (theme, ', '.join(mods_), note))
add('')
add('**Developer 组换代**：%s' % EVOLUTION['dev_shift'])
add('')
add('**Editor 组**：%s' % EVOLUTION['editor_shift'])
add('')
add('**插件层新生与死亡**：%s' % EVOLUTION['plugin_births'])
add('')
add('**确认退役**：%s' % EVOLUTION['plugin_deaths'])
add('')
add('## 附录：数据与核验')
add('')
add('**数据文件**（`_work/`）：`engine_modules_merged.json`（494 模块页完整提取，条目带官方 Remarks）、`local_uplugins.json`（本机 5.8 版 %d 个 .uplugin）、`bp_categories_full.json`（889 蓝图分类页全量）、`python_sections.json`（Python API 类型清单）、`diff_427_58.json` + `groups_427.json` + `groups_versions.json` + `module_timeline.json`（版本组页/差分/入场时间线；5.0 实测回退 4.27 快照）、`plugin_mods_local.json`（插件模块反射面 262 个）、`cpp_leaf_summary.json` + `py_leaf.json` + `py_sweep_full.json`（叶级：32 C++ 类 + 28 Python 类 + 250 动作类普查）、`bp_node_leaf.json` + `bp_nodes_all.json`（节点页 600 个含宿主声明）、`doc_data*.py`/`build_doc.py`（生成器，含 494 模块恰好归一域校验）。' % len(plugs))
add('')
add('**核验方式**：')
add('')
add('1. 数据经真实浏览器会话从文档站 `document.json` 接口逐页提取，494 个引擎模块页全量命中、零失败；')
add('2. 插件：抽 8 个文档页描述/分类与本机 UE_5.8 `.uplugin` 逐字节比对，8/8 一致，统计采用本地全量；')
add('3. 正文所有类名与英文引文（AActor/UFunction/FSoftObjectPath/AGameModeBase/FDynamicRHI/FVertexFactory/SWindow/UUserWidget/UMovieScene/AAIController/FGuidReferences/UMassEntitySubsystem/UInterchangeBaseNodeContainer/UNNEModelData 等）均直接取自提取数据；')
if len(bp) - len(bp_ok) == 0:
    add('4. 蓝图 889 个分类页**全量抓取完成**（含 Add* 系列实测 0 子项的图菜单占位分类），合计 %s 个子条目（子分类+节点页）；' % fmt(bp_children))
else:
    add('4. 蓝图 %d 个分类页因站点限流（HTTP 429）未取回，蓝图统计基于已取回的 %d 个分类，已如实标注；' % (len(bp) - len(bp_ok), len(bp_ok)))
add('5. 机制/能做什么/工作流为综合归纳（官方无此维度），模块域归属经脚本校验（494 恰好各归一域）。')

# 自动生成目录（## 与 ### 两级，GitHub 风格锚点）
import re as _re_toc
def _slug(t):
    t = t.strip().lower()
    t = _re_toc.sub(r'[.,/：:·()（）?？*`\[\]]', '', t)
    t = t.replace(' ', '-')
    return t
_toc = ['## 目录', '']
for _ln in L:
    if _ln.startswith('## ') and not _ln.startswith('## 目录'):
        _t = _ln[3:].strip()
        _toc.append('- [%s](#%s)' % (_t, _slug(_t)))
    elif _ln.startswith('### '):
        _t = _ln[4:].strip()
        _toc.append('  - [%s](#%s)' % (_t, _slug(_t)))
_toc.append('')
# 插入到第一个 '## 0.' 之前
_idx = L.index('## 0. 三套 API 体系与它们的关系')
L[_idx:_idx] = _toc

print(NL.join(L))
