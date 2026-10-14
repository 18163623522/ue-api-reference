# -*- coding: utf-8 -*-
# 深度分析第二层：Editor/Developer 逐子域、API 形态统计、BP 工作流加密、Python 配方带示意代码
# 引文全部取自 engine_modules_merged.json / bp_categories_full.json 提取数据

DEEP2 = {
'核心与运行时基础': {'quotes': []},
'游戏框架与玩法': {'quotes': [
  ('Engine', 'ULevelStreaming', 'Abstract base class of container object encapsulating data required for streaming…', '关卡流送容器：大世界按需加载的抽象'),
  ('Engine', 'UCharacterMovementComponent', 'CharacterMovementComponent handles movement logic for the associated Character owner.', '角色移动逻辑宿主——行走/跳跃/飞行/游泳模式与网络同步都在此'),
]},
'渲染与图形': {'quotes': [
  ('Renderer', 'FGraphicsMinimalPipelineStateInitializer', 'Pipeline state without render target state. Useful for mesh passes where the render target state is not changing between draws.', '无渲染目标态的管线状态——网格 Pass 间渲染目标不变时的快速比较优化'),
]},
'物理与碰撞': {'quotes': []},
'几何与建模': {'quotes': [
  ('MeshDescription', 'FAttributesSetBase', 'This is the container for all attributes and their arrays.', '网格属性容器：顶点/三角的任意属性数组的统一存储——"属性化网格"设计的核心'),
  ('InteractiveToolsFramework', 'AGizmoActor', 'is a base class for Actors that would be created to represent Gizmos in the scene.', '场景中呈现 Gizmo 的 Actor 基类——交互工具的视口可视化层'),
  ('InteractiveToolsFramework', 'FActivateToolChange', 'is used by UInteractiveToolManager to change the active tool.', '工具管理器切换活动工具的事务封装——支持 Undo/Redo 的工具切换'),
]},
'UI 界面': {'quotes': [
  ('UMG', 'FOnNavigationTransition', 'If Entered, Other Widget is the Widget Navigated From. If Exited, Other Widget is the Widget Navigated To', '导航转移事件：手柄焦点在控件间迁移的钩子'),
  ('UMG', 'FUMGDragDropOp', 'This is the drag/drop class used for UMG, all UMG drag drop operations utilize this operation.', 'UMG 拖拽操作统一载体'),
]},
'Sequencer 与影视虚拟制片': {'quotes': [
  ('MovieSceneTracks', 'FInterrogationChannels', 'A class specialized for interrogating Sequencer entity data without applying any state to objects.', '"审讯"通道：不施加状态地读取序列实体数据——烘焙/导出序列的标准姿势'),
]},
'音频': {'quotes': []},
'AI 与导航': {'quotes': []},
'网络与在线服务': {'quotes': [
  ('Sockets', 'ISocketSubsystem', 'This is the base interface to abstract platform specific sockets API differences.', '套接字子系统基接口：抹平平台 Socket API 差异'),
  ('Sockets', 'FInternetAddr', 'Represents an internet address. All data is in network byte order', '网络字节序的地址表示'),
  ('Messaging', 'IMessageBridge', 'Interface for message bridges.', '消息桥接口：进程间/网络消息总线的接驳点'),
]},
'资产与内容管线': {'quotes': [
  ('AssetRegistry', 'IAssetRegistry', 'Global singleton interface for accessing a catalog of all packages (and some other content file types) that are stored in any mounted d[irectory]', '资产注册表全局单例：访问任意挂载目录下全部包的目录清单——按需加载的查询面'),
]},
}

