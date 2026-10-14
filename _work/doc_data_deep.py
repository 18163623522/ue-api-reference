# -*- coding: utf-8 -*-
# 深度分析层数据：每域机制/官方引文/用途（引文全部取自 engine_modules_merged.json 提取数据）

DEEP = {
'核心与运行时基础': {
 'mech': '一切 API 的地基。Core 提供容器（TArray/TMap/TSet）、字符串（FString/ FName）、智能指针、线程与任务图（TaskGraph/Async）、数学库——它是 API 条目数第二大的模块（6,277 条，其中 Functions 2,935 条）。CoreUObject 在其上建立 UObject 反射体系：类的属性/函数在运行时可见，这是编辑器属性面板、序列化、网络复制、蓝图暴露的共同前提。Json/XmlParser/Cbor 提供数据交换，uLang 系列是 Verse 语言的运行时核心。',
 'quotes': [
  ('CoreUObject', 'UObject', 'The base class of all UE objects.', '所有 UE 对象的基类'),
  ('CoreUObject', 'UFunction', 'Reflection data for a replicated or Kismet callable function.', '反射数据：描述一个可复制或蓝图（Kismet）可调用的函数——一句话点明"反射=复制+蓝图"两大消费方'),
  ('CoreUObject', 'FSoftObjectPath', 'A struct that contains a string reference to an object, either a package, a top level asset or a subobject.', '软引用：以字符串引用资产/子对象，是异步加载与流送的基础'),
  ('CoreUObject', 'FObjectInitializer', 'Internal class to finalize UObject creation (initialize properties) after the real C++ constructor is called.', '对象初始化器：C++ 构造之后的属性终态化'),
 ],
 'uses': ['自定义序列化格式 / 存档结构（配合 SaveGame 插件的存档体系）', '软引用 + AssetManager 做按需异步加载与流送', '利用反射写通用编辑器工具（自动生成 UI、批量属性修改）', '在 Shipping 里裁剪 Developer/Editor 代码时的分层依赖设计'],
},
'游戏框架与玩法': {
 'mech': 'Engine 是全引擎最大的模块（8,796 条 API），定义了 Actor-Component 组合模型：Actor 是可放置/生成的对象，组件提供可复用行为；SceneComponent 增加 Transform 与挂接，PrimitiveComponent 再增加可渲染/可碰撞几何。游戏规则由 GameMode 在服务器端定义，玩家通过 PlayerController 占有 Pawn；Character 自带网格、碰撞与内置移动逻辑（CharacterMovementComponent）。GameInstance 则是跨越关卡切换的进程级管理器。UGameplayStatics/UKismetSystemLibrary 是这套能力暴露给蓝图的静态函数桥。',
 'quotes': [
  ('Engine', 'AActor', 'Actor is the base class for an Object that can be placed or spawned in a level.', '可放置或生成到关卡中的对象的基类'),
  ('Engine', 'AGameModeBase', 'The GameModeBase defines the game being played.', 'GameMode 定义"玩的是什么游戏"——比赛规则、重生、胜利条件的家'),
  ('Engine', 'APawn', 'Pawn is the base class of all actors that can be possessed by players or AI.', '可被玩家或 AI 占有的 Actor 基类'),
  ('Engine', 'ACharacter', 'Characters are Pawns that have a mesh, collision, and built-in movement logic.', '自带网格+碰撞+内置移动逻辑的 Pawn'),
  ('Engine', 'UActorComponent', 'ActorComponent is the base class for components that define reusable behavior that can be added to different types of Actors…', '可复用行为的组件基类——UE 组合优于继承的落点'),
  ('Engine', 'UPrimitiveComponent', 'PrimitiveComponents are SceneComponents that contain or generate some sort of geometry, generally to be rendered or used as collision…', '携带/生成几何（渲染或碰撞用途）的组件层'),
  ('Engine', 'UGameInstance', 'GameInstance: high-level manager object for an instance of the running game.', '进程级高阶管理器：跨关卡存续'),
 ],
 'uses': ['用组件组合设计任何玩法对象（而不必继承庞大 Actor 子类）', '自定义 GameMode/GameState 规则与观战/重生逻辑', '定制 CharacterMovementComponent 做特殊移动模式', '关卡流送（ULevelStreaming）与世界分区大世界', 'GameplayTags/GameplayTasks 作为轻量玩法基建（标签驱动状态机、异步任务）'],
},
'输入与 XR 设备': {
 'mech': 'InputCore 定义按键/手势/轴的抽象数据；InputDevice 是设备接入接口层；HeadMountedDisplay 模块定义 XR 头显与追踪系统的公共接口（IHeadMountedDisplay/IXRTrackingSystem），OpenXR/各厂商插件在其上实现；EyeTracker/Voice 提供眼动与语音通道。运行时的按键映射推荐走 EnhancedInput 插件（上下文映射）。',
 'quotes': [
  ('HeadMountedDisplay', 'IHeadMountedDisplay', 'HMD device interface', '头显设备接口'),
  ('HeadMountedDisplay', 'IXRTrackingSystem', 'Main access point to an XR tracking system. Use it to enumerate devices and query their poses.', 'XR 追踪系统主入口：枚举设备、查询位姿'),
 ],
 'uses': ['为特殊硬件（踏板/方向盘/航班摇杆）写输入设备插件（RawInput 插件即此类）', 'XR 应用：手柄位姿、注视交互、空间锚（ARPin 走 BP AR 分类）', '语音命令与辅助功能（Text to Speech 插件）'],
},
'渲染与图形': {
 'mech': '三层栈：RHI 是跨图形 API 的硬件抽象（FRHICommandList 命令缓冲、FRHITexture 等资源接口；FDynamicRHI 为动态绑定入口），D3D12RHI/VulkanRHI/OpenGLDrv 是各平台后端；RenderCore 提供公共层（顶点工厂 FVertexFactory 把顶点数据源链接进顶点着色器、GPU 场景、着色器绑定）；Renderer 实现场景渲染器（延迟着色管线、网格绘制命令 FMeshDrawCommand 的缓存与逐帧构建）。要做渲染扩展，通常从 RenderCore/Renderer 的扩展点（顶点工厂、Mesh Processor、自定义 Pass）入手而不是直接写 RHI。',
 'quotes': [
  ('RHI', 'FDynamicRHI', 'The interface which is implemented by the dynamically bound RHI.', '动态绑定 RHI 的接口——启动时选定的图形后端入口'),
  ('RenderCore', 'FVertexFactory', 'Encapsulates a vertex data source which can be linked into a vertex shader.', '封装可链接进顶点着色器的顶点数据源——自定义网格渲染的标准扩展点'),
  ('Renderer', 'FCachedMeshDrawCommandInfo', 'Stores information about a mesh draw command which is cached in the scene.', '场景中缓存的网格绘制命令——UE 渲染器"命令缓存复用"设计的体现'),
 ],
 'uses': ['自定义顶点工厂+材质绘制特殊几何（如 Niagara 的各 VertexFactories 插件做法）', '渲染器扩展：后处理材质、自定义 Screen Pass（引擎源码级）', '平台适配：新 GPU API/新硬件的 RHI 后端（专业团队）', '图形调试：RenderDocPlugin/PixWinPlugin/DumpGPUServices 插件直接可用', '色彩管理 OpenColorIO、上采样/帧生成（DLSS/FSR 插件分类）'],
},
'物理与碰撞': {
 'mech': '5.x 物理统一到 Chaos：Chaos 模块是解算器内核（宽相 FBasicBroadPhase 按 AABB 筛粒子对、求解器全步骤容器 FAllSolverTasks、CCD 修正 FCCDModifier），ChaosSolverEngine 把解算器包装成场景对象（UChaosSolver），PhysicsCore 提供碰撞通道/Profile/BodySetup 等抽象。破坏系统=几何集合（FGeometryCollection，可破碎的分层网格数据）+ FieldSystemEngine 力场（UFieldSystemComponent 在空间中施加断裂/力场）。ChaosVD 录制回放用于物理调试；载具走 ChaosVehicles。',
 'quotes': [
  ('Chaos', 'FBasicBroadPhase', 'Run through a list of particle pairs and pass them onto the collision detector if their AABBs overlap.', '宽相：遍历粒子对，AABB 重叠者送碰撞检测——物理管线第一步'),
  ('Chaos', 'FAllSolverTasks', 'Container for all steps required to fully update a solver.', '解算器完整更新的全步骤容器'),
  ('Chaos', 'FCCDModifier', 'Allows the user to modify the results of CCD collision detection prior to the CCD rewind being applied.', 'CCD（连续碰撞检测）回卷前的结果修正点'),
  ('ChaosSolverEngine', 'UChaosSolver', 'UChaosSolver ( UObject )', '场景级解算器对象'),
 ],
 'uses': ['刚体破坏玩法（几何集合 + 力场组件 + 破碎触发，FractureEditor/PlanarCut 插件做预破碎）', '载具（ChaosVehicles）与布料（ChaosCloth 系列插件）', '物理控制动画（PhysicsControl 插件对静态/骨骼网格做物理驱动）', '碰撞查询（Blueprint 的 Trace/Overlap 全家桶即其暴露面）', '物理回放调试（Chaos Visual Debugger）'],
},
'几何与建模': {
 'mech': 'MeshDescription 是引擎统一的网格数据结构（静态/骨骼网格资产内部即用它存储），GeometryCore 提供几何算法库（661 个函数），GeometryFramework/CADKernel 支撑 CAD 数据，Dataflow 系列提供节点图式几何处理资产（布料/破坏资产编辑都建在其上）。InteractiveToolsFramework 定义编辑器交互工具的标准基类（选中/接受/取消的生命周期）——编辑器"建模模式"整套工具就是它的大规模应用。',
 'quotes': [
  ('InteractiveToolsFramework', None, None, None),
 ],
 'uses': ['程序化网格生成与编辑（GeometryScripting 插件把整套几何函数暴露给蓝图）', '自定义编辑器建模工具（挂进 ModelingToolsEditorMode 的工具模式）', 'Dataflow 节点式几何资产（布料资产、破坏资产的数据流编辑）', 'CAD/工业数据导入管线（CADKernel + DatasmithCADImporter）'],
},
'UI 界面': {
 'mech': '两层 UI：Slate/SlateCore 是保留模式 UI 框架（声明式 SlateBuilder 语法、合成/布局/绘制全自研，编辑器全部界面皆 Slate，也能做游戏 UI）；UMG 在 Slate 外包一层 UObject（UWidget 系列）使其可蓝图化、可序列化为 WidgetBlueprint 资产，UUserWidget 是"用蓝图拼 UI"的载体。WebBrowser/CEF3Utils 提供内嵌浏览器控件；渲染走 SlateRHIRenderer。跨平台手柄导航用 CommonUI 插件。',
 'quotes': [
  ('SlateCore', 'SWindow', 'SWindow is a platform-agnostic representation of a top-level window.', '平台无关的顶层窗口表示——独立工具窗口的容器'),
  ('Slate', 'SButton', "Slate's Buttons are clickable Widgets that can contain arbitrary widgets as its Content().", '按钮可容纳任意控件作为内容——组合式 UI 的体现'),
  ('Slate', 'SListView', 'A ListView widget observes an array of data items and creates visual representations of these items.', '列表视图：观察数据数组并生成可视化项（MVVM 式）'),
  ('UMG', 'UUserWidget', 'A widget that enables UI extensibility through WidgetBlueprint.', '通过 WidgetBlueprint 实现 UI 扩展——蓝图 UI 的载体'),
  ('UMG', 'UWidget', 'This is the base class for all wrapped Slate controls that are exposed to UObjects.', '所有被 UObject 包装的 Slate 控件的基类——两层 UI 的粘合层'),
 ],
 'uses': ['游戏 HUD/菜单/背包（UMG + 控件动画）', '编辑器工具窗口与属性面板（纯 Slate，配合 EditorWidgets/GraphEditor 做图编辑器 UI）', '主机/手柄 UI 导航与样式系统（CommonUI 插件，游戏无关的可复用控件库）', '内嵌网页（登录/商城/ wiki 面板，CEF 内核）', 'UMG 预览与调试（UMGWidgetPreview 插件免 PIE 预览）'],
},
'动画与布料': {
 'mech': 'AnimationCore 是动画数据结构（姿势/曲线/骨骼）基础层，AnimGraphRuntime 是动画蓝图运行时（状态机/混合空间/各种节点的求值实现，并以 *Library 类把节点上下文操作暴露成函数）。外部数据经 LiveLink 三件套流入（动捕服、面部捕捉、DCC 软件桥）；布料已归 Chaos 体系（ClothingSystemRuntime* 接口层 + ChaosCloth 插件实现）；MRMesh 承载面部混合现实网格。高端链路：ControlRig（程序化绑定动画）、IK Rig（重定向）、MLDeformer（机器学习形变压缩）。',
 'quotes': [
  ('AnimGraphRuntime', 'UAnimationStateMachineLibrary', 'Exposes operations to be performed on anim state machine node contexts.', '暴露状态机节点上下文操作——动画蓝图的程序化接口'),
  ('AnimGraphRuntime', 'UBlendSpaceLibrary', 'Exposes operations to be performed on a blend space anim node.', '混合空间节点操作库'),
 ],
 'uses': ['动画蓝图/状态机/混合空间的深度定制（通知窗口、自定义节点求值）', 'Live Link 动捕直播到引擎（角色/相机/灯光均可作为源）', 'Control Rig 程序化动画与绑定（绑定资产在运行时求值）', 'IK Rig + 重定向把动画跨骨架复用（IKRetarget 插件）', 'ML 形变器把高质量模拟"烘焙"成轻量推理（MLDeformer/NearestNeighbor）'],
},
'Sequencer 与影视虚拟制片': {
 'mech': 'MovieScene 定义序列资产本体（UMovieScene + UMovieSceneSequence 抽象 + Section 轨道分节），LevelSequence 把序列落到关卡 Actor 上、ULevelSequencePlayer 负责运行时播放；TimeManagement 提供帧率/时间码标准。影片输出与摄制工作流由插件完成：Take Recorder（表演采集）、Movie Render Queue（离线高质量渲染）、AVEncoder/AVIWriter（编码）、nDisplay/VCam/Composure（虚拟摄制与合成）、StageDataCore（舞台数据）。BP 的 Camera/Cinematics 分类是这套能力的节点面。',
 'quotes': [
  ('MovieScene', 'UMovieScene', 'Implements a movie scene asset.', '影片场景资产实现'),
  ('MovieScene', 'UMovieSceneSequence', 'Abstract base class for movie scene animations (C++ version).', '序列抽象基类——一切"可播放时间线"的父类'),
  ('LevelSequence', 'ULevelSequence', 'Movie scene animation for Actors.', '针对关卡 Actor 的序列动画'),
  ('LevelSequence', 'ULevelSequencePlayer', 'is used to actually "play" a level sequence asset at runtime.', '运行时真正"播放"关卡序列的播放器'),
 ],
 'uses': ['过场动画与游戏内事件时间线（导演式控制任意 Actor 属性）', '技能/交互的时序编排（序列驱动粒子/相机/音效）', '虚拟摄制全流程：nDisplay 多屏、VCam 虚拟相机、Composure 实时合成、ICVFX 摄制内视效', '自动化出片：Movie Render Queue 批量高质量渲染 + Take Recorder 采集'],
},
'音频': {
 'mech': 'AudioMixer 是混音器主框架（设备管理、总线 FMixerAudioBus、源管理），SignalProcessing 是 DSP 基础库，AudioLink 让外部混音器（Wwise 等）接管；音乐系统 Quartz 提供采样级精确的量化时钟（FQuantizedOtherClockStart 等）；分析与采集走 AudioAnalyzer/AudioCapture。上层内容体系在插件里：MetaSound（DSP 图式声音资产，官方描述"让声音设计师完全掌控声音源的 DSP 图生成"）、AudioModulation（参数调制）、SoundFields/ResonanceAudio（空间化）。编解码器（Opus/Vorbis/Bink/ADPCM/Rad）按平台接入。',
 'quotes': [
  ('AudioMixer', 'FMixerAudioBus', 'Bus instance data. Holds source id bus instances and bus sends data.', '总线实例数据：源与发送关系的运行时载体'),
  ('AudioMixer', 'FQuantizedOtherClockStart', 'starts a second clock on a sample-accurate boundary', '在采样级精确边界启动第二个时钟——Quartz 程序化音乐的精度基础'),
  ('AudioMixer', 'FOnSynthEnvelopeValue', "Called by a synth component and returns the sound's envelope value (using an envelope follower in the audio renderer).", '包络跟随器回调：音频驱动的视觉反馈（如 UI 随音起舞）的数据源'),
 ],
 'uses': ['MetaSound 搭建可参数化的程序化音源（替代 SoundCue 的下一代）', 'Quartz 做节拍同步玩法（音游、随节拍生成敌人）', 'Submix/效果链处理与录音输出', '对话与本地化配音管理', '空间化与混响（Resonance Audio 房间声学）'],
},
'AI 与导航': {
 'mech': 'AIModule 提供 AI 三件套：AAIController 驱动 AI Pawn（大脑组件 BrainComponent 挂行为树/HTN），UAIPerceptionComponent 注册为感知系统的监听者收集刺激，UBTTaskNode 等构成行为树节点体系（Task 是"执行动作的叶子节点"）。导航侧 NavigationSystem 管理导航数据（ANavigationData 抽象出 NavMesh/NavGraph），Navmesh 模块是 Recast 生成器，ANavModifierVolume 可用体积动态改 NavMesh 区域属性。环境查询 EQS、人群 MassCrowd、机器学习 LearningAgents 都挂在这套地基上。',
 'quotes': [
  ('AIModule', 'AAIController', 'AIController is the base class of controllers for AI-controlled Pawns.', 'AI 控制 Pawn 的控制器基类'),
  ('AIModule', 'UAIPerceptionComponent', 'is used to register as stimuli listener in AIPerceptionSystem and gathers registered stimuli…', '注册为感知系统监听者并收集刺激（视觉/听觉/伤害感知的接收端）'),
  ('AIModule', 'UBTTaskNode', 'Task are leaf nodes of behavior tree, which perform actual actions', '行为树叶子节点：执行实际动作'),
  ('NavigationSystem', 'ANavigationData', 'Represents abstract Navigation Data (sub-classed as NavMesh, NavGraph, etc). Used as a common interface for all navigation types…', '导航数据抽象：NavMesh/NavGraph 的公共接口'),
  ('NavigationSystem', 'ANavModifierVolume', 'Allows applying selected AreaClass to navmesh, using the shape of the Volume', '用体积形状给 NavMesh 施加区域属性（动态成本/禁区）'),
 ],
 'uses': ['行为树 AI（巡逻/追击/逃跑的经典栈：BT + 黑板 + EQS 选点）', '感知型 AI（视觉锥/听觉半径触发行为切换）', '动态导航（破坏桥后重生成 NavMesh、用 NavModifier 改通行成本）', '大规模人群（MassCrowd 样条人群 + 避障）', '强化学习角色控制（LearningAgents 训练后运行时推理）'],
},
'网络与在线服务': {
 'mech': '复制栈：NetCore 管理 NetDriver/连接（FConnectionHandle 每 NetDriver 唯一），对象引用跨机器以 NetGUID 复制（FGuidReferences 的官方说明直接点明原因："字面内存指针在不同机器上不同"），PacketHandler 做包处理链，IrisCore 是 5.x 在研的新一代复制系统（按状态描述符序列化，更细粒度的脏跟踪）。通信设施：Sockets/HTTP/HttpServer/WebSockets/Stomp/XMPP，Messaging 系是引擎内部消息总线。回放系统 NetworkReplayStreaming 有五种后端实现（本地文件/内存/HTTP/存档/空）。在线服务走 OnlineServices 体系（EOS 等插件）。',
 'quotes': [
  ('NetCore', 'FGuidReferences', 'References to Objects (including Actors, Components, etc.) are replicated as NetGUIDs, since the literal memory pointers will be different across machines.', '对象引用复制为 NetGUID——因为裸指针在每台机器上都不同'),
  ('NetCore', 'FConnectionHandle', 'The handle is unique per netdriver.', '每 NetDriver 唯一的连接句柄'),
  ('HTTP', 'FHttpModule', 'Use FHttpFactory to create a new Http request', 'HTTP 请求工厂入口'),
  ('HTTP', 'IHttpResponse', 'Interface for Http responses that come back after starting an Http request', 'HTTP 响应接口'),
 ],
 'uses': ['多人游戏：属性复制（DOREPLIFETIME 宏）+ RPC + 相关性（每帧只发玩家附近的）', '专用服务器与回放（DemoNetDriver + 流后端选择）', '对接账号/好友/成就/匹配（OnlineServices + EOS/Steam/谷歌插件）', '游戏内 Web 面板（HttpServer + WebSockets 推送，Pixel Streaming 远程操控同源）', 'DDoS 检测与限流（FDDoSDetection 直接可用）'],
},
'媒体播放': {
 'mech': 'Media/MediaAssets/MediaUtils 构成媒体框架三件套：UMediaPlayer 是播放器资产，视频轨渲染到 UMediaTexture，音频走 UMediaSoundComponent，ImageDownload 支撑运行时图片拉取。具体解码/协议由插件提供：ElectraPlayer（跨平台流媒体主力）、AvfMedia/WebMMedia/WindowsMoviePlayer（平台原生）、ImgMedia（EXR 序列，虚拟摄制视频墙主力）、AjaMedia（采集卡 I/O）。',
 'quotes': [
  ('MediaAssets', 'UMediaPlayer', 'Implements a media player asset that can play movies and other media sources.', '媒体播放器资产'),
  ('MediaAssets', 'UMediaTexture', 'Implements a texture asset for rendering video tracks from UMediaPlayer assets.', '把视频轨渲染成纹理——视频贴到任意材质的通道'),
  ('MediaAssets', 'UMediaSoundComponent', "Implements a sound component for playing a media player's audio output.", '播放媒体音频输出的组件'),
 ],
 'uses': ['游戏内视频屏幕（监控器/电视机/巨幕，MediaTexture 贴材质）', '虚拟摄制 LED 墙内容播放（ImgMedia EXR 序列 + nDisplay 同步）', '过场视频与开场动画（平台原生解码器保证兼容）', '直播流/网络视频接入（Electra 支持 HLS/DASH 流）'],
},
'地形与植被': {
 'mech': 'Landscape 是高度场地形系统：组件化分块、多层材质混合、支持编辑层（FEditLayerRenderItem 描述每层能渲染什么）、与 World Partition 深度联动（按地块流送）；Foliage 是实例化植被（一株资产刷 N 个实例，GPU 实例化渲染）。程序化生成可接 PCG 插件（图驱动散布）与 Landmass（地形侵蚀）。',
 'quotes': [
  ('Landscape', 'FEditLayerRenderItem', 'Each edit layer render item represents the capabilities of what a given edit layer can render in terms of landscape data…', '编辑层渲染项：描述该编辑层能渲染的地形数据能力——非破坏性地形分层编辑的机制核心'),
 ],
 'uses': ['大世界地形（World Partition 分块流送 + HLOD）', '多层非破坏编辑（每层可独立开关/回滚的雕塑与绘制）', '植被/岩石散布（刷绘或 PCG 规则化散布 + 运行时节裁）', '程序化地形（Landmass 侵蚀 + 水系 Water 插件联动雕刻河道）'],
},
'Mass 实体系统': {
 'mech': 'Mass 是 UE 的 ECS 式框架：实体=纯 ID+分块存储的组件数据，Processor 在多线程上处理队列（FProcessorWorker/FChunkWorker 是其工作单元），UMassEntitySubsystem 作为世界子系统承载实体管理器。它与传统 Actor 世界通过 Spawner/Representation 处理器桥接（远处的车是 Mass 实体，近了才生成真 Actor）。配套：ZoneGraph（样条路网）、StateTree（行为）、MassCrowd/MassAI 插件。',
 'quotes': [
  ('MassEntity', 'UMassEntitySubsystem', 'The sole responsibility of this world subsystem class is to host the default instance of FMassEntityManager for a given UWorld.', '承载某 UWorld 默认 FMassEntityManager 的世界子系统'),
  ('MassEntity', 'FProcessorWorker', 'A worker to execute queued processors', '执行排队处理器的工作单元——多线程处理器的运行形态'),
 ],
 'uses': ['大规模人群/车流（万级实体占 CPU 小头）', '环境生命模拟（鸟群、鱼群、战场背景单位）', 'LOD 化玩法代理（远处 ECS、近处真 Actor 的无缝切换）'],
},
'资产与内容管线': {
 'mech': 'AssetRegistry 是全项目资产的元数据库（磁盘缓存的 FAssetRegistryState），编辑器内容浏览器、加载校验、按标签/类检索都靠它，且暴露给蓝图/Python。Interchange 是新一代统一导入框架：导入物先转换为通用节点图（UInterchangeBaseNodeContainer），再经管线（UInterchangePipelineBase）喂给各格式工厂——FBX/glTF/USD/OBJ 都走这条路。打包侧：PakFile/IoStoreOnDemand 打包与按需分发，BuildPatchServices 做差分补丁，Zen 是 DDC/构建存储服务。Datasmith 是工业管线（CAD/Revit/SketchUp→引擎）的专用通道。',
 'quotes': [
  ('AssetRegistry', 'FAssetRegistryState', 'The state of an asset registry, this is used internally by IAssetRegistry to represent the disk cache…', '资产注册表状态=磁盘缓存——资产查询的数据底座'),
  ('InterchangeCore', 'UInterchangeBaseNodeContainer', 'The Interchange UInterchangeBaseNode graph is a format used to feed factories and writers when they import, reimport, and export', 'Interchange 节点图：导入/重导/导出时喂给工厂与写入器的统一格式'),
  ('InterchangeCore', 'UInterchangePipelineBase', 'Pipeline implementation:', '管线基类——自定义导入处理的挂点'),
 ],
 'uses': ['按类/标签/路径批量检索资产做工具（Python EditorAssetLibrary 的底层就是它）', '自定义 Interchange 管线处理专有格式导入（重命名/LOD/碰撞预设自动化）', '游戏运行时资产发现（不加载资产本体即可枚举：开放世界按区加载、Mod 发现）', '补丁/按需分发（BuildPatchServices 差分 + IoStoreOnDemand 流送）'],
},
'遥测与性能分析': {
 'mech': 'TraceLog 是低开销埋点数据流（运行时常开），TraceServices/TraceAnalysis 是分析后端，TraceInsights 系即 Unreal Insights 前端（帧/网络/内存/资产加载多维分析）；Analytics* 是可插拔遥测后端（CSV/ET/日志/Swrve/Horde）；PerfCounters 暴露运行时计数器；RewindDebugger 是动画/属性回溯调试器的运行时接口。第三方 RenderDoc/PIX 插件负责 GPU 级抓帧。',
 'quotes': [
  ('TraceLog', None, None, None),
 ],
 'uses': ['性能回归看板（Insights + Gauntlet 自动化性能测试出报告）', '线上问题遥测（Analytics 后端自选落地）', '多人同步分析（Concert Insights 让多客户端同起 Trace）', '动画逐帧回溯（Rewind Debugger）'],
},
'自动化测试': {
 'mech': 'AutomationTest 框架（Runtime 侧）+ AutomationController/Driver/Window（Developer 侧驱动与窗口自动化）+ FunctionalTesting（关卡式功能测试 Actor）。打包后自动化跑 Gauntlet 插件（以测试控制器驱动整包游戏），性能自动化走 AutomatedPerfTesting。CQTest 提供断言库。',
 'quotes': [
  ('AutomationTest', None, None, None),
 ],
 'uses': ['单元/冒烟/功能三级测试金字塔接入 CI', '截图比对回归（ScreenShotComparison）', '整包自动化与性能基线（Gauntlet + 性能测试控制器）', 'UI 自动化（AutomationDriver 驱动 Slate 控件）'],
},
'新兴与实验技术': {
 'mech': '五件套：VerseCompiler/uLang（UEFN 的 Verse 语言编译与运行时）、NNE 神经网络引擎（UNNEModelData 资产存模型，运行时由插件提供四种后端：ONNX Runtime、IREE、CoreML、RDG——即 CPU/GPU/苹果/渲染图四种推理路径）、VectorVM（Niagara GPU 仿真的向量虚拟机）、CUDA（NVIDIA 直连）、AutoRTFM（事务内存实验，让"回滚式"并行成为可能）。',
 'quotes': [
  ('NNE', 'UNNEModelData', 'This class represents assets that store neural network model data.', '存储神经网络模型数据的资产——引擎内跑 AI 推理的载体'),
 ],
 'uses': ['在引擎/游戏内跑 ML 模型（超分、动画混合、NPC 行为，配 NNERuntime 插件选后端）', 'Verse 脚本生态（UEFN 创作者生态的语言基础）', 'VectorVM 写数据并行脚本（Niagara Simulation Stage 的执行后端）'],
},
}

