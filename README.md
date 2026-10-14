# ue-api-reference-summary

Unreal Engine 官方 API 文档的深度解读与全量提取数据（基准版本 UE 5.8，抓取日期 2026-10-08）。

## 成品交付

- [UE-API索引.html](UE-API索引.html) —— **可查询单文件索引页**（零依赖，数据内嵌）：五个页签（引擎模块 494 / 蓝图分类 889 / 插件 893 / **节点样本 533（可按 Target 宿主搜索）** / 叶级与普查 294 + 宿主分布 78），全局搜索 + 组/功能域/插件分类/节点分类筛选 + 任意列排序，每行 ↗ 直链官方文档页。生成器 `_work/build_index.py`。

- [UE官方API文档分类总览.md](UE官方API文档分类总览.md) —— **详细分析版**（1363 行）：
  - 第 0 章：三套 API 体系（C++ / Blueprint / Python）的"暴露树"关系
  - 第 1 章 C++ API（494 模块 / 49,168 条目）：
    - 1.1 四个核心机制（UObject 反射 / Actor-Component / 渲染三层栈 / 资产管线三件套）
    - 1.2 API 形态数据观察：前缀分布 + 角色分类学 + Subsystem 体系专节 + 反射密度谱 + 条目类型分布（数据重 vs 行为重）+ **文档覆盖质量元分析**（Classes Remarks 52% vs Functions 96%、分域覆盖率表）
    - 1.3 十九个功能域逐域分析（机制 → 官方引文代表 API → 能做什么）
    - 1.4/1.5 Editor 组与 Developer 组各八个子域逐个分析
    - 1.6 速查（域总表 / Top25 / 重点模块 / 学习路径 / 核心模块内部导览 / **核心类成员面（32 类叶级抽样：AActor 643 函数 210 派生、UObject 2001 派生）** / 全清单）；1.7 插件分类能力画像（22 类）+ **1.7.1 插件模块反射面排行**（本地源码口径：PCG 852 > ControlRig 729 > Niagara 670，实验/稳定体量差一倍）
  - 第 2 章 Blueprint：十六个典型工作流（真实节点名，含智能对象/样条/程序化网格/Take Recorder）+ 域聚类覆盖（**889/889 分类页全量抓取完成**，14,613 子条目）+ **2.3 节点详情页抽样**（"Target is X"=BP→C++ 溯源锚点、逐引脚 tooltip）+ **2.4 节点宿主分布**（1,296 节点/28 分类：函数库与组件双形态、领域库+领域对象配对、1,160 声明由 179 个宿主承接）+ **2.5 蓝图动词词表**（Get 35% / 读：写=3:2 / 约 30 词迷你语言 / 跨分类重名 589 个）
  - 第 3 章 Python：八个自动化配方（示意代码）+ Python 面形态分析 + 3.3 主力类成员数排行（28 类抽样）+ **3.4 动作类全量普查**（250 个 Library/Subsystem：MathLibrary 705 登顶、Library/Subsystem 密度相当、互操作管线 USD 166/ControlRig 131、5 个 404 差集）
  - 第 4 章 三套 API 选型 + 三层对照表（20 功能）+ **域能力矩阵**（四路数据按 19 域合流）
  - 第 5 章 4.27 → 5.8 演化：**模块入场时间线**（4.27/5.4/5.6/5.8 四快照点仲裁 + 5.0 快照缺失的元发现）+ Runtime 八大主题 + 换代与插件生死；附录：数据与核验方法

## 数据文件（_work/）

| 文件 | 内容 |
|---|---|
| `engine_modules_merged.json` | 494 个引擎模块页完整提取（分节 + 每条目官方 Remarks），49,168 条 API 条目 |
| `local_uplugins.json` | 本机 UE_5.8 安装版 893 个 .uplugin 描述符，与文档页抽样 8/8 逐字节一致 |
| `bp_categories_full.json` | 889 个蓝图分类页（588 个含子条目数据，其余受站点限流） |
| `python_sections.json` | Python API 全部类型页清单（Class 5149 / Struct 4106 / Enum 1776 / Delegate 618 / Native 26） |
| `diff_427_58.json` + `groups_427.json` + `groups_versions.json` + `module_timeline.json` | 4.27/5.0/5.4/5.6 版组页名单、差分与入场时间线（5.0 参数实测回退 4.27 快照） |
| `cpp_leaf_summary.json` + `py_leaf.json` + `py_sweep_full.json` | 叶级数据：32 个 C++ 核心类成员面 + 28 个 Python 主力类 + **250 个动作类全量普查** |
| `plugin_mods_local.json` + `plugin_mods_target.json` | 87 个重要插件的 262 个模块本地源码反射面计数（UCLASS/USTRUCT/UENUM/UINTERFACE，限速时的零网络替代路线） |
| `doc_data.py` / `doc_data_deep.py` ~ `doc_data_deep6.py` / `build_doc.py` | 文档生成器（域映射含 494 模块恰好归一域校验），`python build_doc.py > 目标.md` 重生成 |

## 抓取方法备忘

- 文档站前端纯客户端渲染，curl 直连被 Cloudflare 拦截（403）；数据实际来自 `dev.epicgames.com/community/api/documentation/document.json?path=/documentation/unreal-engine/<slug>&lang=en-us`（加 `&application_version=4.27` 可取历史版本），需在真实浏览器会话内 fetch（站内 origin 带 cookie）。
- 限流规律：连续约 800~1000 次请求后返回 HTTP 429，冷却 10~15 分钟恢复；evaluate 单轮 30 秒硬超时，长任务用页面内带游标 stepper 分轮。
- 插件描述与文档页同源于 .uplugin 描述符，可用本机引擎安装版交叉验证。
