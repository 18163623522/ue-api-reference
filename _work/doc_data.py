# -*- coding: utf-8 -*-
# 文档生成用的纯数据（域映射、重点模块、插件亮点、BP 聚类规则）

DOMAIN_ORDER = [
    '核心与运行时基础', '游戏框架与玩法', '输入与 XR 设备', '渲染与图形', '物理与碰撞',
    '几何与建模', 'UI 界面', '动画与布料', 'Sequencer 与影视虚拟制片', '音频',
    'AI 与导航', '网络与在线服务', '媒体播放', '地形与植被', 'Mass 实体系统',
    '资产与内容管线', '遥测与性能分析', '自动化测试', '新兴与实验技术',
]

DOMAIN_ABILITY = {
    '核心与运行时基础': '容器/算法/字符串/线程/内存等基础设施、UObject 反射与序列化、JSON/XML/Verse 语言运行时——一切模块的地基',
    '游戏框架与玩法': 'Actor/Component/关卡/游戏模式/标签/任务等玩法骨架与运行时游戏逻辑（含启动影片、内置菜单等外围）',
    '输入与 XR 设备': '输入抽象、设备接口、眼动追踪、HMD/AR/XR 头显与语音',
    '渲染与图形': '渲染器、RHI 抽象层与 D3D12/Vulkan/OpenGL 后端、贴图与网格数据转换、材质着色质量设置',
    '物理与碰撞': 'Chaos 物理（刚体/载具/布料解算）、碰撞查询、力场与破坏（几何集合）、物理录制回放调试',
    '几何与建模': '网格描述数据结构、几何内核、CAD 内核、Dataflow 图、交互式建模工具框架（编辑器建模模式的地基）',
    'UI 界面': 'Slate 保留模式 UI 框架 + UMG 蓝图化 UI + 内嵌网页浏览器与控件渲染',
    '动画与布料': '动画图运行时、动画核心数据、Live Link 外部数据流入、布料仿真、面部捕捉 MR 网格',
    'Sequencer 与影视虚拟制片': 'Sequencer 时间线、关卡序列、影片采集编码、虚拟摄制舞台数据、Cine 摄像机',
    '音频': '音频混音器、DSP 信号处理、音频分析器/采集、Audio Link、各类音频编解码器（Opus/Vorbis/Bink/ADPCM）',
    'AI 与导航': 'AI 控制器/行为树/黑板/感知、导航系统与 Navmesh 生成查询',
    '网络与在线服务': '复制与 PacketHandler、Iris 新一代复制、Socket/HTTP/WebSocket/XMPP 消息总线、Portal 会话服务、网络回放流',
    '媒体播放': '媒体资产/播放器框架与媒体工具（视频源播放、图片下载）',
    '地形与植被': 'Landscape 地形与 Foliage 植被实例化',
    'Mass 实体系统': 'Mass Entity/ECS 式大规模实体框架（人群、环境模拟）与信号',
    '资产与内容管线': 'Asset Registry 资产注册表、Interchange 导入框架、Datasmith、Pak/IO Store 打包、按需下载、补丁分发、网络文件系统',
    '遥测与性能分析': 'Analytics 遥测后端、Trace/Insights 追踪、性能计数器、硬件调查、Rewind Debugger 接口',
    '自动化测试': '自动化测试框架运行时侧（Automation Test/Worker/Messages）',
    '新兴与实验技术': 'Verse 语言编译器、NNE 神经网络推理、VectorVM、CUDA 绑定、AutoRTFM 事务内存、StateStream',
}