EDITOR_ANALYSIS = 'Editor 组 139 个模块就是"编辑器这台机器"本身：UnrealEd（857 类）承载编辑器引擎、事务（Undo/Redo）、选择、PIE；Kismet/KismetCompiler/BlueprintGraph/GraphEditor 构成蓝图编辑器与编译器；ContentBrowser/AssetDefinition/PropertyEditor/DetailCustomizations 是内容浏览器与"任意 UObject 的属性面板"的定制点（做编辑器插件必碰）；各资产编辑器（MaterialEditor/Persona=动画编辑器/StaticMeshEditor/UMGEditor/Sequencer…）互相独立可替换；LevelEditor/ViewportInteraction/VREditor 管主视口与交互模式；WorldPartitionEditor/DataLayerEditor 支撑大世界编辑。给编辑器写扩展的常规路径：EditorSubsystem（全局服务）+ AssetAction（资产右键菜单）+ DetailCustomization（属性面板定制）+ ToolMenus（菜单注册）+ EditorUtilityWidget（免 C++ 的工具面板）。'

DEV_ANALYSIS = 'Developer 组 109 个模块是"造游戏的工具链"：构建烘焙链（TargetPlatform→ShaderCompiler/TextureBuild/MeshBuilder/NaniteBuilder→CookedEditor/PakFileUtilities）与新一代加速基建 Horde（分布式构建）+ Zen（存储服务）+ DDC 虚拟化；设备管理（DeviceManager/TargetDeviceServices/Turnkey 一键装机）；自动化（AutomationController/Driver + FunctionalTesting）；分析前端全家桶（TraceInsights=Unreal Insights、SessionFrontend、MessageLog、ProfileVisualizer）；协作（SourceControl 体系、UncontrolledChangelists、SubmitTool、Slack 集成、多用户 Concert 插件的服务端）；本地化（Localization Dashboard 全流程）。这些模块不进 Shipping 包，是团队产能引擎。'

