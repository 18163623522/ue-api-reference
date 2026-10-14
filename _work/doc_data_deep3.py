# -*- coding: utf-8 -*-
# 深度分析第三层：子系统体系、角色分类学、模块解剖（反射密度）、4.27→5.8 演化、学习路径
# 数据来源：engine_modules_merged.json 统计 + diff_427_58.json（4.27 组页差分）

SUBSYS = {
 'intro': 'Subsystem（子系统）是 5.x 时代替代"单例 Manager"的标准服务模式。引擎里的定义方式完全一致——官方 Remarks 用同一句话式：*"Base class for auto instanced and initialized systems that share the lifetime of the X"*（自动实例化与初始化、与 X 共享生命周期的系统基类），X 分别是 Engine / GameInstance / World / Local Player / Editor。也就是说：**子系统=按生命周期自动管理的全局服务**，你只管实现类，引擎按作用域自动创建销毁，蓝图/Python/编辑器处处可直接取用（BP 的 Get Subsystem 节点、Python 的 unreal.get_engine_subsystem() 系）。',
 'families': [
  ('EngineSubsystem', '进程级', '随引擎/程序进程存续。适合与具体游戏无关的服务（如 Quartz 音频时钟 UQuartzSubsystem、资产注册表类服务）。'),
  ('GameInstanceSubsystem', '游戏实例级', '跨关卡存续、随游戏实例销毁。放"整局游戏"的状态与服务（网络会话管理、MOD 加载器）。'),
  ('WorldSubsystem', '世界级', '随每个 UWorld 创建销毁。放场景逻辑服务（导航、Mass 的实体管理器宿主 UMassEntitySubsystem 即此类）。'),
  ('LocalPlayerSubsystem', '本地玩家级', '每本地玩家一个实例（分屏/多视口各一份）。放按玩家的输入/相机/UI 服务。'),
  ('EditorSubsystem', '编辑器级', '仅编辑器进程。脚本期暴露面（UUnrealEditorSubsystem "Subsystem for exposing editor functionality to scripts"、ULevelEditorSubsystem、UStaticMeshEditorSubsystem 等成套出现）。'),
 ],
 'stats': '全引擎 494 模块共 85 个 Subsystem 类（Editor 家族 13、Engine 家族 8、World 4、GameInstance 2、LocalPlayer 2，其余为派生/变体）；分布最集中的宿主是 Engine（28 个，含全部基类）与 UnrealEd（14 个）。',
 'quotes': [
  ('Engine', 'UEngineSubsystem', 'Base class for auto instanced and initialized systems that share the lifetime of the Engine', '与引擎同生命周期的子系统基类'),
  ('EditorSubsystem', 'UEditorSubsystem', 'Base class for auto instanced and initialized systems that share the lifetime of the Editor', '与编辑器同生命周期——同一句式定义，换个作用域就是新家族'),
  ('LevelEditor', 'ULevelEditorSubsystem', 'Subsystem for exposing Level Editor related functionality to scripts', '"把编辑器功能暴露给脚本"是编辑器子系统的典型用途'),
 ],
 'uses': ['把项目里的 Manager 类改造成子系统：自动生命周期+蓝图/Python 原生可达，告别手写单例', '按作用域选型：跨关卡状态用 GameInstance 系、场景服务用 World 系、编辑器工具用 Editor 系', '发现可复用服务：在模块页搜 "Subsystem" 后缀即可枚举该领域的官方服务面'],
}

ROLE_TAXONOMY = [
 ('*Component（组件）', 199, '挂在 Actor 上的功能单元（USpringArmComponent/UAIPerceptionComponent…）。组件数是模块"玩法可用性"的直观指标。'),
 ('*Settings（设置）', 197, '配置对象（UDeveloperSettings 派生）。一个模块带 Settings 类=它有项目设置面板入口。'),
 ('*Proxy（代理）', 121, '两种语义要区分：U*Proxy 多为蓝图异步节点的工作对象（如 UAIAsyncTaskBlueprintProxy）；F*SceneProxy/F*RenderProxy 是渲染线程的镜像数据（游戏线程不可直接碰的渲染态）。同名后缀不同世界。'),
 ('*Library（函数库）', 102, '静态函数集合（BlueprintFunctionLibrary 形态），Runtime 组占 86 个——引擎把能力"倒"进蓝图的标准容器，也是查"这功能蓝图怎么调"的最快入口。'),
 ('*Subsystem（子系统）', 85, '按生命周期自动管理的服务（见上文专节）。'),
 ('*Instance（实例）', 41, '运行期单例/实例包装（UGameInstance 之外的零散模式）。'),
 ('*DataAsset（数据资产）', 4, '纯数据资产类（多数数据资产类不带此后缀，用 UPrimaryDataAsset 系，此处仅统计字面后缀）。'),
]