DOMAIN_MODULES = {
    '核心与运行时基础': ['ApplicationCore','AppFramework','BuildSettings','Core','CoreOnline','CorePreciseFP','CoreUObject','CrashReportCore','Cbor','DeveloperSettings','EngineSettings','EventLoop','FieldNotification','Json','JsonObjectGraph','JsonUtilities','Launch','MathCore','PropertyPath','Serialization','XmlParser','uLangCore','uLangJSON','uLangUE','Projects','TypedElementFramework','TypedElementRuntime'],
    '游戏框架与玩法': ['Engine','BlueprintRuntime','GameplayMediaEncoder','GameplayTags','GameplayTasks','UELibrary','Advertising','FriendsAndChat','GameMenuBuilder','GameplayDebugger','MoviePlayer','MoviePlayerProxy','PreLoadScreen'],
    '输入与 XR 设备': ['InputCore','InputDevice','EyeTracker','HeadMountedDisplay','AugmentedReality','Overlay','Voice'],
    '渲染与图形': ['RenderCore','Renderer','RHI','RHICore','D3D12RHI','OpenGLDrv','VulkanRHI','NullDrv','ImageCore','ImageWrapper','ImageWriteQueue','IESFile','ISMPool','MaterialShaderQualitySettings','MeshConversion','MeshConversionEngineTypes','MeshUtilitiesCommon','TextureUtilitiesCommon','StreamingPauseRendering','OpenColorIOWrapper'],
    '物理与碰撞': ['Chaos','ChaosCore','ChaosSolverEngine','ChaosSpatialPartitions','ChaosVehiclesCore','ChaosVehiclesEngine','Constraints','FieldSystemEngine','RigidPhysics','PhysicsCore','Voronoi','ChaosVDData','ChaosVDRuntime'],
    '几何与建模': ['CADKernel','CADKernelEditor','CADKernelEngine','GeometryCore','GeometryFramework','GeometryCollectionEngine','MeshDescription','StaticMeshDescription','SkeletalMeshDescription','RawMesh','DataflowCore','DataflowEngine','DataflowSimulation','InteractiveToolsFramework'],
    'UI 界面': ['AdvancedWidgets','Slate','SlateCore','SlateBaseRenderer','SlateNullRenderer','SlateRHIRenderer','UMG','WidgetCarousel','WebBrowser','WebBrowserTexture','CEF3Utils'],
    '动画与布料': ['AnimGraphRuntime','AnimationCore','ClothingSystemRuntimeCommon','ClothingSystemRuntimeInterface','ClothingSystemRuntimeNv','LiveLinkAnimationCore','LiveLinkInterface','LiveLinkMessageBusFramework','MRMesh'],
    'Sequencer 与影视虚拟制片': ['AVEncoder','AVIWriter','CinematicCamera','LevelSequence','MovieScene','MovieSceneCapture','MovieSceneTracks','SequenceRuntimeRecorder','SerializedRecorderInterface','StageDataCore','TimeManagement','VirtualProduction'],
    '音频': ['AdpcmAudioDecoder','AudioAnalyzer','AudioCaptureCore','AudioCaptureRtAudio','AudioChannelAgnosticCore','AudioExtensions','AudioLinkCore','AudioLinkEngine','AudioMixer','AudioMixerCore','AudioPlatformConfiguration','BinkAudioDecoder','NonRealtimeAudioRenderer','OpusAudioDecoder','RadAudioDecoder','SignalProcessing','SoundFieldRendering','VorbisAudioDecoder'],
    'AI 与导航': ['AIModule','Navmesh','NavigationSystem'],
    '网络与在线服务': ['BandwidthDebugDelegates','BandwidthMeasurementTool','ClientBandwidthDebugVisualizer','ClientPilot','DownlinkBandwidthManager','EngineMessages','ExternalRpcRegistry','HTTP','HttpNetworkReplayStreaming','HttpServer','Icmp','InMemoryNetworkReplayStreaming','IPC','IrisCore','LocalFileNetworkReplayStreaming','Messaging','MessagingCommon','MessagingRpc','NetCommon','NetCore','NetworkReplayStreaming','Networking','NullNetworkReplayStreaming','PacketHandler','PortalMessages','PortalRpc','PortalServices','ReliabilityHandlerComponent','RSA','SSL','SaveGameNetworkReplayStreaming','SessionMessages','SessionServices','Sockets','Stomp','WebSockets','WebSocketServer','XMPP','GDKRuntime','GDKSaveGameSystem','GDKPackageManifest'],
    '媒体播放': ['ImageDownload','Media','MediaAssets','MediaUtils'],
    '地形与植被': ['Foliage','Landscape'],
    'Mass 实体系统': ['MassCore','MassDeveloper','MassEngine','MassEntity','MassSignals'],
    '资产与内容管线': ['AssetRegistry','BackgroundHTTP','BackgroundHTTPFileHash','BuildPatchServices','DatasmithCore','DumpPackageToJson','IndexedCacheStorage','InterchangeCore','InterchangeEngine','IoStoreOnDemandCore','NetworkFile','NetworkFileSystem','PakFile','RuntimeAssetCache','SandboxFile','StreamingFile','UniversalObjectLocator','InstallBundleManager','LauncherCheck','LauncherPlatform'],
    '遥测与性能分析': ['Analytics','AnalyticsCSV','AnalyticsET','AnalyticsHorde','AnalyticsLog','AnalyticsSwrve','AnalyticsVisualEditing','HardwareSurvey','Instrumentation','PerfCounters','StudioTelemetry','SynthBenchmark','TelemetryUtils','TraceBasedDebuggers','TraceBasedDebuggersAnalysis','TraceLog','RewindDebuggerRuntimeInterface'],
    '自动化测试': ['AutomationMessages','AutomationTest','AutomationWorker'],
    '新兴与实验技术': ['AutoRTFM','CUDA','NNE','VectorVM','VerseCompiler','StateStream'],
}