EDITOR_SUB = [
 ('编辑器框架与工作流', 28, 'UnrealEd（857 类，Editor 组最大）承载编辑器引擎本体（UEditorEngine：*"Engine that drives the Editor"*）、事务（Undo/Redo 贯穿一切编辑操作）、选择集与 PIE；FAssetEditorToolkit（*"Base class for toolkits that are used for asset editing (abstract)"*）是所有资产编辑器窗口的容器基类；MainFrame/LevelEditor 拼装主界面，ToolMenus 提供统一菜单注册。',
  [('UnrealEd', 'FAssetEditorToolkit', 'Base class for toolkits that are used for asset editing (abstract)', '资产编辑器工具包抽象基类')],
  ['写编辑器插件的标准路径：EditorSubsystem（全局服务）+ ToolMenus（菜单）+ 注册 Tab', '自定义资产编辑器（Toolkit + Tab Spawner + 视口布局 FAssetEditorViewportLayout）', 'PIE 前后钩子做自动化（配合 Blutility）', '事务感知的批量编辑（Scoper 保证可撤销）']),
 ('内容浏览器与资产管理', 17, 'UAssetDefinition（*"Asset Definitions represent top level assets that are known to the editor"*）是新一代资产类型注册面——图标/颜色/菜单/打开行为集中声明；内容浏览器的检索由 FAssetTextFilter（文本过滤）与 FFrontendFilter 系（如 FFrontendFilter_CheckedOut 只显示已检出资产）组成；WorldPartitionEditor 提供大世界分块管理 UI。',
  [('ContentBrowser', 'FFrontendFilter_CheckedOut', 'A filter that displays only checked out assets', '前端过滤器示例：只显示已检出——版本感知的资产视图'),
   ('AssetDefinition', 'UAssetDefinition', 'Asset Definitions represent top level assets that are known to the editor.', '资产定义：编辑器认识一种新资产的唯一注册点')],
  ['注册自定义资产类型（含缩略图/颜色/操作菜单全套）', '内容浏览器自定义过滤器/列', '集合（Collection）与标签的批量管理工具', 'World Partition 地块批量操作']),
 ('蓝图与图编辑器', 10, 'Kismet 系（FBlueprintEditor：*"Main Kismet asset editor"*）+ KismetCompiler 构成蓝图编辑与编译；GraphEditor 是公共图编辑底座，FConnectionDrawingPolicy（*"draws the connections for an UEdGraph composed of pins and nodes"*）这样的绘制策略类让连线样式可定制。材质图、动画蓝图、行为树、RigVM 图全部复用这套底座。',
  [('Kismet', 'FBlueprintEditor', 'Main Kismet asset editor', '蓝图主编辑器'),
   ('GraphEditor', 'FConnectionDrawingPolicy', 'This class draws the connections for an UEdGraph composed of pins and nodes.', '连线绘制策略：图可视化定制点（如动画蓝图的运动轨迹连线）')],
  ['自定义图节点（材质/动画蓝图/行为树节点的编辑器侧）', '图搜索与 Diff 工具（FGraphDiffControl 做版本对比）', '蓝图编译器扩展：静态分析/规范校验插件', '给自研节点系统复用 GraphEditor 底座']),
 ('资产编辑器', 40, '每类资产一个编辑器模块（材质 MaterialEditor、动画 Persona/SkeletalMeshEditor、网格 StaticMeshEditor、贴图 TextureEditor、UI UMGEditor、曲线 Curve*Editor、表 DataTable/CurveTable/StringTable Editor、序列 Sequencer、地形 LandscapeEditor……），全部基于 Toolkit + GraphEditor + PropertyEditor 组合搭建。这套"每种资产一个编辑器"的架构让编辑器可按需裁剪。',
  [('MovieSceneTracks', 'FCameraShakePreviewer', 'A class that owns a gameplay camera shake manager, so that we can use it to preview shakes in editor.', '编辑器内预览相机抖动——"编辑时所见即游戏所得"的细节体现')],
  ['定制各资产编辑器（工具栏、细节面板、预览场景 AdvancedPreviewScene）', '批量资产处理入口（配合 AssetTools 的动作）', '自动化打开/截图资产编辑器做管线校验']),
 ('视口与交互模式', 13, '专用拾取模式（ActorPickerMode/SceneDepthPickerMode）、VR 编辑（VREditor + ViewportInteraction）、对齐吸附（ViewportSnapping）。交互模式 = 编辑器里临时接管视口输入的标准机制（工具型插件常驻 EdMode）。',
  [],
  ['自定义编辑器模式（EdMode）做专用工具（建模模式即此形态）', '特殊拾取工作流（从场景/深度选目标）', 'VR 中的编辑与审查流程']),
 ('调试与专项面板', 15, 'GameplayDebuggerEditor/MassEntityDebugger 挂运行时调试数据的视口叠加；StatsViewer 性能计数；DeviceProfileEditor 管设备配置档；PIEPreviewDeviceSpecification 模拟移动设备分辨率/性能档。',
  [],
  ['游戏内调试 HUD（Gameplay Debugger 分类频道）', '移动端预览与性能分档验证', '设备配置（Device Profile）调优面板']),
 ('属性与 UI 定制', 5, 'PropertyEditor + DetailCustomizations 是"任意 UObject 自动生成属性面板"的引擎：FMathStructCustomization（*"Base class for math struct customization (e.g, vector, rotator, color)"*）这类定制类决定每种类型怎么渲染/编辑；ComponentVisualizers 给组件画视口句柄。这是游戏项目最常碰的编辑器扩展点。',
  [('DetailCustomizations', 'FMathStructCustomization', 'Base class for math struct customization (e.g, vector, rotator, color)', '数学结构体的细节面板定制基类'),
   ('PropertyEditor', 'FDetailsDisplayManager', 'provides an API to tweak various settings of your details view', '细节视图显示设置的管理入口')],
  ['为项目自定义类型定制编辑体验（颜色选择器/曲线/滑杆约束）', '隐藏/重排引擎属性防止美术误改', '组件视口可视化（样条/约束/体积的手柄）']),
 ('工具与杂项', 10, 'Blutility 是"用蓝图写编辑器工具"的体系：UAssetActionUtility（*"Base class for all asset action-related utilities…"*）/UActorActionUtility 让蓝图函数直接出现在资产/Actor 右键菜单；UEditorUtilityDialogLibrary 提供 PIE 事件对话框。AddContentDialog/PluginWarden 管内容新建与插件合规。',
  [('Blutility', 'UAssetActionUtility', 'Base class for all asset action-related utilities. Any functions/events that are exposed on derived classes that have the correct signat[ure]…', '资产动作工具基类：派生类上带正确签名的函数自动进右键菜单')],
  ['Editor Utility 蓝图：美术自助批量工具（免 C++）', 'Editor Utility Widget：拖控件搭工具面板', '右键菜单动作（资产级/Actor 级）']),
]

