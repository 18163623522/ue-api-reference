# -*- coding: utf-8 -*-
# 深度分析第十七层：接口与枚举命名模式（零网络）

IFACE_ENUM = {
 'iface_intro': '1,709 个接口的 **100% 以 I 开头**——接口是全引擎命名最整齐的类别。但后缀分布极散（Top 1 EditorModule 仅 29 个），说明接口命名没有统一模板。',
 'iface_findings': [
  '**接口/类比值=“扩展开放度”**——Developer 组的子域普遍高于 Runtime 组：平台与设备管理 177%、媒体 68%、资产管线 60%、分析前端 56%、属性定制 52%——这些是“邀请你注入实现”的域；而物理 3%、AI 5%、渲染 7%、游戏框架 8%——这些是“封闭实现、只暴露调用”的域。**扩展开放度与反射密度谱（1.2.3）形成正交维度**：高反射+低接口（Engine/AIModule）=“给设计师用但不给程序员扩展”；高接口+低反射（平台/管线）=“给程序员扩展但设计师不直接碰”。',
  '**Provider/Handler 模式**：ProfilerProvider 7、DataProvider 5、ProviderInterface 5、EventHandler 5——这些接口后缀标出了引擎的“插件位”：实现 IProfilerProvider 就能接入性能分析后端，实现 IDataProvider 就能注入数据源',
  '**ModularFeature 7 个**：IModularFeature 是引擎的模块化特性注册机制的入口接口——不常用但关键',
  '接口最集中的模块：TraceServices 61、DatasmithCore 59、SequencerCore 47、PropertyEditor 45、InteractiveToolsFramework 44——正好对应 1.2.4 节的“扩展点优先”模块清单（数据交叉验证）',
 ],
 'enum_intro': '3,778 个枚举的命名揭示了一个令人意外的事实：**EE\\* 开头的枚举占 71%**（2,703 个）——这不是“E + 领域词”的预期格式，而是“EE”双 E 前缀（如 EEnvQueryStatus、EExpressionType）。这是因为 Doxygen 会把 E 前缀去掉后取首词，很多枚举的领域词本身以 E 开头（Env/Expression/Editor…），加上前缀 E 就成了 EE。',
 'enum_findings': [
  '**领域专属枚举首词 Top**：EE\\*（通用）、EUE\\*（引擎全局 371）、EChaos\\*（物理 90）、EAudio\\*（音频 46）、EERHI\\*（渲染 30）、ETrace\\*（追踪 27）——这些首词直接标出了“该域有多少种‘模式/状态/开关’需要枚举”',
  '**各域枚举方言**：物理域 EChaos\\* 92 个（Chaos 子系统的模式极多）；游戏框架 EE\\* 817 个（Engine 模块的枚举大户）；渲染域 EERHI\\* 30 + EERDG\\* 17（RHI 和 RDG 的状态/格式枚举）',
  '**E 前缀占 77%**（2,941/3,778），其余 23% 以 U 开头（390 个）——U 开头的枚举其实是“反射可见的枚举”（UENUM 标注的蓝图可用枚举），它们在文档站被归入 Enums 节但保留了 U 前缀',
 ],
}