EDITOR_DOMAINS = {
    '编辑器框架与工作流': ['ActionableMessage','EditorConfig','EditorFramework','EditorStyle','EditorSubsystem','EditorToolEvents','EditorWidgets','MainFrame','LevelEditor','StatusBar','ToolMenusEditor','WorkspaceMenuStructure','GameProjectGeneration','NewLevelDialog','ProjectTargetPlatformEditor','HardwareTargeting','UATHelper','TurnkeySupport','Documentation','ConfigEditor','InputBindingEditor','JsonUtilitiesEditor','MergeActors','UndoHistoryEditor','SourceControlWindowExtender','SwarmInterface','ZenEditor','UnrealEd','UnrealEdMessages'],
    '内容浏览器与资产管理': ['AssetDefinition','AssetTagsEditor','ContentBrowser','ContentBrowserData','UserAssetTagsEditor','PackagesDialog','SubobjectDataInterface','SubobjectEditor','DataHierarchyEditor','UniversalObjectLocatorEditor','Layers','SceneOutliner','WorldBrowser','WorldPartitionEditor','WorldBookmark','DataLayerEditor','HierarchicalLODOutliner'],
    '蓝图与图编辑器': ['AIGraph','AnimGraph','BlueprintGraph','BehaviorTreeEditor','GraphEditor','Kismet','KismetCompiler','KismetWidgets','AnimationBlueprintEditor','BlueprintEditorLibrary'],
    '资产编辑器': ['AnimationEditMode','AnimationEditor','AnimationEditorWidgets','AnimationBlueprintLibrary','AnimationModifiers','AnimationSettings','AudioEditor','CurveAssetEditor','CurveEditor','CurveTableEditor','DataTableEditor','DistCurveEditor','FontEditor','MaterialEditor','MirrorDataTableEditor','PListEditor','PhysicsAssetEditor','Sequencer','SequencerCore','SequencerWidgets','SequenceRecorder','SequenceRecorderSections','MovieSceneCaptureDialog','MovieSceneTools','SkeletonEditor','SkeletalMeshEditor','StaticMeshEditor','StringTableEditor','TextureEditor','UMGEditor','SparseVolumeTexture','VirtualTexturingEditor','LandscapeEditor','LandscapeEditorUtilities','FoliageEdit','MeshPaint','ClothPainter','ClothingSystemEditor','ClothingSystemEditorInterface','Persona'],
    '视口与交互模式': ['AdvancedPreviewScene','ActorPickerMode','SceneDepthPickerMode','EnvironmentLightingViewer','LevelInstanceEditor','VREditor','ViewportInteraction','ViewportSnapping','OverlayEditor','PlacementMode','PixelInspectorModule','RenderResourceViewer','SVGDistanceField'],
    '调试与专项面板': ['GameplayDebuggerEditor','GameplayTasksEditor','MassEntityDebugger','MassEntityEditor','StatsViewer','DerivedDataEditor','DerivedDataWidgets','DeviceProfileEditor','DeviceProfileServices','PIEPreviewDeviceProfileSelector','PIEPreviewDeviceSpecification','StructUtilsEditor','StructViewer','ClassViewer','RewindDebuggerInterface'],
    '属性与 UI 定制': ['DetailCustomizations','PropertyEditor','ComponentVisualizers','CommonMenuExtensions','PinnedCommandList'],
    '工具与杂项': ['AddContentDialog','Blutility','CSVtoSVG','EditorInteractiveToolsFramework','ScriptableEditorWidgets','LocalizationCommandletExecution','LocalizationDashboard','InternationalizationSettings','PluginWarden','VirtualizationEditor'],
}