DEV_SUB = [
 ('构建/烘焙/DDC', 35, '派生数据缓存采用函数式构建模型：FBuildDefinition（*"an immutable reference to a build function and its inputs"*）把"构建=函数+输入"变成可寻址对象——输入相同即命中缓存，这是 DDC 全部魔法的根基。Zen 是配套存储服务，Horde 是分布式调度（FBlobHandle：*"Handle to a blob"* 的对象存储模型）；各类资产烘焙器（MeshBuilder/NaniteBuilder/TextureBuild/ShaderPreprocessor）挂在其上。',
  [('DerivedDataCache', 'FBuildDefinition', 'A build definition is an immutable reference to a build function and its inputs.', '构建定义=函数+输入的不可变引用——内容寻址缓存的键'),
   ('DerivedDataCache', 'FBuildContext', 'A build context provides the inputs for a build function and saves its outputs.', '构建上下文：供给输入、保存输出的执行环境'),
   ('Horde', 'FBlobHandle', 'Handle to a blob.', 'Horde 对象存储的 blob 句柄')],
  ['自定义烘焙产物缓存策略（共享 DDC/虚拟化到云存储）', '烘焙流水线定制（资产烹饪顺序、依赖预热）', 'Horde 集群扩容：分布式 shader 编译/DDC 加速']),
 ('平台与设备管理', 8, 'FTargetPlatformBase（*"Base class for target platforms"*）定义目标平台抽象（ cooks/plays 什么格式），TargetDeviceServices 提供设备代理服务（发现/部署/执行），TurnkeyIO 自动下载安装平台依赖（SDK/证书）。',
  [('TargetPlatform', 'FTargetPlatformBase', 'Base class for target platforms.', '目标平台抽象基类：烹饪格式/纹理压缩/着色器格式的决策点'),
   ('TargetPlatform', 'FTargetDeviceId', 'Implements a target devices identifier.', '目标设备标识')],
  ['新平台移植（嵌入式/定制主机）的平台模块', '设备农场：批量部署到真机跑自动化', 'Turnkey 一键补齐平台环境']),
 ('自动化与功能测试', 10, 'FunctionalTesting 提供关卡内测试 Actor（AScreenshotFunctionalTest 系做截图金样比对）；AutomationDriver 是 UI 自动化的流式 API——By（*"a collection of fluent helper functions designed to make accessing and creating element locators easy"*）定位控件、Until/FWaitTimeout 构成等待模型，与 Selenium 同构。',
  [('AutomationDriver', 'By', 'Represents a collection of fluent helper functions designed to make accessing and creating element locators easy', '元素定位器的流式构造（类似 Selenium 的 By）'),
   ('FunctionalTesting', 'AScreenshotFunctionalTest', 'No UI', '无 UI 截图测试（继承基类获得截图比对能力）')],
  ['Slate UI 自动化测试（按控件语义而非像素驱动）', '关卡功能测试（放置测试 Actor + 断言序列）', '截图回归基线管理', 'CI 冒烟与性能测试编排（配合 Gauntlet 插件）']),
 ('分析与调试前端', 19, 'TraceInsights 系即 Unreal Insights 的前端实现（FTimingEventSearch 做参数化时间轴事件检索），TraceServices/TraceAnalysis 消费 Trace 数据流；SessionFrontend 是远程会话统一面板（消息/测试/性能）；MessageLog/OutputLog 是结构化日志面。',
  [('TraceInsights', 'FTimingEventSearchParameters', 'Parameters for a timing event search.', '时间轴事件检索参数——Insights 里"找一帧里最贵的调用"背后的查询模型')],
  ['帧时间/网络/内存/资产加载四维性能分析', '自动化性能报告（Insights 导出+比对）', '自定义 Trace 通道的可视化扩展', '远程会话调试（连真机/连服务器）']),
 ('版本控制与协作', 10, 'SourceControl 把版本控制操作对象化：FCheckIn（*"Operation used to check files into source control"*）/FCheckOut/FConnect——任何 VCS 后端（Git/Perforce/自研）实现同一套操作接口即可接入编辑器；UncontrolledChangelists 支持"非受控变更单"工作流；SubmitTool 定制提交流水线。',
  [('SourceControl', 'FCheckIn', 'Operation used to check files into source control', '检出/提交/连接皆为操作对象——VCS 可插拔的接口设计'),
   ('SourceControl', 'FAnnotationLine', 'A single line of an annotated file', '文件注解行（blame 信息）')],
  ['接自研版本系统/资产审阅平台', '提交前自动校验（命名/引用/截图）流水线', '多用户同场景协作（Concert/MultiUser 插件的服务端就在这组）']),
 ('资产工具与导入导出', 12, 'AssetTools 的 FAssetTypeActions_Base（*"A base class for all AssetTypeActions"*）是资产右键动作的注册面（与 Editor 组 UAssetDefinition 分工：一个管"是什么资产"，一个管"能对它做什么"）；DatasmithExporter/Facade + DirectLink 支持从引擎反向导出与 DCC 直连实时同步。',
  [('AssetTools', 'FAssetTypeActions_Base', 'A base class for all AssetTypeActions.', '资产类型动作基类：右键菜单/拖放/颜色/缩略图的一站式注册')],
  ['自定义资产批量操作（右键菜单插件）', 'Datasmith 导出：把 UE 场景送进 DCC/归档', 'DirectLink：Maya/3ds Max 与编辑器增量同步']),
 ('本地化', 2, 'Localization 模块 + LocalizationDashboard 界面覆盖"采集→翻译→编译→导入导出"全流程；FLocTextHelper（*"High-level access to the non-compiled localization resources (manifests and archives)"*）抽象清单/档案两种资源格式。',
  [('Localization', 'FLocTextHelper', 'High-level access to the non-compiled localization resources (manifests and archives) in a way that abstracts some of their quirks.', '本地化资源高层访问：抹平清单/档案格式细节')],
  ['多语言管线（PO/XLIFF 交接翻译商）', '运行时切语言/字体的自动化验证', '文化区（Culture）特定的资产替换管线']),
 ('编辑器支撑库', 14, 'Settings/SettingsEditor 让 UDeveloperSettings 派生类自动获得设置面板；SourceCodeAccess 桥接各 IDE；StandaloneRenderer 让独立 Slate 程序能渲染；SlateReflector 提供控件树/样式审查器（F5 调 UI 神器）。',
  [],
  ['项目设置面板（UDeveloperSettings 三行代码接入）', '独立 Slate 小工具（不带引擎的轻量 GUI）', 'UI 调试：控件树/继承链/样式来源审查']),
]