ANATOMY = [
 # 模块, 类数, 反射密度(U/A%), F%, S%, 解读
 ('AIModule', 195, 92, 6, 0, '全引擎反射密度最高的大模块——AI 面完全向蓝图/编辑器开放'),
 ('MovieScene', 118, 82, 15, 0, '序列几乎全是 UObject：轨道/节都做成资产对象，天然可编辑'),
 ('MassEntity', 21, 76, 23, 0, 'ECS 内核却保持高反射——官方刻意让 Mass 可被蓝图观测与配置'),
 ('UMG', 203, 69, 27, 2, 'UI 的 UObject 包装层，正是为了蓝图可拼'),
 ('UnrealEd', 857, 62, 29, 6, '编辑器=UObject 世界 + 54 个 Slate 控件 + 29 个 Settings'),
 ('Engine', 2456, 55, 41, 0, '玩法主体：131 个 Actor + 101 个组件 + 49 个 Proxy，反射与性能并存'),
 ('AudioMixer', 28, 28, 71, 0, '混音核心以 F 为主，U 类只留服务面（Quartz/Bus 子系统）'),
 ('CoreUObject', 392, 17, 70, 0, '反射系统本身大多是 F 实现——"制造反射的机器不需要反射"'),
 ('NetCore', 47, 6, 78, 0, '复制管线纯 C++，U 类只留驱动与连接面'),
 ('SlateCore', 140, 5, 70, 10, 'UI 框架本体非反射（性能），控件树由 S 构成'),
 ('GeometryCore', 232, 0, 47, 0, '几何算法库零反射——纯数据与函数（其余为 T 模板）'),
 ('Chaos / RenderCore / RHI / Core', 644 + 283 + 124 + 927, 0, 80, 0, '物理内核/渲染公共层/RHI/基础库全部 0% 反射、F 类占 62~95%（表中为四模块均值）——离硬件越近反射越零；性能敏感内核通过上层模块（ChaosSolverEngine、Renderer）包出 UObject 面'),
]

ANATOMY_NOTE = '把每个模块的类按 U/A（反射可见）、F（纯 C++）、S（Slate）统计占比，得到一条**反射密度谱**：它实际度量的是"这个模块离设计师多近、离硬件多近"。写代码选落点时可以用它判断：想在 Engine/AIModule/MovieScene 这类高反射模块扩展，蓝图与编辑器会自然受益；想在 Chaos/RHI 这类 0% 模块扩展，就是在写引擎内核，必须考虑线程、性能与上层包装。'