PLUGIN_CAT_NOTES = [
 ('Animation', 83, '动画生产链全覆盖：压缩（ACLPlugin）、程序化绑定（ControlRig "Framework for animation driven by user controls"）、重定向（IKRig）、外部流入（LiveLink）、性能（AnimationBudgetAllocator 动画预算分配）、共享姿势（AnimationSharing）。做角色动画技术方案基本绕不开这一类。'),
 ('Virtual Production', 73, '虚拟摄制全家桶：nDisplay 多屏（DisplayClusterLaunch）、虚拟相机（VCam/CineCameraRigs）、实时合成（Composite/Composure）、远程控制（RemoteControl）、关卡快照（LevelSnapshots）、Switchboard 统一启动器。是片场级虚拟化拍摄的工具箱。'),
 ('Editor', 67, '编辑器生产力：建模模式（ModelingToolsEditorMode）、PCG 程序化内容生成（"Visual scripting framework for procedurally populating worlds"）、电子表格式批量编辑（ObjectMixer "Edit any properties of scene objects in a spreadsheet format"）、多用户协作（MultiUserClient）、崩溃恢复（DisasterRecoveryClient）。'),
 ('Media Players', 41, '按平台/格式的播放器矩阵：ElectraPlayer（跨平台流媒体主力）、ImgMedia（EXR 序列/LED 墙）、平台原生（AvfMedia/WindowsMoviePlayer/WebMMedia）、采集卡（AjaMedia）。配合 Media 框架三件套选用。'),
 ('Online Platform', 36, '在线服务矩阵：OnlineSubsystemUtils + 各平台实现（EOS/GooglePlay/iOS/Xbox），覆盖账号/好友/成就/匹配/语音。新一代统一入口是 OnlineServices 体系。'),
 ('Audio', 33, '音频高阶体系：MetaSound（DSP 图式音源，"complete control over audio DSP graph generation"）、参数调制（AudioModulation）、空间声场（ResonanceAudio/SoundFields）、采集（AudioCapture）、调优（AudioInsights）。'),
 ('Gameplay', 29, '玩法框架级组件：GAS（GameplayAbilities "Adds GameplayEffect and GameplayAbility classes to handle complicated gameplay interactions"）、模块化玩法（ModularGameplay + GameFeatures 插件化内容）、通用状态机（StateTree "General purpose hierarchical state machine"）、智能对象（SmartObjects）、对话树（CommonConversation）。'),
 ('Rendering', 26, '渲染扩展与调试：自定义/程序化网格组件（CustomMeshComponent/ProceduralMeshComponent）、色彩管理（OpenColorIO）、GPU 调试（RenderDocPlugin/PixWinPlugin/DumpGPUServices）、体渲染工具（Volumetrics）。'),
 ('Physics', 24, 'Chaos 专用玩法层：解算器（ChaosSolverPlugin）、布料（ChaosCloth/ChaosClothAsset 板型布料资产）、物理控制（PhysicsControl）、破碎辅助（PlanarCut 平面切割）。'),
 ('Importers', 22, '数据进口：Datasmith 工业管线（CAD/C4D/Revit）、Alembic/USD/SpeedTree/AxF 专用导入器。配合 Interchange 框架自定义扩展。'),
 ('Testing', 20, '测试基建：Gauntlet 整包自动化（"helper class for creating and managing tests in your game"）、自动化性能测试（AutomatedPerfTesting）、自动化 RPC（AutomationControllerRpc）。'),
 ('FX', 10, '特效全家桶：Niagara 本体 + 流体（NiagaraFluids "Fluid simulation toolkit for Niagara"）、Nanite 渲染器（NiagaraNanite）、仿真缓存回放（NiagaraSimCaching）、旧系统 Cascade 与迁移器（CascadeToNiagaraConverter）、AI 工具（NiagaraToolsets）。'),
 ('AI', 11, 'AI 增强：Mass 人群/交通（MassAI/MassCrowd）、环境查询编辑器、HTN 规划器（实验）、机器学习（LearningAgents "machine learning library for AI character control"、MLAdapter RPC 训练桥）。'),
 ('UI', 11, 'UI 体系增强：CommonUI（"A repository for game independent UI elements" 主机级 UI 库）、MVVM（SlateModelViewViewModel/ModelViewViewModelPreview）、即时模式（SlateIM "immediate mode wrapper for Slate"）、预览调试（UMGWidgetPreview）、AI 操控（UMGToolSet）。'),
 ('Geometry', 11, '几何/毛发：GeometryScripting（蓝图几何函数库）、毛发渲染模拟（HairStrands "Rendering and simulation of grooms"）、发卡生成（HairCardGenerator）、几何集合（GeometryCollectionPlugin）、几何数据流（GeometryDataflow/GeometryFlow）。'),
 ('Scripting', 9, '脚本与数据科学：PythonScriptPlugin（编辑器 Python）、EditorScriptingUtilities、SequencerScripting（序列脚本化）、ML Python 包（PyTorch/TensorBoard/MLflow 自动装）。'),
 ('MetaHuman', 12, '数字人官方套件：MetaHuman 本体、生成器（MetaHumanGenerator "AI-driven character creation and editing"）、校准诊断、动画工具、UAF 支持。'),
 ('Virtual Reality', 12, 'XR 标准与外设：OpenXR 标准（"OpenXR is an open VR/AR standard"）+ 手部追踪/眼动/面捕扩展、MixedRealityCapture 混合现实采集框架。'),
 ('ML', 5, 'NNE 推理后端矩阵：ONNX Runtime（CPU/GPU）、IREE（MLIR 编译栈）、CoreML（苹果）、RDG（渲染图内推理）——同一 NNE 模型资产四种部署路径。'),
 ('Input Devices', 10, '输入外设：RawInput（飞行摇杆/方向盘）、GameInput（新一代统一输入 API）、MIDI/OSC（音乐与演出控制）、数位笔（StylusInput）。'),
 ('Water', 4, '水系统：Water 主体（"oceans, river, lakes or custom water bodies that carve landscape and interacts with gameplay"）、浮力（Buoyancy）、高级模拟（WaterAdvanced 基于 Niagara Fluids）。'),
 ('Compositing', 7, '实时合成：新一代 Composite/CompositeCore（带默认 holdout 管线）、镜头畸变（OpenCVLensDistortion 校准与置换图）。'),
]

