# -*- coding: utf-8 -*-
# 深度分析第六层：插件模块反射面（本地 5.8 源码 UCLASS/USTRUCT/UENUM/UINTERFACE 计数口径）
# 数据：plugin_mods_local.json（262 个目标插件模块；283 个目标中 21 个未在安装版源码树定位到目录）

PLUGIN_MOD_SURFACE = {
 'intro': '插件生态的"重量"用另一把尺子量：在本机 UE_5.8 安装版源码里统计每个插件模块的**反射面**（UCLASS/USTRUCT/UENUM/UINTERFACE 声明计数）。这不是文档页条目口径（文档 Classes 表含非反射的纯 C++ 类，本地无法稳定复现），而是"可被蓝图/序列化/编辑器看见的类型面"——对插件而言恰恰是最有意义的度量：插件的价值就在于把能力暴露出来。统计范围：87 个重要插件的 262 个模块（目录定位 262/283）。',
 'anchor': '锚定对照：引擎 Engine 模块本地 UCLASS 计数 1,326——即最重的官方插件 Niagara（224 个 UCLASS）约为 Engine 的 17%，PCG（443）约为 1/3。**没有任何插件的反射面能比肩引擎核心模块，但头部插件已经是"准引擎级"的体量**。',
 'findings': [
  '模块 Top 3：PCG 852（U443+S195+E207）、ControlRig 729（其中 USTRUCT 646——绑定单位 RigUnit 几乎全是结构体，结构体驱动的框架设计）、Niagara 670',
  '插件 Top 5：Niagara 1047（7 模块）、PCG 962（3 模块）、ControlRig 837（3 模块）、Avalanche 682（32 模块——模块数最多但单模块小）、MeshModelingToolset 559（7 模块）',
  '实验 vs 稳定：实验插件模块均值 18 条 vs 稳定 37 条——**体量与成熟度正相关**，实验插件确实"还没长大"，选型时值得纳入考量',
  'GAS（GameplayAbilities 277）与 GeometryScripting（294）、StateTree（311）、IKRig（246）、MovieRenderPipeline（284）构成第二梯队——玩法与管线插件的反射面显著大于一般编辑器工具插件',
 ],
}