DEV_DOMAINS = {
    '构建/烘焙/DDC': ['CookMetadata','CookedEditor','DerivedDataCache','Virtualization','IoStoreUtilities','PakFileUtilities','MeshBuilder','MeshBuilderCommon','NaniteBuilder','NaniteUtilities','TextureBuild','TextureBuildUtilities','TextureCompressor','TextureFormat','ShaderCompilerCommon','ShaderFormatOpenGL','ShaderFormatVectorVM','ShaderPreprocessor','Horde','UbaCoordinatorHorde','Zen','ZenOplogUtils','MeshReductionInterface','MeshBoneReduction','MeshDescriptionOperations','MeshMergeUtilities','MeshUtilities','MeshUtilitiesEngine','Merge','HierarchicalLODUtilities','MaterialBaking','MaterialUtilities','PhysicsUtilities','SkeletalMeshUtilitiesCommon','GeometryProcessingInterfaces'],
    '平台与设备管理': ['TargetPlatform','DesktopPlatform','DeviceManager','TargetDeviceServices','TurnkeyIO','LauncherServices','LegacyProjectLauncher','GDKPlatformEditor'],
    '自动化与功能测试': ['AITestSuite','AutomationController','AutomationDriver','AutomationWindow','CQTest','FunctionalTesting','MassEntityTestSuite','StructUtilsTestSuite','ScreenShotComparison','ScreenShotComparisonTools'],
    '分析与调试前端': ['CollisionAnalyzer','DrawPrimitiveDebugger','LogVisualizer','MessageLog','OutputLog','ProfileVisualizer','ScriptDisassembler','SessionFrontend','TraceAnalysis','TraceInsights','TraceInsightsCore','TraceInsightsFrontend','TraceServices','TraceTools','GraphColor','VisualGraphUtils','TreeMap','CSVUtils','EditorAnalyticsSession'],
    '版本控制与协作': ['SourceControl','LocalizationService','SourceControlCheckInPrompt','UncontrolledChangelists','UndoHistory','UnsavedAssetsTracker','HotReload','DirectoryWatcher','SlackIntegrations','SubmitToolCore'],
    '资产工具与导入导出': ['AnimationDataController','AnimationWidgets','AssetTools','AudioSettingsEditor','BSPUtils','CollectionManager','DatasmithExporter','DatasmithExporterUI','DatasmithFacade','DirectLink','ExternalImagePicker','FileUtilities'],
    '本地化': ['Localization','TranslationEditor'],
    '编辑器支撑库': ['BlankModule','DeveloperToolSettings','Settings','SettingsEditor','SharedSettingsWidgets','SlateFileDialogs','SlateReflector','SourceCodeAccess','SourceControlViewport','StandaloneRenderer','ToolMenus','ToolWidgets','WidgetRegistration','DesktopWidgets'],
}