EVOLUTION = {
 'counts': '引擎模块（三组）4.27 共 419 个 → 5.8 共 494 个（Runtime 183→246、Editor 128→139、Developer 108→109）；插件条目 983→842 是**粒度重组**而非缩水：4.27 的 PluginIndex 把插件子模块（*Editor/*Factory/*Core）也当条目列，5.8 拆成"842 插件 + 1375 插件模块"两层，对比新增名单时要过滤这批假新增/假删除。',
 'runtime_added_themes': [
  ('Mass 全家入驻 Runtime', ['MassCore','MassEngine','MassEntity','MassDeveloper','MassSignals'], 'ECS 框架从实验插件升格为引擎模块——大规模实体成为一等公民'),
  ('新语言与 AI', ['VerseCompiler','uLangCore','uLangJSON','uLangUE','NNE'], 'Verse 语言编译器与神经网络引擎 NNE 进入 Runtime'),
  ('消息协议矩阵', ['XMPP','Stomp','WebSocketServer','IPC','ExternalRpcRegistry'], 'IM/消息总线类协议模块化，服务化架构准备'),
  ('音频解码器归位', ['OpusAudioDecoder','VorbisAudioDecoder','AdpcmAudioDecoder','RadAudioDecoder','AudioChannelAgnosticCore','AudioLinkCore'], '解码器从 Developer 的 AudioFormat* 重组为 Runtime 模块 + AudioLink 对外混音器桥'),
  ('GDK/发行三件', ['GDKRuntime','GDKSaveGameSystem','GDKPackageManifest'], 'Xbox/商店生态的运行时支撑入模块'),
  ('遥测与观测', ['Instrumentation','StudioTelemetry','HardwareSurvey','TraceBasedDebuggers','TraceBasedDebuggersAnalysis','BandwidthDebugDelegates','BandwidthMeasurementTool'], '运行时观测面持续加厚'),
  ('内容分发', ['IoStoreOnDemandCore','BackgroundHTTP','BackgroundHTTPFileHash','RuntimeAssetCache','IndexedCacheStorage'], '按需流送/热更基建下沉为引擎模块'),
  ('CAD 与几何', ['CADKernelEditor','CADKernelEngine','DataflowSimulation'], 'CAD 内核全链路 + Dataflow 仿真的引擎化'),
 ],
 'dev_shift': 'Developer 组 +21/-20，数字平稳但**换代剧烈**：老 Profiler 系（ProfilerClient/ProfilerService/ProfilerMessages/RealtimeProfiler）整体退场，被 Trace 系（TraceInsightsCore/TraceInsightsFrontend/TraceTools）取代——这就是 Unreal Insights 取代旧 Profiler 的模块级证据；TextureFormat*/AudioFormat* 等"格式模块"从 Developer 组消失（挪入平台层）；新增全是协作与构建加速（SlackIntegrations/SubmitToolCore/UbaCoordinatorHorde/ZenOplogUtils）。',
 'editor_shift': 'Editor 组 +17/-6：Cascade（旧粒子编辑器模块）退场（转为插件形态保遗留资产）、SettingsViewer/ProjectSettingsViewer 合并进新配置体系；新增 MassEntityDebugger/Editor、ZenEditor、UniversalObjectLocatorEditor、WorldBookmark——大世界与新存储的编辑器配套。',
 'plugin_births': '4.27 没有而 5.8 出生的标志性插件（按主题）：**MetaHuman 全家**（MetaHuman/Generator/Calibration*/AnimationTools/Crowd/SDK）、**Electra 播放器矩阵**（ElectraPlayer/ElectraCodecs + 各解码器）、**新动画框架 UAF**（UAF/UAFAnimGraph/UAFControlRig/UAFMass/UAFPoseSearch/UAFChooser 等 13 个）、**Chaos 玩法化**（ChaosOutfitAsset/ChaosFleshGenerator/ChaosModularVehicle/ChaosRigidAsset）、**Mover 移动新框架**、**StateTree/SmartObjects 引擎化前的插件生态**、**OnlineServices 新在线体系**（OnlineServices* + EOSVoiceChat）、**Pixel Streaming 2**、**OpenXR 全面接管 XR**、**CaptureManager/虚拟摄制扩容**（Composite/ComposureShared/StageMonitoring）、以及 **ModelContextProtocol/CmdLinkServer**（AI 工具链接口，5.8 很新的动向）。',
 'plugin_deaths': '确认真死亡的代表性插件：Oculus 系（OculusAudio/OnlineSubsystemOculus→Meta 迁移 OpenXR+EOS）、GoogleARCore 系（被 OpenXR 吸收）、旧在线体系（Party/Lobby/Qos/Rejoin→OnlineServices）、MegascansPlugin（并入 Fab 生态）、SteamAudio、AzureSpatialAnchors、PlasticSourceControl（4.27 收录、5.8 移除）。',
}

LEARN_PATH = [
 ('游戏框架', 'Engine', 'AActor → UActorComponent → AGameModeBase → UGameplayStatics'),
 ('对象系统', 'CoreUObject', 'UObject → UClass → FSoftObjectPath → FObjectInitializer'),
 ('物理', 'Chaos + ChaosSolverEngine', 'UChaosSolver → FGeometryCollection → UFieldSystemComponent'),
 ('渲染', 'RenderCore + Renderer', 'FVertexFactory → FSceneInterface → FSceneRenderer 系'),
 ('UI', 'Slate + UMG', 'SWidget → SWindow → UWidget → UUserWidget'),
 ('AI', 'AIModule', 'AAIController → UBehaviorTreeComponent → UAIPerceptionComponent'),
 ('Sequencer', 'MovieScene + LevelSequence', 'UMovieSceneSequence → ULevelSequence → ULevelSequencePlayer'),
 ('网络', 'NetCore', 'UNetDriver → FGuidReferences(NetGUID 机制) → FConnectionHandle'),
 ('资产管线', 'AssetRegistry + InterchangeCore', 'IAssetRegistry → FAssetRegistryState → UInterchangePipelineBase'),
 ('编辑器扩展', 'UnrealEd + EditorSubsystem 模块', 'UEditorSubsystem → FAssetTypeActions_Base(AssetTools) → UAssetDefinition'),
 ('Mass', 'MassEntity', 'UMassEntitySubsystem → UMassSpawner → Processor 模式'),
 ('音频', 'AudioMixer', 'UQuartzSubsystem → FMixerAudioBus → MetaSound 插件'),
]
