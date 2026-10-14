# -*- coding: utf-8 -*-
# 深度分析第五层：模块入场时间线（四快照点仲裁版）、文档覆盖质量元分析、域能力矩阵映射
# 数据来源：module_timeline 计算逻辑内嵌生成器；groups_427/groups_versions 快照；engine_modules_merged；bp_categories_full；python_sections；local_uplugins

TIMELINE = {
 'meta': '文档站的版本化 API 快照实际只有**四个独立时点：4.27、5.4、5.6、5.8**。`application_version=5.0` 参数经字节级比对确认返回的是 4.27 快照的逐字节副本（站点从未为 5.0 重建 API 页）——这本身是关于"官方文档覆盖度"的元发现：**UE5.0 的模块面在文档站上不可考**，5.1~5.3 的新模块（如 NNE）只能归入"4.27 之后~5.4 之间"的窗口。因此时间线按快照窗口标注，不给单点版本归因。',
 'buckets': [
  # 窗口, 数量(Dev/Ed/Rt), 代表模块, 解读
  ('≤4.27', 384, '88/122/174', 'Engine、Core、Slate、UMG、MovieScene、AIModule、Chaos、IrisCore（Iris 早在 4.x 已实验性在册）……',
   '78% 的模块是 UE4 时代遗产——UE5 的演进方式是"老模块内部换血"（渲染器重写、物理迁 Chaos）而非另起炉灶'),
  ('4.27 → 5.4 窗口', 40, '7/5/28', 'NNE、AudioLinkCore、解码器四件（Opus/Vorbis/Adpcm/Rad）、UniversalObjectLocator、XMPP、Stomp、IPC、BackgroundHTTP、CEF3Utils、CUDA、HardwareSurvey',
   'UE5 前半程的模块化主题：神经网络引擎入场、音频解码器从 Developer 组归位 Runtime、消息协议与后台下载基建'),
  ('5.4 → 5.6 窗口', 38, '10/8/20', 'VerseCompiler + uLang 三件、MassEntity（首个 Mass 引擎模块）、AutoRTFM、DataflowSimulation、CADKernelEngine、TraceInsights 拆分三件、MathCore、StateStream',
   '5.5/5.6 是"新范式入引擎"的一代：Verse 语言、Mass、事务内存并行、TraceInsights 拆分细化同期发生'),
  ('5.7 → 5.8 窗口', 32, '4/4/24', 'Mass 家族补全（MassCore/MassEngine/MassDeveloper/MassSignals）、GDK 三件、RigidPhysics、ChaosSpatialPartitions、带宽调试四件、WebSocketServer、TraceBasedDebuggers 两件',
   '最新一代是"收尾与配套"：Mass 从单模块长成五件套，Xbox GDK 与观测/调试面补齐'),
 ],
 'moves': '窗口期内的**搬家与退场**同样有信息量：SerializedRecorderInterface 从 Editor 组整体搬进 Runtime 组（录制能力运行时化）；ColorManagement 与 VirtualFileCache 一直活到 5.6 快照、5.8 前退场（色彩管理并入 OpenColorIOWrapper 体系、VFC 让位 Zen）。',
}

COVERAGE = {
 'headline': [
  ('Classes Remarks', '6,303 / 11,933 = 52%', '全引擎一半的类在文档页上没有说明文字'),
  ('Structs Remarks', '5,519 / 10,671 = 51%', '结构体同样约一半无说明'),
  ('Functions Remarks', '14,083 / 14,631 = 96%', '函数级几乎全覆盖——UE 的 Doxygen 习惯是函数注释勤、类注释懒'),
  ('插件描述', '850 / 893 = 95%', '.uplugin 的 Description 字段覆盖极好（43 个为空，如 IKRig/MotionWarping）'),
 ],
 'domain_note': '分域看更有指导意义（按类 Remarks 覆盖率排序，由生成器实时计算）：媒体播放/Mass/新兴技术等**新模块域覆盖率最高（73~78%）**——新代码带着文档习惯入场；而 **AI 与导航（32%）、输入与 XR（34%）、地形与植被（39%）、游戏框架（46%）这些最常用的域反而覆盖最低**——Engine/AIModule 的海量内部类常年没写类注释，使用这些域时要更多依赖源码与社区资料，不能只看 API 页。Best/Worst 模块同样两极：Horde 97%、DerivedDataCache 95%、SourceControl 93%（基建模块文档最勤）vs AudioEditor 3%、AnimationDataController 3%、MassEntityTestSuite 3%（编辑器与测试模块最懒）。',
 'advice': '实操建议：① 高覆盖域（网络/几何/遥测）可直接按 API 页 Remarks 理解模块；② 低覆盖域把 API 页当"索引"用——类名/继承链/函数签名可靠，说明文字缺失时转源码头文件与官方论坛；③ 函数级 96% 覆盖意味着**查"这个函数干什么"几乎总是有答案的**，查"这个类是什么"则一半要靠别处。',
}

MATRIX = {
 'intro': '把四路数据（引擎模块、蓝图分类、Python 类、官方插件）按 19 个功能域合流成一张能力矩阵，回答"每个域在各暴露层的厚度"。C++ 列是精确计数；BP/Python/插件三列是**启发式归类**（关键词/前缀/官方分类映射，一个条目可能计入多个域），看相对量级而非绝对值。',
 'reading': [
  '动画域是"编辑器侧最厚"的域：插件 83 个 + Python 300 类 + BP 1,700+ 子项，但引擎 C++ 模块只有 9 个——动画的重头戏全在插件生态（ControlRig/LiveLink/MLDeformer）',
  '网络域正相反：C++ 41 个模块（全引擎域第一）但 Python 面 0 类、BP 仅 15 个分类——纯运行时系统，编辑器/脚本侧天然薄',
  '渲染域 C++ 3,567 条 + Python 517 类（Material* 470 为主）——程序化材质是编辑器脚本化的最热门入口',
  '游戏框架域四面均衡（C++ 8,965 条 + BP 65 分类 + Python 110 类 + 插件 29 个）——离所有使用者都近，所以每层都有面',
  '核心基础域（C++ 10,176 条全引擎第一）在其他三层几乎为零——地基不需要被蓝图直接调用',
  '特效（Niagara）不在矩阵中：它是插件而非引擎模块，属于插件生态列的 FX 类（10 个插件），BP 侧 177 子项见第 2 章',
 ],
}