BP_WORKFLOWS = [
 ('生成与查找 Actor', 'Actor 分类（32 子项）', 'SpawnActor 系列 + Get All Actors Of Class / Find Nearest Actor / Actor Has Tag——游戏脚本的第一入口；配 Game 分类的 Add Component by Class、Construct Object from Class 做运行时组装。'),
 ('物理交互', 'Physics 分类（136 子项）', 'Add Force / Add Impulse（含 At Location/Local/All Bodies Below 变体）、Add Radial Force、物理混合权重（Accumulate All Bodies Below Physics Blend Weight）——爆炸冲击波、拖拽物体、布娃娃过渡全靠这套。'),
 ('碰撞查询', 'Collision 分类（83 子项）', 'Box/Capsule/Sphere 的 Overlap 与 Trace 全家桶（By Channel/By Profile/For Objects 三种过滤）——命中判定、视线检测、范围伤害的标准做法，不用写一行物理代码。'),
 ('AI 行为', 'AI 分类（38 子项）+ Blackboard（12）', 'AI MoveTo + Get/Set Blackboard 变量 + EQS 查询——巡逻/追击的最小闭环；复杂逻辑下沉到行为树资产，蓝图只做感知响应。'),
 ('输入响应', 'Input 分类（108 子项）', 'Enhanced Input 体系：Add Mapping Context 动态切换输入上下文（走路 vs 开车 vs 菜单），Input Action 值的 Break/组合——手游手柄键盘三端一套映射。'),
 ('多人判定', 'Networking 分类（14 子项）', 'Has Authority / Is Server / Get Local Role 分支权威逻辑，Set Replicates / Set Net Dormancy / Force Net Update 控制复制行为——蓝图多人游戏的全部开关。'),
 ('特效驱动', 'Niagara 分类（177 子项，全站第一梯队）', 'Set/Get 全类型参数、Parameter Collection 覆盖、Advance Simulation by Time 手动步进、Sim Cache 回放——除了拼特效还能当 GPU 计算的外围控制面。'),
 ('相机与过场', 'Camera（121）+ Cinematics（9）', 'Activate Camera for Player / 相机系统叠加激活（Camera Rig 分层）、镜头特效（Lens Effect）；Sequencer 分类（22 子项）播放关卡序列做脚本化演出。'),
 ('标签驱动玩法', 'GameplayTags 分类（42 子项）', '容器匹配查询（Does Container Match Tag Query）、标签变化事件绑定、按标签查 Actor——免硬编码字符串的状态/能力标记系统。'),
 ('技能系统（GAS）', 'GameplayAbilities 分类（13 子项）', 'Give Ability / Clear Ability / Find All Abilities with Tags——装备驱动技能装卸；配 GameplayEffect/Attribute 分类做数值养成。'),
]