API_SHAPE = [
 ('类名前缀即架构索引', [
   ('F（纯 C++）', 5868, 49, '引擎一半的类不进反射系统——性能与基础设施层（容器/数学/渲染/物理内核）'),
   ('U（UObject 系）', 4037, 33, '反射层：资产、组件、子系统、函数库——可序列化/蓝图可见'),
   ('T（模板）', 985, 8, '泛型容器与智能指针（TArray/TObjectPtr…）'),
   ('S（Slate 控件）', 540, 4, 'UI 控件层（Slate 两模块合计 391 类）'),
   ('A（Actor）', 209, 2, '可放置物只占 2%——量化印证"行为往组件放、Actor 保持克制"的组合模型'),
   ('I（接口，另计）', 1709, 0, '接口不在前缀统计内而单列 Interfaces 节：Runtime 1001/Editor 408/Developer 300——模块解耦靠接口而非继承'),
 ]),
 ('三个形态规律', [
   '219/494 个模块带独立 Functions 节——"BlueprintFunctionLibrary 式函数库"是引擎暴露功能给蓝图的标准形态',
   'Editor 组 139 个模块平均条目少但面宽（每资产一个编辑器模块），Runtime 组 246 个模块条目高度集中在头部（Engine/Core/CoreUObject/Chaos 四个占全引擎 40%）',
   '命名前缀本身就是文档导航：找"能放置的东西"搜 A，找"可蓝图化的对象"搜 U，找"UI"搜 S，找"扩展点"进 Interfaces 节',
 ]),
]