FEATURED = [
    ('Engine', [], '游戏世界的全部骨架：Actor/Component/关卡/光照/相机/粒子(Cascade)/声音组件、角色移动组件、蓝图运行时桥。官方对 AActor 的描述是"可放置或生成到关卡中的对象基类"，UWorld 为"代表一张地图或沙盒、容纳 Actor 与 Component 的顶层对象"'),
    ('Core', [], '引擎最底层：容器(TArray/TMap)、字符串(FString)、智能指针、线程与任务图、数学库宿主；API 面积全引擎第二'),
    ('CoreUObject', [], 'UObject 反射/序列化/GC/软引用体系：UObject（"所有 UE 对象的基类"）、UClass、UPackage、委托与属性包装'),
    ('Chaos', ['ChaosCore','ChaosSolverEngine','FieldSystemEngine'], 'Chaos 物理核心：刚体解算器、几何集合（FGeometryCollection，破坏系统的数据结构）、聚类与碰撞'),
    ('PhysicsCore', [], '物理抽象层：碰撞通道/Profile、BodyInstance 与物理接口的公共定义'),
    ('Renderer', [], '场景渲染器：延迟着色管线、光照、阴影、后处理的实现层'),
    ('RenderCore', [], '渲染公共层：着色器绑定、顶点工厂（FVertexFactory："封装可链接进顶点着色器的顶点数据源"）、GPU 统计'),
    ('RHI', ['D3D12RHI','VulkanRHI','OpenGLDrv'], '渲染硬件接口：FRHICommandList/FRHITexture 等跨 API 抽象；D3D12RHI/VulkanRHI/OpenGLDrv 为平台后端'),
    ('Slate / SlateCore', [], '保留模式 UI 框架，编辑器全部界面与运行时 HUD 的地基；SWindow 为"平台无关的顶层窗口表示"'),
    ('UMG', [], '蓝图可视化 UI：UUserWidget（"通过 WidgetBlueprint 实现 UI 可扩展性的控件"）、Button/CanvasPanel 等 UObject 包装控件'),
    ('AIModule', [], 'AI 框架：AAIController（"AI 控制 Pawn 的控制器基类"）、行为树/黑板组件、感知系统'),
    ('NavigationSystem / Navmesh', [], '导航与寻路：NavMesh 边界体积（"仅阻挡路径构建、无游戏碰撞"）、寻路查询、导航数据生成'),
    ('MovieScene / Sequencer / LevelSequence', ['MovieSceneTracks','SequencerCore','Sequencer'], 'Sequencer 时间线体系：UMovieScene（"影片场景资产"）、轨道求值、关卡序列与录制'),
    ('Landscape / Foliage', [], '地形高度场渲染与编辑、植被实例化刷绘'),
    ('MassEntity / MassCore', ['MassEngine','MassSignals'], 'ECS 式大规模实体：UMassEntitySubsystem（"承载 FMassEntityManager 默认实例的世界子系统"）、生成器与信号'),
    ('AnimGraphRuntime / AnimationCore', [], '动画图运行时求值、混合空间、动画姿势数据结构'),
    ('LiveLink 三件套', ['LiveLinkInterface','LiveLinkMessageBusFramework'], '外部动画/设备数据流入框架（动作捕捉、DCC 联动）'),
    ('AudioMixer / SignalProcessing', [], '音频混音器主框架与 DSP；配合各编解码器模块与 AudioLink 对接外部混音器'),
    ('NetCore / PacketHandler / IrisCore', [], '经典复制栈与新一代复制系统 Iris（5.x 官方在研替代方案）'),
    ('AssetRegistry', [], '资产注册表：编辑器/运行时枚举与查询项目资产（Python/蓝图的资产查询 API 即其暴露面）'),
    ('InterchangeCore / InterchangeEngine', [], '统一导入管线框架：UInterchangePipelineBase（"管线实现"）——FBX/glTF/USD 等导入器的公共架构'),
    ('UnrealEd', [], '编辑器主模块（857 类）：UEditorEngine（"驱动编辑器的引擎"）、事务/选择/PIE/工具基类'),
    ('Kismet / BlueprintGraph', [], '蓝图编辑器与蓝图编译器（Kismet 为蓝图系统内部代号）'),
    ('VerseCompiler / uLang 系列', [], 'Verse 语言（UEFN 背后的新脚本语言）编译器与运行时核心'),
    ('NNE', [], '神经网络引擎：UNNEModelData（"存储神经网络模型数据的资产"），在引擎内跑推理'),
    ('TypedElementFramework', [], '类型化元素框架：编辑器中统一表示"任何可被选中/操作的对象"的新抽象'),
    ('InteractiveToolsFramework', [], '交互式工具框架：建模模式、雕刻等编辑器工具的标准基类'),
    ('GeometryCore / MeshDescription 系列', ['GeometryFramework','StaticMeshDescription','SkeletalMeshDescription'], '几何处理库与网格数据结构（建模工具链的数据底座）'),
]

