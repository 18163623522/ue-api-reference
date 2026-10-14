# -*- coding: utf-8 -*-
# 深度分析第四层：条目类型分布（数据重/行为重）、Python 面形态、Top 模块内部导览、三层对照表

SECTION_TYPES = {
 'intro': '模块页不止 Classes 一张表——Structs（全引擎 10,671 条）、Enums（3,778）、Interfaces（1,709）与 Classes 之间的比例本身就是模块性格的诊断指标。**结构体/类比值**高的模块是"数据编排系统"（状态与描述符多、行为对象少），比值低的模块是"行为系统"（大量活跃对象）。',
 'struct_heavy': [
  ('MovieScene', 656, 118, 5.6, '序列=数据编排：轨道求值靠海量求值模板/通道结构体驱动，行为类极少'),
  ('TypedElementFramework', 185, 55, 3.4, '行/列/元数据模型——数据表式设计'),
  ('IrisCore', 228, 116, 2.0, '新复制系统以"状态描述符"数据为核心（对照 NetCore 的行为型设计，两代架构风格差一目了然）'),
  ('RHI', 214, 124, 1.7, '资源/管线状态描述符密集'),
  ('Core', 1070, 927, 1.2, '容器与数学本就是数据结构'),
  ('Chaos', 320, 644, 0.5, '行为系统：大量解算器/粒子对象'),
  ('UnrealEd', 270, 857, 0.3, '编辑器以工具对象为主'),
 ],
 'iface_dense': '**接口密度**（接口数相对类数）则标出"扩展点优先"的模块——它们以少量实现+大量接口邀请你注入自己的逻辑：TraceServices（61 接口 / 19 类，Insights 的分析提供者全是接口）、DatasmithCore（59/21）、SequencerCore（47/60）、PropertyEditor（45/43，属性编辑全靠接口注入）、InteractiveToolsFramework（44/196，工具/目标皆接口）、AudioExtensions（41/23）、DerivedDataCache（34/40）。给这些模块写扩展时，先翻 Interfaces 节而不是 Classes 节。',
}

PY_SURFACE = {
 'theme': [
  ('Material*', 470), ('Anim*', 235), ('Niagara*', 147), ('Editor*', 71), ('Meta*', 66),
  ('Data*', 57), ('Level*', 52), ('Audio*', 50), ('Nav*', 44), ('Control*', 38),
  ('Cam*', 37), ('AI*', 35), ('Gameplay*', 35),
 ],
 'facts': [
  'Material* 是最大的主题群（470 类）——材质图的程序化读写面在 Python 里最厚，材质管线自动化是 Python API 的第一强项',
  '196 个 *Library* 函数库类 + 62 个 *Subsystem 结尾类——C++ 侧的"函数库暴露模式"与"子系统服务模式"在 Python 面原样复现',
  '618 个 Delegate 类型是 C++ 动态委托的直接映射（ActorBeginOverlapSignature / ActorComponentActivatedSignature 等）——意味着 Python 脚本也能挂引擎事件回调（编辑器场景下做监听式自动化）',
  '4,106 个 Struct 让"传参"几乎都有类型化载体（Vector/Transform/各资产导入设置），写脚本不必拼字典',
 ],
}

MODULE_GUIDE = [
 ('Engine', [
  ('AController', 'Controllers are non-physical actors that possess a Pawn to control its actions.', '控制器的本质：非物理 Actor，占有 Pawn 来驱动它'),
  ('AInfo', 'Info, the root of all information holding classes.', '所有"信息载体"类的根（GameMode/PlayerState 等挂在它下面）'),
  ('APlayerState', 'A PlayerState is created for every player on a server', '每个玩家一份的服务器侧状态（名字/分数的归所）'),
  ('UCheatManager', 'Cheat Manager is a central blueprint to implement test and debug code and actions that are not to ship…', '作弊/调试命令的集中地——"不随游戏发行"的测试动作'),
  ('UInstancedStaticMeshComponent', 'A component that efficiently renders multiple instances of the same StaticMesh.', '高效渲染同网格多实例——植被/森林/人群的标准件'),
  ('UCapsuleComponent / USphereComponent / UBoxComponent', 'generally used for simple collision. Bounds are rendered as lines in the editor.', '三大碰撞基元——角色胶囊体的老家'),
  ('UMaterial', 'A Material is an asset which can be applied to a mesh to control the visual look of the scene.', '材质资产定义'),
  ('UExponentialHeightFogComponent', 'Used to create fogging effects…with a density that is related to the height of the fog.', '指数高度雾'),
 ]),
 ('Core', [
  ('FArchive', 'Base class for archives that can be used for loading, saving, and garbage collecting in a byte order neutral way', '归档器：一个抽象同时服务序列化/存档/垃圾回收三件事——引擎最经典的接口复用'),
  ('FRunnable / FThread', 'Interface for "runnable" objects. / Simple API for system threads.', '线程的官方姿势：Runnable 接口 + FThread 包装'),
  ('TArray / FString / FName', 'Templated dynamic array / A dynamically sizeable string / Public name, available to the world.', '三大基础类型；FName 走全局名表（"对世界公开的名字"）'),
  ('FColor / FGuid / FDateTime', 'Stores a color with 8 bits…/ Implements a globally unique identifier / Implements a date and time', '常用值类型的家'),
 ]),
 ('CoreUObject', [
  ('FProperty', 'An UnrealScript variable.', '属性反射类——Remarks 仍写着历史名 UnrealScript：反射系统从 UE3 脚本时代一路演化而来'),
  ('UObjectBase', 'Low level implementation of UObject, should not be used directly in game code', 'UObject 的低层实现（游戏代码不应直用）'),
 ]),
 ('Chaos', [
  ('FBasicBroadPhase', '…pass them onto the collision detector if their AABBs overlap.', '宽相筛对'),
  ('FCCDModifier', '…modify the results of CCD collision detection prior to the CCD rewind being applied.', 'CCD 修正点'),
  ('FGeometryCollection', '( FTransformCollection )', '可破坏资产的分层网格数据结构（继承自变换集合）'),
 ]),
 ('UnrealEd', [
  ('UEditorEngine', 'Engine that drives the Editor.', '编辑器引擎本体'),
  ('FAssetEditorToolkit', 'Base class for toolkits that are used for asset editing (abstract)', '资产编辑器容器基类'),
  ('FAssetDeleteModel', 'The model behind a delete operation, which is an asynchronous process because of all the checks…against the GC', '删资产是异步的——引用与 GC 检查决定了编辑器的每次删除'),
 ]),
 ('MovieScene', [
  ('UMovieScene', 'Implements a movie scene asset.', '序列资产'),
  ('FInterrogationChannels（MovieSceneTracks）', '…interrogating Sequencer entity data without applying any state to objects.', '无副作用审讯序列数据'),
 ]),
 ('AIModule', [
  ('AAIController', 'AIController is the base class of controllers for AI-controlled Pawns.', 'AI 控制器'),
  ('UAIPerceptionComponent', '…register as stimuli listener in AIPerceptionSystem and gathers registered stimuli', '感知监听'),
  ('UBTTaskNode', 'Task are leaf nodes of behavior tree, which perform actual actions', '行为树叶节点'),
 ]),
]

