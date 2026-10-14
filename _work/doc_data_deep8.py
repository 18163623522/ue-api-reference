# -*- coding: utf-8 -*-
# 深度分析第八层：蓝图节点页抽样（18 个叶级节点页，bp_node_leaf.json）

BP_NODE_LEAF = {
 'intro': '最后一层叶子——**节点详情页**抽样 18 个（跨 AI/碰撞/标签/工具/游戏/物理/输入/网络/Niagara/音频/网格 11 个分类）。节点页格式高度统一：Navigation + **Inputs/Outputs 引脚表**（类型 + 引脚名 + 逐引脚悬浮提示），页均不到 2.5KB。',
 'findings': [
  '**"Target is X"是 BP→C++ 的溯源锚点**：节点页描述的第二行几乎总在声明宿主——Box Trace By Channel →*"Target is Kismet System Library"*（即 UKismetSystemLibrary）、Add Impulse →*"Target is Primitive Component"*、Add Mapping Context →*"Target is Enhanced Input Subsystem Interface"*、Clear Focus →*"Target is AIController"*。想知道一个蓝图节点背后的 C++ 函数在哪，节点页第一屏就有答案。',
  '**逐引脚有独立说明**：引脚表的第二列携带 tooltip 原文（如 Box Trace 的 Start 引脚：*"Start of line segment."*；Add Mapping Context 的 Mapping Context：*"A set of key to action mappings to apply to this player"*）——比编辑器悬浮提示更完整的参数文档。',
  '15/18 抽样节点带描述；**少数"子目录"页面混在节点层**（Utilities/Array、Game/Damage 实为更深一级的分类目录）——蓝图目录树实际有 3 层以上，14,613 个子条目里目录页与节点页混编。',
  '异步节点形态可见：Async Load Asset 页只有 Inputs+Outputs 而无"Target is"——它挂的是潜在节点（Latent action）而非某库函数。',
 ],
}
