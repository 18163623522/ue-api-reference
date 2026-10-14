# -*- coding: utf-8 -*-
# 深度分析第九层：Python 动作类全量普查（250 个 *Library/*Subsystem，py_sweep_full.json）

PY_CENSUS = {
 'intro': '把 3.3 节的 28 类抽样升级为**全量普查**：Python 侧 5,149 个类中所有以 *Library / *Subsystem 结尾的 250 个动作类逐页测完。结果：217 个有效页面、28 个 0 成员（几乎全是抽象基类：Subsystem/EngineSubsystem/EditorSubsystem/WorldSubsystem 等——模板类没有可调成员）、**5 个 404**（SynthesisUtilitiesBlueprintLibrary/BehaviorTreeLibrary/BlueprintMaterialLibrary/BlueprintPathsLibrary/CameraLibrary——引擎注册了暴露名册但文档站没生成页面，属于 Python 暴露名册与实际页面的已知差集）。',
 'findings': [
  '**MathLibrary 以 705 个成员登顶**（第二名 SystemLibrary 273 的 2.6 倍）——KismetMathLibrary 的 Python 面：数学工具箱是 unreal 模块里动作最密集的区域，做数值处理脚本几乎绕不开它。',
  '**两种模式密度相当**：Library 171 个有效类合计 3,479 方法（均值 20）vs Subsystem 45 个合计 830（均值 18）——函数库偏静态工具集、子系统偏有状态服务，但动作面厚度同级。',
  '**互操作管线厚得惊人**：UsdConversionLibrary 166（USD 转换面）+ ControlRigSequencerLibrary 131 + AnimationLibrary 119 + RigVMBlueprintLibrary 15——程序化动画与 USD 数据管线是 Python 自动化的第二大聚集区（仅次于资产/网格线）。',
  '**编辑器子系统第一梯队**：StaticMeshEditorSubsystem 64、TakeRecorderSubsystem 58、DataLayerEditorSubsystem 52、LayersSubsystem 46、EditorAssetSubsystem 43、LevelSequenceEditorSubsystem 38、EditorActorSubsystem 35——大世界分区（DataLayer/Layers）与录制/序列高居前列。',
  '**长尾极长**：171 个有效 Library 里 86 个只有 ≤5 个成员（一半是插件为蓝图暴露的单门面工具函数，Python 侧同样名存实亡）；全体 ≥50 成员的动作类仅 18 个——**Python 动作面高度头部集中**（4,329 个方法中 Top18 类占约四成）。',
 ],
}
