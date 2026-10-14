# 附录：本地引擎源码扫描 vs 官方文档对比

> 数据源：F:/Github/UnrealEngine（5.7.4 完整源码）47,054 个 .cpp 文件扫描 + 官方 5.8 文档（6,581 个变量）

## 扫描结果

| 指标 | 数量 |
|---|---|
| 源码中 CVar 注册总数 | **9,827** |
| 源码中 Console Command 注册总数 | **788** |
| 官方 5.8 文档变量数 | 6,581 |
| 两者交集 | 5,690 |
| 源码有但文档没有 | **4,137** |
| 文档有但源码没有（5.8 新增） | 890 |

## 差异分析

**文档只收录了源码实际 CVar 的约 2/3**——4,137 个变量在源码中注册但未出现在官方 Console Variables Reference 页。主要原因：

1. **插件 CVar 未收录**：GAS（AbilitySystem.* 52 个）、PCG（pcg.* 113 个）、nDisplay（117 个）、PixelStreaming（67 个）等
2. **Console Command 不算 CVar**：源码中有 788 个 FAutoConsoleCommand（纯命令如 stat、open、freeze），文档只列变量不列命令
3. **渲染/物理长尾**：源码 r.* 有 1358 个未入文档、p.* 有 321 个——多为引擎内部调试/实验参数

## 源码独有变量的前缀 Top 15

| 前缀 | 数量 | 来源 |
|---|---|---|
| r.* | 1358 | 渲染器内部/实验参数 |
| p.* | 321 | Chaos 物理内部 |
| nDisplay.* | 117 | nDisplay 多屏插件 |
| pcg.* | 113 | PCG 程序化内容生成 |
| a.* | 106 | 动画系统内部 |
| au.* | 88 | 音频系统内部 |
| net.* | 81 | 网络系统内部 |
| PixelStreaming.* | 67 | Pixel Streaming |
| fx.* | 56 | 特效系统 |
| GameplayCameras.* | 55 | 相机系统插件 |
| AbilitySystem.* | 52 | GAS 技能系统 |
| mutable.* | 48 | Mutable 插件 |
| Concert.* | 44 | 多用户协作 |
| USD.* | 41 | USD 插件 |
| np2.* | 41 | 网络物理 |

## 怎么查源码独有的 CVar

完整清单在 _work/local_cvar_scan.json。在引擎控制台直接输入即可使用（所有注册的 CVar 运行时都可用，只是官方参考页没列出）。