XREF = [
 # 功能, C++ 模块/类, BP 分类, Python 类
 ('静态网格', 'Engine: UStaticMeshComponent / UStaticMesh', 'Static Mesh（BP 分类）', 'unreal.StaticMesh / StaticMeshEditorSubsystem'),
 ('骨骼网格与动画', 'Engine: USkeletalMeshComponent；AnimGraphRuntime', 'Animation（140 子项）/ Skeletal Mesh', 'unreal.SkeletalMesh* / AnimSequence* / SkeletalMeshEditorSubsystem'),
 ('材质', 'Engine: UMaterial；RenderCore: 顶点工厂', 'Materials / Material（BP 节点）', 'unreal.Material*（470 类最大群）/ MaterialEditingLibrary'),
 ('物理与破坏', 'Chaos / ChaosSolverEngine: UChaosSolver；FieldSystemEngine', 'Physics（136）/ Chaos / Destruction', 'unreal.GeometryCollection* / PhysicsUtils（插件）'),
 ('碰撞查询', 'Engine: UPrimitiveComponent；PhysicsCore', 'Collision（83 子项：Overlap/Trace 全家桶）', 'unreal.SystemLibrary（Box Trace 等）'),
 ('特效', 'Niagara 插件（引擎外）', 'Niagara（177 子项）', 'unreal.Niagara*（147 类）'),
 ('AI 行为', 'AIModule: AAIController/BT/Perception', 'AI（38）/ Blackboard / Behavior Tree', 'unreal.AISystem / AIBlueprintHelperLibrary'),
 ('导航', 'NavigationSystem / Navmesh', 'Navigation / Nav Mesh', 'unreal.NavigationSystemV1'),
 ('输入', 'InputCore；EnhancedInput 插件', 'Input（108）/ Enhanced Input', 'unreal.EnhancedInput*'),
 ('UI', 'Slate/SlateCore + UMG: UUserWidget', 'UMG / Widget 各分类', 'unreal.UserWidget / WidgetBlueprint*（配 UMGToolSet 插件）'),
 ('过场/时间线', 'MovieScene/LevelSequence: ULevelSequencePlayer', 'Sequencer / Level Sequence / Cinematics', 'unreal.LevelSequence*（配 Sequencer Scripting 插件）'),
 ('网络复制', 'NetCore: UNetDriver；IrisCore（新一代）', 'Networking（14 子项：Has Authority 等）', '（运行时系统，Python 面基本不涉及）'),
 ('音频', 'AudioMixer/SignalProcessing；MetaSound 插件', 'Audio（79）/ Meta Sound', 'unreal.Audio*（50 类）/ Metasound*'),
 ('地形植被', 'Landscape / Foliage', 'Landscape / Foliage', 'unreal.Landscape*（31 类）'),
 ('大规模实体', 'MassEntity/MassCore: UMassEntitySubsystem', 'Mass / Mass Spawner', 'unreal.MassEntity*（部分）'),
 ('资产管理', 'AssetRegistry: IAssetRegistry', 'Asset Registry / Asset Manager', 'unreal.AssetRegistry / AssetRegistryHelpers / EditorAssetLibrary'),
 ('存档', 'Engine: USaveGame（+ SaveGame 插件体系）', 'SaveGame 分类', 'unreal.SaveGame'),
 ('关卡与流送', 'Engine: ULevelStreaming；World Partition（插件组）', 'Level / Level Streaming / World Partition', 'unreal.LevelEditorSubsystem / EditorLevelLibrary'),
 ('编辑器工具', 'UnrealEd + EditorSubsystem 模块；Blutility', 'Editor Utility / Editor Scripting', 'unreal.UnrealEditorSubsystem / EditorUtilityLibrary（+ Python 本身）'),
 ('脚本自动化', '（C++ 即本体）', 'Python 分类（BP 桥）', 'unreal 模块全体（Python 本体）'),
]