PY_RECIPES = [
 ('资产批量治理', 'unreal.EditorAssetLibrary + unreal.AssetRegistryHelpers', '按目录/类/标签筛资产，批量改名/迁移/设标签/校验引用；配合脚本做资产命名规范 CI 卡点。'),
 ('关卡批量操作', 'unreal.EditorLevelLibrary / unreal.LevelEditorSubsystem', '遍历关卡 Actor、批量替换/移动/设置属性、合并小关卡；世界分区地块批量处理。'),
 ('引用链分析', 'unreal.AssetRegistry（依赖/引用查询）', '查谁引用了这个材质/贴图，删除前安全检查；生成资产依赖图谱报表。'),
 ('程序化内容生成', 'unreal.EditorLevelLibrary + PCG/GeometryScript 蓝图库', 'Python 驱动参数扫描：调 PCG 种子/参数批量生成变体并截图归档。'),
 ('材质批量改写', 'unreal.MaterialEditingLibrary', '遍历材质图节点改参数/换贴图/批量创建材质实例（MIC）；做材质版本迁移脚本。'),
 ('动画资产管线', 'unreal.AnimSequence / SkeletalMeshEditorSubsystem', '批量设置压缩设置/通知/根运动、重定向到新骨架、导出元数据表。'),
 ('Sequencer 自动化', 'unreal.LevelSequence + Sequencer Scripting 插件', '批量生成/修改序列轨道、绑定轨迹、按表格生成镜头序列。'),
 ('构建前钩子', 'unreal.SystemLibrary / 任意 EditorSubsystem', '在 CI 里以 Commandlet 跑 Python 脚本完成数据校验、自动提交资产快照。'),
]