PLUGIN_HIGHLIGHTS = [
    'Niagara', 'PCG', 'Metasound', 'CommonUI', 'EnhancedInput',
    'GameplayAbilities', 'GameFeatures', 'ModularGameplay',
    'ModelingToolsEditorMode', 'Water', 'Paper2D', 'PythonScriptPlugin',
    'EditorScriptingUtilities', 'OodleNetwork', 'USDImporter', 'GLTFExporter',
    'LiveLink', 'ControlRig', 'ACLPlugin', 'AudioModulation', 'ChaosSolverPlugin',
]

BP_RULES = [
    ('动画/骨骼/Rig', ['Anim','Pose','Skeleton','Rig','Motion','Montage','Blend','IK','Retarget','Live Link','Cloth','Bone']),
    ('UI/UMG/控件', ['Widget','UMG','UI','Text','Button','Panel','Layout','Common','Slate','Scroll','List View','Carousel','Combo','Check Box','Safe Zone']),
    ('物理/碰撞/破坏', ['Physics','Collision','Chaos','Constraint','Buoyancy','Destruction','Field']),
    ('AI/导航/行为', ['AI','EQS','Blackboard','Behavior','Navigation','Nav Mesh','Crowd','Smart Object','Targeting']),
    ('渲染/材质/贴图', ['Material','Rendering','Nanite','Texture','Lighting','Lights','Ray Tracing','Virtual Texture','Render']),
    ('音频', ['Audio','Sound','Meta Sound','Music','Quartz','Submix','Synth','MIDI','Tone']),
    ('Sequencer/影视/虚拟制片', ['Sequencer','Cine','Movie','Take','Level Sequence','Composure','NDisplay','Virtual Production','VCam','Camera']),
    ('特效 Niagara', ['Niagara','FX','Particle']),
    ('网络/多人/在线', ['Networking','Replication','Online','Multi','Replay','Pixel Streaming']),
    ('输入/设备/XR', ['Input','Motion Controller','XR','AR ','Head Mounted','Eye Tracking','Virtual Keyboard']),
    ('玩法能力系统', ['Abilities','Ability','Gameplay','Attribute','Cue','Effect','Tag','State Tree','Mass']),
    ('编辑器脚本/资产工具', ['Editor','Asset','Content Browser','Dataprep','Geometry Script','Python','Automation','Utility','Blutility','Scriptable']),
    ('数学/通用工具库', ['Math','Kismet','Array','Set','Map','String','Transform','Rotation','Intersection','Date Time','Guid']),
]