BP_WORKFLOWS2 = [
 ('生成与查找 Actor', 'Actor 分类（32 子项）', 'SpawnActor 系列 + Get All Actors Of Class / Find Nearest Actor / Actor Has Tag；配合 Game 分类的 Add Component by Class、Construct Object from Class、Get Game Mode / Get Game State / Get Instigator、FindPlayerStart、Flush Level Streaming——从"造一个东西"到"问世界要信息"的第一入口集。'),
 ('物理交互', 'Physics 分类（136 子项）', '力与冲量全家桶：Add Force（At Location/Local/All Bodies Below 变体）、Add Impulse、Add Angular Impulse in Degrees/Radians、Add Torque、Add Radial Force；约束控制 Break Constraint / Add Constrained Bodies；模拟开关 Enable/Disable Simulation；过渡到布娃娃用 Physics Blend Weight 累积。爆炸、抓取、载具漂移、绳桥全在这套节点里。'),
 ('碰撞查询', 'Collision 分类（83 子项）', 'Box/Capsule/Sphere 三形状 × Overlap（Actors/Components/With Orientation）× Trace（By Channel/By Profile/For Objects）矩阵 + Break Hit Result 拆命中信息 + Can Character Step Up / Move Ignore 系列控制通行——命中判定、视线遮挡、范围伤害、可攀爬判定的无代码做法。'),
 ('AI 行为', 'AI（38 子项）+ Blackboard（12）+ EQS', 'AI MoveTo 移动 + Get/Set Blackboard 变量读写记忆 + EQS 环境查询选点 + Get Focal Point 控制注视——巡逻/追击/逃跑最小闭环；复杂决策下沉行为树资产，蓝图只做感知响应（配 GameplayDebuggerEditor 实时可视调试）。'),
 ('输入响应', 'Input 分类（108 子项）', 'Enhanced Input 体系：Add Mapping Context 按状态切换输入映射（走路/开车/菜单），Break Input Action Value 拆动作值，Create Dynamic/Linked Value Input 动态构造输入值（运行时生成按键绑定）；另有 Create Root Motion Source 等高级入口。一套映射通吃键鼠/手柄/触屏。'),
 ('多人判定', 'Networking 分类（14 子项）', 'Has Authority / Is Server / Is Dedicated Server 分支权威逻辑，Get Local/Remote Role 判断角色，Set Replicates / Set Replicate Movement 开复制，Set Net Dormancy / Flush Net Dormancy / Force Net Update 管休眠与刷新，Tear Off 断联——蓝图多人游戏的全部开关，一眼看清"谁有权改什么"。'),
 ('特效驱动', 'Niagara 分类（177 子项，第一梯队）', 'Get/Set 全类型参数（Bool/Float/Int/Color/变量）、Parameter Collection 实例与覆盖、Set Desired Age / Advance Simulation by Time 手动步进（配合录屏/逐帧分析）、Get All Emitters / Data Interface 深入发射器内部——不止调特效，还能当 GPU 计算的参数面板。'),
 ('相机与过场', 'Camera（121）+ Cinematics（9）', 'Activate Camera 系（含 Camera System/Rig 分层叠加激活）、Deproject Screen to World 屏幕转世界（拾取/瞄准线基础）、Get Aim Dir 拿瞄准方向、Blend Camera Evaluation Data 混合相机求值；Cinematics 分类预测位姿（Predict World Transform at Time）做时间轴精确演出。'),
 ('标签驱动玩法', 'GameplayTags 分类（42 子项）', 'Does Container Match Tag Query 容器查询、Bind Event Wrapper to Gameplay Tag Changed 标签变化事件、Get All Actors Of Class Matching Tag Query 按查询拉 Actor——用标签替代字符串/枚举做状态标记，改配置不改代码。'),
 ('技能系统（GAS）', 'GameplayAbilities（13）+ GameplayEffects/Attributes 分类', 'Give Ability / Clear Ability / Find All Abilities with Tags 装卸技能，Input Confirm/Cancel 处理确认流，配 Effect/Attribute 分类节点做数值与状态——ARPG 技能系统的蓝图操作面。'),
 ('声音与音乐', 'Audio 分类（79 子项）', 'Create Sound 2D / Reverb Effect 开关、Sound Mix Modifiers 覆盖、Envelope Following 拿包络做视觉反馈、Bus/Bus sends 路由、Bounce 导出渲染——游戏内混音面板的节点形态（上层由 MetaSound 插件接管 DSP 图）。'),
 ('动画事件与程序化动画', 'Animation 分类（140 子项）', 'Bind to Animation Started/Finished/Event 生命周期事件、Control Rig Layer 运行时驱动绑定层、Add Socket / Add Node Asset Override 动态改装、Calculate Direction 算移动方向供混合空间用——动画蓝图之外的事件/参数通道。'),
 ('智能对象（Smart Objects）', 'SmartObject 分类（57 子项）', 'Add Smart Object / Find Smart Objects in Targeting Request / Add Tag to Slot——把世界里的椅子/工位/掩体登记为"可被 AI 预约使用的资源"，配 StateTree 做占用与排队：环境 AI 交互的标准基建。'),
 ('样条与程序化路径', 'Spline 分类（97 子项）', 'Add Spline Point at Index / Convert Spline to Poly Line / Divide Spline into Polyline Recursive——道路中心线、巡逻路径、轨道镜头、河流走向的统一做法：样条定义 + 采样离散化。'),
 ('程序化网格构建', 'StaticMesh 分类（33 子项）', 'Create Static Mesh Description / Build from Static Mesh Descriptions / Begin-Finish Assembly Build——蓝图层直接组装静态网格资产（配合 GeometryScripting 插件的几何函数库）：批量化生成道具变体的资产级管线。'),
 ('表演采集（Take Recorder）', 'TakeRecorder 分类（75 子项）', 'Add Source for Actor / Compute Next Take Number / Find Takes / Cancel Recording——把运行时表演（动画/音频/粒子状态）录制成 Take 资产再入 Sequencer：虚拟摄制与动作捕捉的录制面。'),
]

