# -*- coding: utf-8 -*-
# 深度分析第七层：叶级抽样——C++ 核心类成员面（32 类）与 Python 主力类成员数（28 类）
# 数据：cpp_leaf_summary.json / py_leaf.json（类页/类型页逐页抓取）

CPP_LEAF = {
 'intro': '再往下一层抽样：直接抓取 32 个核心类的**类页面**（叶级），统计其文档化的函数/变量/派生类数量。这一层能看到模块页看不到的东西——引擎真正的"重量都压在哪几个类上"。',
 'findings': [
  '**AActor 是引擎最胖的玩法类**：643 个文档化函数 + 117 变量 + **210 个文档化派生类**——可放置物的家族树。',
  '**UObject 的派生类清单有 2,001 个**——"一切之根"第一次有了量化数字（该清单还只是文档页直接列出的直接派生）。',
  '**UCharacterMovementComponent 是"配置之王"**：354 函数 + **236 个变量**——移动手感全靠参数堆出来的实证。',
  '**UEditorEngine 有 497 个函数**，直逼 AActor——编辑器引擎本体的类面与游戏核心同量级。',
  '**薄壳模式**：UChaosSolver（1 函数）、UMassEntitySubsystem（3 函数）这类"上层包装类"在文档面极薄——真实工作全在 F 层（Chaos 解算器内核/FMassEntityManager），印证 1.2.3 反射密度谱的结论：U 类只是壳。',
  'UUserWidget 250 函数/12 派生、SWidget 205 函数/7 派生——UI 两层基类的家族规模。',
 ],
 'quote_note': '类页还带完整版类注释（模块页只给一行截断）。AActor 页官方完整说明包含 **Actor 初始化顺序**：*"Actor initialization has multiple steps, here'"'"'s the order of important virtual functions that get called"*——从 UObject::PostLoad（仅静态放置的 Actor）→ UActorComponent::OnComponentCreated（生成时）开始的完整虚函数调用次序，这是生命周期问题的权威出处（比模块页 Remarks 详细得多）。',
}

PY_LEAF = {
 'intro': 'Python 侧同样下探一层：逐页抓取 28 个主力类/资产类的类型页，统计成员数（dt 条目，含方法与属性）。排行揭示了编辑器脚本面的真实形状：',
 'findings': [
  '**SystemLibrary 以 273 个成员居首**——Box/Capsule/Sphere 的 Trace/Overlap 全家桶 + Timer/Delay + DrawDebug 全在里面：它就是"蓝图工具箱"的 Python 镜像。',
  '**Actor 197 / GameplayStatics 147**——运行时操作面在编辑器脚本里依然可用（修改场景里的 Actor 不受"仅编辑器"限制，只是不能在打包后跑）。',
  '**World 只有 2 个成员**（get_data_layer_manager / get_world_settings）——运行时最核心的对象在编辑器脚本侧是薄壳：操作世界要走 LevelEditorSubsystem（36）与 EditorLevelLibrary（37）。这是"运行时面 ≠ 脚本面"的最好例证。',
  '**序列资产是 Python 的洼地**：LevelSequence 7 个、AnimSequence 4 个——官方把序列/动画脚本化的重担交给了专用插件（Sequencer Scripting / 各 EditorSubsystem），核心类只留元数据操作。',
  'Material 的 57 个"成员"大半是 used_with_* 用途属性而非方法——资产类的 Python 面以**属性直读写**为主，函数库类（*Library/*Subsystem）才是动作面。',
  'editor 侧双子星：MaterialEditingLibrary 77（建/连/删表达式全套）+ StaticMeshEditorSubsystem 64（LOD/碰撞/UV/Nanite）——材质与网格是脚本化自动化投入产出比最高的两个领域。',
 ],
}
