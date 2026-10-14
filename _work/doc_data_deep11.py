# -*- coding: utf-8 -*-
# 深度分析第十六层：结构体命名模式（零网络，10,671 个 Structs）

BP_STRUCTS = {
 'intro': 'C++ 类的前缀/后缀已分析（1.2 节），现在看另一半——**10,671 个 Structs 的命名模式**（零网络分析）。F 前缀占 **85%**（9,090 个），T 模板 10%，其余 5% 零星——结构体命名比类更整齐（没有 U/A 反射前缀的分裂）。',
 'findings': [
  '**后缀分布极其分散**：Top 1 后缀 SerializerConfig 仅 70 个（0.7%）——与类的 Top 后缀 Component 199 个（1.7%）相比更散，结构体没有一个"统帅型"后缀',
  '**数据描述类后缀合计 23%**（Params/Desc/Info/Data/Config/Settings/Init）：四分之一的结构体是"纯数据描述体"——印证了 1.2.4 节"结构体=数据编排系统"的定性',
  '**各域有鲜明的结构体方言**：网络域的 SerializerConfig/SerializerInfo（序列化描述符密集，对应 Iris 新复制系统的状态描述符设计）；物理域的 DataWrapper（21 个，Chaos 解算器数据包装）；Sequencer 域的 KeyStruct/ComponentData/PropertyTraits（轨道键值与属性求值）；AI 域的 DecoratorMemory/TaskMemory（行为树节点记忆体）——结构体后缀就是各域的"设计签名"',
  '**序列化/版本相关结构体极多**：SerializerConfig 70 + SerializerInfo 65 + ObjectVersion 37 + CustomVersion 16 = 188 个——引擎的版本管理与数据迁移占了结构体的近 2%',
  '**委托签名类结构体 150 个**（Delegate/Signature/Handler 后缀）——BP 动态委托在 C++ 侧以结构体形式存在，与 Python 侧的 618 个 Delegate 类型形成对应',
  '**结构体的 Remarks 列显示"100% 覆盖"是假象**——多数 Remarks 只写了类型定义语法（如 "( FTransformCollection )"）而非实际说明——这是文档质量的又一个元发现：**覆盖率和信息量不是同一件事**',
 ],
}