PY_SNIPPETS = [
 ('资产批量治理', 'unreal.EditorAssetLibrary + unreal.AssetRegistryHelpers', '按目录/类/标签筛资产，批量改名/迁移/设标签；做命名规范 CI 卡点。',
  'assets = unreal.EditorAssetLibrary.list_assets("/Game/Props", recursive=True)'),
 ('引用链分析', 'unreal.AssetRegistryHelpers.get_asset_registry()', '查谁引用了该资产（删除前安全检查）、生成依赖图谱报表。',
  'refs = reg.get_referencers("/Game/Props/Table.SM_Table", unreal.AssetRegistryDependencyOptions())'),
 ('关卡批量操作', 'unreal.EditorLevelLibrary / unreal.LevelEditorSubsystem', '遍历 Actor 批量替换/移动/改属性；世界分区地块处理。',
  'actors = unreal.EditorLevelLibrary.get_all_level_actors()'),
 ('材质批量改写', 'unreal.MaterialEditingLibrary', '遍历材质图节点改参数/换贴图、批量生成材质实例。',
  'unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(mic, "Rough", 0.5)'),
 ('骨骼网格批处理', 'unreal.SkeletalMeshEditorSubsystem', '批量设置 LOD/骨骼/物理资产元数据，动画资产管线预处理。',
  'unreal.SkeletalMeshEditorSubsystem.set_bone_category_name(mesh, "hand", "UpperBody")'),
 ('Sequencer 自动化', 'unreal.LevelSequence + Sequencer Scripting 插件', '按表格批量生成镜头序列/绑定轨道。',
  'seq = unreal.load_asset("/Game/Cine/Intro"); bindings = seq.get_bindings()'),
 ('构建前校验钩子', 'unreal.EditorLoadingAndSavingUtils / SystemLibrary', 'CI 中以 Commandlet 跑 Python：保存全部/校验脏资产/输出报告。',
  'unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)'),
 ('数据表驱动生成', 'unreal.DataTable / EditorAssetLibrary', '读 CSV/DataTable 驱动批量生成蓝图类资产并填参。',
  'rows = unreal.DataTableFunctionLibrary.get_data_table_row_names(dt)'),
]
