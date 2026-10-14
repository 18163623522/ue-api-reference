# Unreal Engine 官方 API 深度解读（分门别类 · 分析版）

> **版本口径**：Epic Developer Community 文档站当前默认的 **Unreal Engine 5.8**（同站可切换 4.27 ~ 5.8）  
> **数据来源**：C++ API / Blueprint API / Python API 三套官方参考体系，494 个模块页 + 842 插件 + 889 蓝图分类 + Python 全部类型页逐页提取（2026-10-08）  
> **读法**：引号内为官方文档原文（英文原句 + 中文释义），全部来自提取数据；"机制/能做什么"为基于类清单与 Remarks 的综合归纳。第一章讲透机制与逐域分析，速查清单在 1.6 与附录。

## 目录

- [0. 三套 API 体系与它们的关系](#0-三套-api-体系与它们的关系)
- [一、C++ API：引擎的骨架（494 模块 / 49,168 条 API 条目）](#一、c++-api引擎的骨架494-模块--49168-条-api-条目)
  - [1.1 先读懂四个机制（理解一切模块的钥匙）](#11-先读懂四个机制理解一切模块的钥匙)
  - [1.2 API 形态：数据驱动的观察](#12-api-形态数据驱动的观察)
  - [1.3 十九个功能域逐域分析](#13-十九个功能域逐域分析)
  - [1.4 Editor 组逐子域分析（139 个模块，8 个子域）](#14-editor-组逐子域分析139-个模块，8-个子域)
  - [1.5 Developer 组逐子域分析（109 个模块，8 个子域）](#15-developer-组逐子域分析109-个模块，8-个子域)
  - [1.6 速查：域总表与模块全清单](#16-速查域总表与模块全清单)
  - [1.7 官方插件生态：842 个插件按类能给什么能力](#17-官方插件生态842-个插件按类能给什么能力)
- [二、Blueprint API：设计师看到的那一面（889 个分类）](#二、blueprint-api设计师看到的那一面889-个分类)
  - [2.1 十六个典型工作流（节点名均取自抓取数据）](#21-十六个典型工作流节点名均取自抓取数据)
  - [2.2 全分类的功能域覆盖（关键词归纳）](#22-全分类的功能域覆盖关键词归纳)
  - [2.3 节点详情页抽样（叶级，18 个）](#23-节点详情页抽样叶级，18-个)
  - [2.4 节点宿主分布（Target is 统计）](#24-节点宿主分布target-is-统计)
  - [2.5 蓝图动词词表（零网络分析）](#25-蓝图动词词表零网络分析)
  - [2.6 结构体命名模式（零网络分析）](#26-结构体命名模式零网络分析)
  - [2.7 接口与枚举的命名模式（零网络分析）](#27-接口与枚举的命名模式零网络分析)
- [三、Python API：编辑器自动化面（unreal 模块，Experimental）](#三、python-api编辑器自动化面unreal-模块，experimental)
  - [3.1 八个典型自动化配方（代码行为示意片段，以官方类名为准）](#31-八个典型自动化配方代码行为示意片段，以官方类名为准)
  - [3.2 Python 面的形态：数据说了什么](#32-python-面的形态数据说了什么)
  - [3.3 主力类成员数排行（28 类叶级抽样）](#33-主力类成员数排行28-类叶级抽样)
  - [3.4 Python 动作类全量普查（250 个 Library/Subsystem）](#34-python-动作类全量普查250-个-librarysubsystem)
- [四、三套 API 选型与组合](#四、三套-api-选型与组合)
  - [4.1 同一功能的三层对照表（20 个高频功能）](#41-同一功能的三层对照表20-个高频功能)
  - [4.2 域能力矩阵：四路数据按 19 域合流](#42-域能力矩阵四路数据按-19-域合流)
- [五、版本口径与 4.27 → 5.8 模块演化（数据差分）](#五、版本口径与-427-→-58-模块演化数据差分)
- [附录：数据与核验](#附录数据与核验)

## 0. 三套 API 体系与它们的关系

| 参考体系 | 入口路径 | 内容形态 | 面向场景 |
|---|---|---|---|
| **C++ API Reference** | `documentation/unreal-engine/API` | 按模块分组的类/结构体/枚举/函数参考，自动从引擎源码生成 | 引擎与游戏底层开发 |
| **Blueprint API Reference** | `documentation/unreal-engine/BlueprintAPI` | 按分类目录组织的全部蓝图节点（889 个分类） | 无代码可视化脚本 |
| **Python API Documentation** | `documentation/unreal-engine/python-api` | unreal 模块全部暴露类型（11675 个类型页，官方标注 Experimental） | 编辑器自动化脚本 |

三者的真实关系是一棵暴露树：**C++ 模块实现功能**（源头，494 个引擎模块 + 842 插件），引擎通过反射（UFUNCTION/USTRUCT/UPROPERTY）把其中设计师需要的部分**暴露成蓝图节点**（889 个分类就是这些节点的目录），又把编辑器侧对象**绑定成 Python 类**（11,675 个类型页）。所以：找"某功能有没有"查 C++ 模块；找"蓝图里怎么调"查 Blueprint 分类；找"怎么批量自动化"查 Python。同一功能三处同名或近名（如 StaticMesh → UStaticMeshComponent / BP 的 Static Mesh 分类 / unreal.StaticMesh）。

## 一、C++ API：引擎的骨架（494 模块 / 49,168 条 API 条目）

官方定位（根页原文）：*"This is an automatically generated reference manual from the Unreal Engine Source code."*（从 Unreal Engine 源码自动生成的参考手册。）每个模块页固定为：头部元信息（模块名/类型/源码位置/Build.cs）+ Classes、Structs、Enums、Interfaces、Functions、Delegates、Typedefs、Variables、Constants 分节表，每行"名称 + Remarks 一行官方说明"。

四大模块组（官方定义）：**Runtime**（246 个，*"contains functionality necessary to run Unreal Engine"*——所有构建配置都编译）；**Editor**（139 个，编辑器内代码，仅编辑器目标）；**Developer**（109 个，*"only in non-shipping build configurations"*——不进发行包的开发工具）；**Plugins**（842 个插件/1375 插件模块，按项目启停）。合计 49,168 条条目：Classes 11,933、Structs 10,671、Enums 3,778、Functions 14,631、Interfaces 1,709、Typedefs 4,472。

### 1.1 先读懂四个机制（理解一切模块的钥匙）

**① UObject 反射是所有 API 形态的共同前提。** UObject 是"所有 UE 对象的基类"（官方 Remarks 原文），其反射数据 UFunction 的官方说明一语道破用途：*"Reflection data for a replicated or Kismet callable function."*（描述一个可复制或蓝图可调用的函数）——即属性/函数一旦反射，就同时获得了序列化、编辑器可见、网络复制、蓝图可调四种能力。软引用 FSoftObjectPath（*"a string reference to an object, either a package, a top level asset or a subobject"*）则支撑异步加载与流送。看懂这一点，模块页里大量 U 前缀类的设计就自明了。

**② Actor-Component 组合模型是玩法层的语法。** Engine 模块（全引擎最大，8,796 条）的定义链：AActor（*"can be placed or spawned in a level"*）→ UActorComponent（*"define reusable behavior that can be added to different types of Actors"*，官方明确把组件定位为跨 Actor 复用的行为单元）→ USceneComponent（*"has a transform and supports attachment, but has no rendering or collision capabilities"*）→ UPrimitiveComponent（*"contain or generate some sort of geometry, generally to be rendered or used as collision"*）。规则归属 AGameModeBase（*"defines the game being played"*），操纵归属 APlayerController → APawn → ACharacter（*"Pawns that have a mesh, collision, and built-in movement logic"*）。

**③ 渲染是三层栈，扩展点在中层。** RHI 做跨 API 抽象（FDynamicRHI：*"The interface which is implemented by the dynamically bound RHI"*，其下 D3D12RHI/VulkanRHI/OpenGLDrv 为后端）；RenderCore 是公共层，顶点工厂 FVertexFactory 的官方定义（*"Encapsulates a vertex data source which can be linked into a vertex shader"*）说明它是自定义几何渲染的标准挂点；Renderer 实现场景渲染器，FCachedMeshDrawCommandInfo（*"a mesh draw command which is cached in the scene"*）体现了绘制命令缓存复用架构。日常扩展（自定义网格/后处理/插件式调试）几乎都落在 RenderCore/Renderer 层。

**④ 资产管线三件套贯穿编辑器与运行时。** AssetRegistry（元数据缓存 FAssetRegistryState：*"used internally by IAssetRegistry to represent the disk cache"*）让"不加载资产就能查询资产"；Interchange 统一导入框架以节点图为核心（UInterchangeBaseNodeContainer：*"a format used to feed factories and writers when they import, reimport, and export"*）；打包分发由 PakFile/IoStore/BuildPatchServices 完成。内容浏览器、Python 资产 API、按需流送都建在这三件套上。

### 1.2 API 形态：数据驱动的观察

对 49,168 条条目做整体统计，能看到文档清单本身看不出来的结构规律。**类名前缀分布**（11,933 个类）：

| 前缀 | 类数 | 占比 | 说明 |
|---|---|---|---|
| F（纯 C++） | 5,868 | 49% | 引擎一半的类不进反射系统——性能与基础设施层（容器/数学/渲染/物理内核） |
| U（UObject 系） | 4,037 | 33% | 反射层：资产、组件、子系统、函数库——可序列化/蓝图可见 |
| T（模板） | 985 | 8% | 泛型容器与智能指针（TArray/TObjectPtr…） |
| S（Slate 控件） | 540 | 4% | UI 控件层（Slate 两模块合计 391 类） |
| A（Actor） | 209 | 2% | 可放置物只占 2%——量化印证"行为往组件放、Actor 保持克制"的组合模型 |
| I（接口，另计） | 1,709 | 另计 | 接口不在前缀统计内而单列 Interfaces 节：Runtime 1001/Editor 408/Developer 300——模块解耦靠接口而非继承 |

- 219/494 个模块带独立 Functions 节——"BlueprintFunctionLibrary 式函数库"是引擎暴露功能给蓝图的标准形态
- Editor 组 139 个模块平均条目少但面宽（每资产一个编辑器模块），Runtime 组 246 个模块条目高度集中在头部（Engine/Core/CoreUObject/Chaos 四个占全引擎 40%）
- 命名前缀本身就是文档导航：找"能放置的东西"搜 A，找"可蓝图化的对象"搜 U，找"UI"搜 S，找"扩展点"进 Interfaces 节

#### 1.2.1 角色分类学：后缀即职能

类名后缀是第二层索引（统计口径：11,933 个类）：

| 后缀/角色 | 类数 | 职能与用法 |
|---|---|---|
| *Component（组件） | 199 | 挂在 Actor 上的功能单元（USpringArmComponent/UAIPerceptionComponent…）。组件数是模块"玩法可用性"的直观指标。 |
| *Settings（设置） | 197 | 配置对象（UDeveloperSettings 派生）。一个模块带 Settings 类=它有项目设置面板入口。 |
| *Proxy（代理） | 121 | 两种语义要区分：U*Proxy 多为蓝图异步节点的工作对象（如 UAIAsyncTaskBlueprintProxy）；F*SceneProxy/F*RenderProxy 是渲染线程的镜像数据（游戏线程不可直接碰的渲染态）。同名后缀不同世界。 |
| *Library（函数库） | 102 | 静态函数集合（BlueprintFunctionLibrary 形态），Runtime 组占 86 个——引擎把能力"倒"进蓝图的标准容器，也是查"这功能蓝图怎么调"的最快入口。 |
| *Subsystem（子系统） | 85 | 按生命周期自动管理的服务（见上文专节）。 |
| *Instance（实例） | 41 | 运行期单例/实例包装（UGameInstance 之外的零散模式）。 |
| *DataAsset（数据资产） | 4 | 纯数据资产类（多数数据资产类不带此后缀，用 UPrimaryDataAsset 系，此处仅统计字面后缀）。 |

#### 1.2.2 Subsystem：按生命周期自动管理的服务（85 个）

Subsystem（子系统）是 5.x 时代替代"单例 Manager"的标准服务模式。引擎里的定义方式完全一致——官方 Remarks 用同一句话式：*"Base class for auto instanced and initialized systems that share the lifetime of the X"*（自动实例化与初始化、与 X 共享生命周期的系统基类），X 分别是 Engine / GameInstance / World / Local Player / Editor。也就是说：**子系统=按生命周期自动管理的全局服务**，你只管实现类，引擎按作用域自动创建销毁，蓝图/Python/编辑器处处可直接取用（BP 的 Get Subsystem 节点、Python 的 unreal.get_engine_subsystem() 系）。

| 家族 | 生命周期 | 适用场景 |
|---|---|---|
| **EngineSubsystem** | 进程级 | 随引擎/程序进程存续。适合与具体游戏无关的服务（如 Quartz 音频时钟 UQuartzSubsystem、资产注册表类服务）。 |
| **GameInstanceSubsystem** | 游戏实例级 | 跨关卡存续、随游戏实例销毁。放"整局游戏"的状态与服务（网络会话管理、MOD 加载器）。 |
| **WorldSubsystem** | 世界级 | 随每个 UWorld 创建销毁。放场景逻辑服务（导航、Mass 的实体管理器宿主 UMassEntitySubsystem 即此类）。 |
| **LocalPlayerSubsystem** | 本地玩家级 | 每本地玩家一个实例（分屏/多视口各一份）。放按玩家的输入/相机/UI 服务。 |
| **EditorSubsystem** | 编辑器级 | 仅编辑器进程。脚本期暴露面（UUnrealEditorSubsystem "Subsystem for exposing editor functionality to scripts"、ULevelEditorSubsystem、UStaticMeshEditorSubsystem 等成套出现）。 |

数据面：全引擎 494 模块共 85 个 Subsystem 类（Editor 家族 13、Engine 家族 8、World 4、GameInstance 2、LocalPlayer 2，其余为派生/变体）；分布最集中的宿主是 Engine（28 个，含全部基类）与 UnrealEd（14 个）。

- `UEngineSubsystem`（Engine）：*"Base class for auto instanced and initialized systems that share the lifetime of the Engine"*——与引擎同生命周期的子系统基类
- `UEditorSubsystem`（EditorSubsystem）：*"Base class for auto instanced and initialized systems that share the lifetime of the Editor"*——与编辑器同生命周期——同一句式定义，换个作用域就是新家族
- `ULevelEditorSubsystem`（LevelEditor）：*"Subsystem for exposing Level Editor related functionality to scripts"*——"把编辑器功能暴露给脚本"是编辑器子系统的典型用途

**怎么用**：把项目里的 Manager 类改造成子系统：自动生命周期+蓝图/Python 原生可达，告别手写单例；按作用域选型：跨关卡状态用 GameInstance 系、场景服务用 World 系、编辑器工具用 Editor 系；发现可复用服务：在模块页搜 "Subsystem" 后缀即可枚举该领域的官方服务面

#### 1.2.3 Top 模块解剖：反射密度谱

把每个模块的类按 U/A（反射可见）、F（纯 C++）、S（Slate）统计占比，得到一条**反射密度谱**：它实际度量的是"这个模块离设计师多近、离硬件多近"。写代码选落点时可以用它判断：想在 Engine/AIModule/MovieScene 这类高反射模块扩展，蓝图与编辑器会自然受益；想在 Chaos/RHI 这类 0% 模块扩展，就是在写引擎内核，必须考虑线程、性能与上层包装。

| 模块 | 类数 | 反射类(U/A)% | F 类% | S 类% | 解读 |
|---|---|---|---|---|---|
| AIModule | 195 | 92% | 6% | 0% | 全引擎反射密度最高的大模块——AI 面完全向蓝图/编辑器开放 |
| MovieScene | 118 | 82% | 15% | 0% | 序列几乎全是 UObject：轨道/节都做成资产对象，天然可编辑 |
| MassEntity | 21 | 76% | 23% | 0% | ECS 内核却保持高反射——官方刻意让 Mass 可被蓝图观测与配置 |
| UMG | 203 | 69% | 27% | 2% | UI 的 UObject 包装层，正是为了蓝图可拼 |
| UnrealEd | 857 | 62% | 29% | 6% | 编辑器=UObject 世界 + 54 个 Slate 控件 + 29 个 Settings |
| Engine | 2,456 | 55% | 41% | 0% | 玩法主体：131 个 Actor + 101 个组件 + 49 个 Proxy，反射与性能并存 |
| AudioMixer | 28 | 28% | 71% | 0% | 混音核心以 F 为主，U 类只留服务面（Quartz/Bus 子系统） |
| CoreUObject | 392 | 17% | 70% | 0% | 反射系统本身大多是 F 实现——"制造反射的机器不需要反射" |
| NetCore | 47 | 6% | 78% | 0% | 复制管线纯 C++，U 类只留驱动与连接面 |
| SlateCore | 140 | 5% | 70% | 10% | UI 框架本体非反射（性能），控件树由 S 构成 |
| GeometryCore | 232 | 0% | 47% | 0% | 几何算法库零反射——纯数据与函数（其余为 T 模板） |
| Chaos / RenderCore / RHI / Core | 1,978 | 0% | 80% | 0% | 物理内核/渲染公共层/RHI/基础库全部 0% 反射、F 类占 62~95%（表中为四模块均值）——离硬件越近反射越零；性能敏感内核通过上层模块（ChaosSolverEngine、Renderer）包出 UObject 面 |

#### 1.2.4 条目类型分布：数据重的模块与行为重的模块

模块页不止 Classes 一张表——Structs（全引擎 10,671 条）、Enums（3,778）、Interfaces（1,709）与 Classes 之间的比例本身就是模块性格的诊断指标。**结构体/类比值**高的模块是"数据编排系统"（状态与描述符多、行为对象少），比值低的模块是"行为系统"（大量活跃对象）。

| 模块 | Structs | Classes | 比值 | 模块性格 |
|---|---|---|---|---|
| MovieScene | 656 | 118 | 5.6 | 序列=数据编排：轨道求值靠海量求值模板/通道结构体驱动，行为类极少 |
| TypedElementFramework | 185 | 55 | 3.4 | 行/列/元数据模型——数据表式设计 |
| IrisCore | 228 | 116 | 2.0 | 新复制系统以"状态描述符"数据为核心（对照 NetCore 的行为型设计，两代架构风格差一目了然） |
| RHI | 214 | 124 | 1.7 | 资源/管线状态描述符密集 |
| Core | 1,070 | 927 | 1.2 | 容器与数学本就是数据结构 |
| Chaos | 320 | 644 | 0.5 | 行为系统：大量解算器/粒子对象 |
| UnrealEd | 270 | 857 | 0.3 | 编辑器以工具对象为主 |

**接口密度**（接口数相对类数）则标出"扩展点优先"的模块——它们以少量实现+大量接口邀请你注入自己的逻辑：TraceServices（61 接口 / 19 类，Insights 的分析提供者全是接口）、DatasmithCore（59/21）、SequencerCore（47/60）、PropertyEditor（45/43，属性编辑全靠接口注入）、InteractiveToolsFramework（44/196，工具/目标皆接口）、AudioExtensions（41/23）、DerivedDataCache（34/40）。给这些模块写扩展时，先翻 Interfaces 节而不是 Classes 节。

#### 1.2.5 文档自身的覆盖质量（元分析）

这套数据还能反过来度量**官方文档本身**：每条 Classes/Structs/Functions 条目在模块页上是否带 Remarks 说明文字。全引擎口径：

- **Classes Remarks：6,303 / 11,933 = 52%**——全引擎一半的类在文档页上没有说明文字
- **Structs Remarks：5,519 / 10,671 = 51%**——结构体同样约一半无说明
- **Functions Remarks：14,083 / 14,631 = 96%**——函数级几乎全覆盖——UE 的 Doxygen 习惯是函数注释勤、类注释懒
- **插件描述：850 / 893 = 95%**——.uplugin 的 Description 字段覆盖极好（43 个为空，如 IKRig/MotionWarping）

分域看更有指导意义（按类 Remarks 覆盖率排序，由生成器实时计算）：媒体播放/Mass/新兴技术等**新模块域覆盖率最高（73~78%）**——新代码带着文档习惯入场；而 **AI 与导航（32%）、输入与 XR（34%）、地形与植被（39%）、游戏框架（46%）这些最常用的域反而覆盖最低**——Engine/AIModule 的海量内部类常年没写类注释，使用这些域时要更多依赖源码与社区资料，不能只看 API 页。Best/Worst 模块同样两极：Horde 97%、DerivedDataCache 95%、SourceControl 93%（基建模块文档最勤）vs AudioEditor 3%、AnimationDataController 3%、MassEntityTestSuite 3%（编辑器与测试模块最懒）。

| 功能域 | Classes Remarks 覆盖 | 功能域 | Classes Remarks 覆盖 |
|---|---|---|---|
| 媒体播放 | 78% (32/41) | Sequencer 与影视虚拟制片 | 62% (227/364) |
| Mass 实体系统 | 78% (29/37) | 渲染与图形 | 52% (295/563) |
| 新兴与实验技术 | 77% (172/222) | 资产与内容管线 | 51% (79/153) |
| 动画与布料 | 73% (63/86) | 物理与碰撞 | 48% (395/810) |
| 核心与运行时基础 | 70% (1,089/1,541) | 游戏框架与玩法 | 46% (1,174/2,525) |
| 网络与在线服务 | 70% (195/275) | 地形与植被 | 39% (43/109) |
| 几何与建模 | 69% (427/615) | 输入与 XR 设备 | 34% (30/86) |
| 遥测与性能分析 | 68% (17/25) | AI 与导航 | 32% (88/268) |
| 音频 | 66% (152/228) | 自动化测试 | 0% (0/4) |
| UI 界面 | 64% (406/627) | | |

实操建议：① 高覆盖域（网络/几何/遥测）可直接按 API 页 Remarks 理解模块；② 低覆盖域把 API 页当"索引"用——类名/继承链/函数签名可靠，说明文字缺失时转源码头文件与官方论坛；③ 函数级 96% 覆盖意味着**查"这个函数干什么"几乎总是有答案的**，查"这个类是什么"则一半要靠别处。

### 1.3 十九个功能域逐域分析

> 域划分为本文归纳（官方无此维度）；每域给出机制 → 代表 API（官方引文）→ 能做什么。模块数 (R/E/D) 标注构建组分布。

#### 核心与运行时基础（27 个模块，R/E/D=27/0/0）

**机制**：一切 API 的地基。Core 提供容器（TArray/TMap/TSet）、字符串（FString/ FName）、智能指针、线程与任务图（TaskGraph/Async）、数学库——它是 API 条目数第二大的模块（6,277 条，其中 Functions 2,935 条）。CoreUObject 在其上建立 UObject 反射体系：类的属性/函数在运行时可见，这是编辑器属性面板、序列化、网络复制、蓝图暴露的共同前提。Json/XmlParser/Cbor 提供数据交换，uLang 系列是 Verse 语言的运行时核心。

**代表 API（官方 Remarks 原文）**：

- `UObject`（CoreUObject）：*"The base class of all UE objects."*——所有 UE 对象的基类
- `UFunction`（CoreUObject）：*"Reflection data for a replicated or Kismet callable function."*——反射数据：描述一个可复制或蓝图（Kismet）可调用的函数——一句话点明"反射=复制+蓝图"两大消费方
- `FSoftObjectPath`（CoreUObject）：*"A struct that contains a string reference to an object, either a package, a top level asset or a subobject."*——软引用：以字符串引用资产/子对象，是异步加载与流送的基础
- `FObjectInitializer`（CoreUObject）：*"Internal class to finalize UObject creation (initialize properties) after the real C++ constructor is called."*——对象初始化器：C++ 构造之后的属性终态化

**能做什么**：自定义序列化格式 / 存档结构（配合 SaveGame 插件的存档体系）；软引用 + AssetManager 做按需异步加载与流送；利用反射写通用编辑器工具（自动生成 UI、批量属性修改）；在 Shipping 里裁剪 Developer/Editor 代码时的分层依赖设计。

#### 游戏框架与玩法（13 个模块，R/E/D=13/0/0）

**机制**：Engine 是全引擎最大的模块（8,796 条 API），定义了 Actor-Component 组合模型：Actor 是可放置/生成的对象，组件提供可复用行为；SceneComponent 增加 Transform 与挂接，PrimitiveComponent 再增加可渲染/可碰撞几何。游戏规则由 GameMode 在服务器端定义，玩家通过 PlayerController 占有 Pawn；Character 自带网格、碰撞与内置移动逻辑（CharacterMovementComponent）。GameInstance 则是跨越关卡切换的进程级管理器。UGameplayStatics/UKismetSystemLibrary 是这套能力暴露给蓝图的静态函数桥。

**代表 API（官方 Remarks 原文）**：

- `AActor`（Engine）：*"Actor is the base class for an Object that can be placed or spawned in a level."*——可放置或生成到关卡中的对象的基类
- `AGameModeBase`（Engine）：*"The GameModeBase defines the game being played."*——GameMode 定义"玩的是什么游戏"——比赛规则、重生、胜利条件的家
- `APawn`（Engine）：*"Pawn is the base class of all actors that can be possessed by players or AI."*——可被玩家或 AI 占有的 Actor 基类
- `ACharacter`（Engine）：*"Characters are Pawns that have a mesh, collision, and built-in movement logic."*——自带网格+碰撞+内置移动逻辑的 Pawn
- `UActorComponent`（Engine）：*"ActorComponent is the base class for components that define reusable behavior that can be added to different types of Actors…"*——可复用行为的组件基类——UE 组合优于继承的落点
- `UPrimitiveComponent`（Engine）：*"PrimitiveComponents are SceneComponents that contain or generate some sort of geometry, generally to be rendered or used as collision…"*——携带/生成几何（渲染或碰撞用途）的组件层
- `UGameInstance`（Engine）：*"GameInstance: high-level manager object for an instance of the running game."*——进程级高阶管理器：跨关卡存续
- `ULevelStreaming`（Engine）：*"Abstract base class of container object encapsulating data required for streaming…"*——关卡流送容器：大世界按需加载的抽象
- `UCharacterMovementComponent`（Engine）：*"CharacterMovementComponent handles movement logic for the associated Character owner."*——角色移动逻辑宿主——行走/跳跃/飞行/游泳模式与网络同步都在此

**能做什么**：用组件组合设计任何玩法对象（而不必继承庞大 Actor 子类）；自定义 GameMode/GameState 规则与观战/重生逻辑；定制 CharacterMovementComponent 做特殊移动模式；关卡流送（ULevelStreaming）与世界分区大世界；GameplayTags/GameplayTasks 作为轻量玩法基建（标签驱动状态机、异步任务）。

#### 输入与 XR 设备（7 个模块，R/E/D=7/0/0）

**机制**：InputCore 定义按键/手势/轴的抽象数据；InputDevice 是设备接入接口层；HeadMountedDisplay 模块定义 XR 头显与追踪系统的公共接口（IHeadMountedDisplay/IXRTrackingSystem），OpenXR/各厂商插件在其上实现；EyeTracker/Voice 提供眼动与语音通道。运行时的按键映射推荐走 EnhancedInput 插件（上下文映射）。

**代表 API（官方 Remarks 原文）**：

- `IHeadMountedDisplay`（HeadMountedDisplay）：*"HMD device interface"*——头显设备接口
- `IXRTrackingSystem`（HeadMountedDisplay）：*"Main access point to an XR tracking system. Use it to enumerate devices and query their poses."*——XR 追踪系统主入口：枚举设备、查询位姿

**能做什么**：为特殊硬件（踏板/方向盘/航班摇杆）写输入设备插件（RawInput 插件即此类）；XR 应用：手柄位姿、注视交互、空间锚（ARPin 走 BP AR 分类）；语音命令与辅助功能（Text to Speech 插件）。

#### 渲染与图形（20 个模块，R/E/D=20/0/0）

**机制**：三层栈：RHI 是跨图形 API 的硬件抽象（FRHICommandList 命令缓冲、FRHITexture 等资源接口；FDynamicRHI 为动态绑定入口），D3D12RHI/VulkanRHI/OpenGLDrv 是各平台后端；RenderCore 提供公共层（顶点工厂 FVertexFactory 把顶点数据源链接进顶点着色器、GPU 场景、着色器绑定）；Renderer 实现场景渲染器（延迟着色管线、网格绘制命令 FMeshDrawCommand 的缓存与逐帧构建）。要做渲染扩展，通常从 RenderCore/Renderer 的扩展点（顶点工厂、Mesh Processor、自定义 Pass）入手而不是直接写 RHI。

**代表 API（官方 Remarks 原文）**：

- `FDynamicRHI`（RHI）：*"The interface which is implemented by the dynamically bound RHI."*——动态绑定 RHI 的接口——启动时选定的图形后端入口
- `FVertexFactory`（RenderCore）：*"Encapsulates a vertex data source which can be linked into a vertex shader."*——封装可链接进顶点着色器的顶点数据源——自定义网格渲染的标准扩展点
- `FCachedMeshDrawCommandInfo`（Renderer）：*"Stores information about a mesh draw command which is cached in the scene."*——场景中缓存的网格绘制命令——UE 渲染器"命令缓存复用"设计的体现
- `FGraphicsMinimalPipelineStateInitializer`（Renderer）：*"Pipeline state without render target state. Useful for mesh passes where the render target state is not changing between draws."*——无渲染目标态的管线状态——网格 Pass 间渲染目标不变时的快速比较优化

**能做什么**：自定义顶点工厂+材质绘制特殊几何（如 Niagara 的各 VertexFactories 插件做法）；渲染器扩展：后处理材质、自定义 Screen Pass（引擎源码级）；平台适配：新 GPU API/新硬件的 RHI 后端（专业团队）；图形调试：RenderDocPlugin/PixWinPlugin/DumpGPUServices 插件直接可用；色彩管理 OpenColorIO、上采样/帧生成（DLSS/FSR 插件分类）。

#### 物理与碰撞（13 个模块，R/E/D=13/0/0）

**机制**：5.x 物理统一到 Chaos：Chaos 模块是解算器内核（宽相 FBasicBroadPhase 按 AABB 筛粒子对、求解器全步骤容器 FAllSolverTasks、CCD 修正 FCCDModifier），ChaosSolverEngine 把解算器包装成场景对象（UChaosSolver），PhysicsCore 提供碰撞通道/Profile/BodySetup 等抽象。破坏系统=几何集合（FGeometryCollection，可破碎的分层网格数据）+ FieldSystemEngine 力场（UFieldSystemComponent 在空间中施加断裂/力场）。ChaosVD 录制回放用于物理调试；载具走 ChaosVehicles。

**代表 API（官方 Remarks 原文）**：

- `FBasicBroadPhase`（Chaos）：*"Run through a list of particle pairs and pass them onto the collision detector if their AABBs overlap."*——宽相：遍历粒子对，AABB 重叠者送碰撞检测——物理管线第一步
- `FAllSolverTasks`（Chaos）：*"Container for all steps required to fully update a solver."*——解算器完整更新的全步骤容器
- `FCCDModifier`（Chaos）：*"Allows the user to modify the results of CCD collision detection prior to the CCD rewind being applied."*——CCD（连续碰撞检测）回卷前的结果修正点
- `UChaosSolver`（ChaosSolverEngine）：*"UChaosSolver ( UObject )"*——场景级解算器对象

**能做什么**：刚体破坏玩法（几何集合 + 力场组件 + 破碎触发，FractureEditor/PlanarCut 插件做预破碎）；载具（ChaosVehicles）与布料（ChaosCloth 系列插件）；物理控制动画（PhysicsControl 插件对静态/骨骼网格做物理驱动）；碰撞查询（Blueprint 的 Trace/Overlap 全家桶即其暴露面）；物理回放调试（Chaos Visual Debugger）。

#### 几何与建模（14 个模块，R/E/D=14/0/0）

**机制**：MeshDescription 是引擎统一的网格数据结构（静态/骨骼网格资产内部即用它存储），GeometryCore 提供几何算法库（661 个函数），GeometryFramework/CADKernel 支撑 CAD 数据，Dataflow 系列提供节点图式几何处理资产（布料/破坏资产编辑都建在其上）。InteractiveToolsFramework 定义编辑器交互工具的标准基类（选中/接受/取消的生命周期）——编辑器"建模模式"整套工具就是它的大规模应用。

**代表 API（官方 Remarks 原文）**：

- `FAttributesSetBase`（MeshDescription）：*"This is the container for all attributes and their arrays."*——网格属性容器：顶点/三角的任意属性数组的统一存储——"属性化网格"设计的核心
- `AGizmoActor`（InteractiveToolsFramework）：*"is a base class for Actors that would be created to represent Gizmos in the scene."*——场景中呈现 Gizmo 的 Actor 基类——交互工具的视口可视化层
- `FActivateToolChange`（InteractiveToolsFramework）：*"is used by UInteractiveToolManager to change the active tool."*——工具管理器切换活动工具的事务封装——支持 Undo/Redo 的工具切换

**能做什么**：程序化网格生成与编辑（GeometryScripting 插件把整套几何函数暴露给蓝图）；自定义编辑器建模工具（挂进 ModelingToolsEditorMode 的工具模式）；Dataflow 节点式几何资产（布料资产、破坏资产的数据流编辑）；CAD/工业数据导入管线（CADKernel + DatasmithCADImporter）。

#### UI 界面（11 个模块，R/E/D=11/0/0）

**机制**：两层 UI：Slate/SlateCore 是保留模式 UI 框架（声明式 SlateBuilder 语法、合成/布局/绘制全自研，编辑器全部界面皆 Slate，也能做游戏 UI）；UMG 在 Slate 外包一层 UObject（UWidget 系列）使其可蓝图化、可序列化为 WidgetBlueprint 资产，UUserWidget 是"用蓝图拼 UI"的载体。WebBrowser/CEF3Utils 提供内嵌浏览器控件；渲染走 SlateRHIRenderer。跨平台手柄导航用 CommonUI 插件。

**代表 API（官方 Remarks 原文）**：

- `SWindow`（SlateCore）：*"SWindow is a platform-agnostic representation of a top-level window."*——平台无关的顶层窗口表示——独立工具窗口的容器
- `SButton`（Slate）：*"Slate's Buttons are clickable Widgets that can contain arbitrary widgets as its Content()."*——按钮可容纳任意控件作为内容——组合式 UI 的体现
- `SListView`（Slate）：*"A ListView widget observes an array of data items and creates visual representations of these items."*——列表视图：观察数据数组并生成可视化项（MVVM 式）
- `UUserWidget`（UMG）：*"A widget that enables UI extensibility through WidgetBlueprint."*——通过 WidgetBlueprint 实现 UI 扩展——蓝图 UI 的载体
- `UWidget`（UMG）：*"This is the base class for all wrapped Slate controls that are exposed to UObjects."*——所有被 UObject 包装的 Slate 控件的基类——两层 UI 的粘合层
- `FOnNavigationTransition`（UMG）：*"If Entered, Other Widget is the Widget Navigated From. If Exited, Other Widget is the Widget Navigated To"*——导航转移事件：手柄焦点在控件间迁移的钩子
- `FUMGDragDropOp`（UMG）：*"This is the drag/drop class used for UMG, all UMG drag drop operations utilize this operation."*——UMG 拖拽操作统一载体

**能做什么**：游戏 HUD/菜单/背包（UMG + 控件动画）；编辑器工具窗口与属性面板（纯 Slate，配合 EditorWidgets/GraphEditor 做图编辑器 UI）；主机/手柄 UI 导航与样式系统（CommonUI 插件，游戏无关的可复用控件库）；内嵌网页（登录/商城/ wiki 面板，CEF 内核）；UMG 预览与调试（UMGWidgetPreview 插件免 PIE 预览）。

#### 动画与布料（9 个模块，R/E/D=9/0/0）

**机制**：AnimationCore 是动画数据结构（姿势/曲线/骨骼）基础层，AnimGraphRuntime 是动画蓝图运行时（状态机/混合空间/各种节点的求值实现，并以 *Library 类把节点上下文操作暴露成函数）。外部数据经 LiveLink 三件套流入（动捕服、面部捕捉、DCC 软件桥）；布料已归 Chaos 体系（ClothingSystemRuntime* 接口层 + ChaosCloth 插件实现）；MRMesh 承载面部混合现实网格。高端链路：ControlRig（程序化绑定动画）、IK Rig（重定向）、MLDeformer（机器学习形变压缩）。

**代表 API（官方 Remarks 原文）**：

- `UAnimationStateMachineLibrary`（AnimGraphRuntime）：*"Exposes operations to be performed on anim state machine node contexts."*——暴露状态机节点上下文操作——动画蓝图的程序化接口
- `UBlendSpaceLibrary`（AnimGraphRuntime）：*"Exposes operations to be performed on a blend space anim node."*——混合空间节点操作库

**能做什么**：动画蓝图/状态机/混合空间的深度定制（通知窗口、自定义节点求值）；Live Link 动捕直播到引擎（角色/相机/灯光均可作为源）；Control Rig 程序化动画与绑定（绑定资产在运行时求值）；IK Rig + 重定向把动画跨骨架复用（IKRetarget 插件）；ML 形变器把高质量模拟"烘焙"成轻量推理（MLDeformer/NearestNeighbor）。

#### Sequencer 与影视虚拟制片（12 个模块，R/E/D=12/0/0）

**机制**：MovieScene 定义序列资产本体（UMovieScene + UMovieSceneSequence 抽象 + Section 轨道分节），LevelSequence 把序列落到关卡 Actor 上、ULevelSequencePlayer 负责运行时播放；TimeManagement 提供帧率/时间码标准。影片输出与摄制工作流由插件完成：Take Recorder（表演采集）、Movie Render Queue（离线高质量渲染）、AVEncoder/AVIWriter（编码）、nDisplay/VCam/Composure（虚拟摄制与合成）、StageDataCore（舞台数据）。BP 的 Camera/Cinematics 分类是这套能力的节点面。

**代表 API（官方 Remarks 原文）**：

- `UMovieScene`（MovieScene）：*"Implements a movie scene asset."*——影片场景资产实现
- `UMovieSceneSequence`（MovieScene）：*"Abstract base class for movie scene animations (C++ version)."*——序列抽象基类——一切"可播放时间线"的父类
- `ULevelSequence`（LevelSequence）：*"Movie scene animation for Actors."*——针对关卡 Actor 的序列动画
- `ULevelSequencePlayer`（LevelSequence）：*"is used to actually "play" a level sequence asset at runtime."*——运行时真正"播放"关卡序列的播放器
- `FInterrogationChannels`（MovieSceneTracks）：*"A class specialized for interrogating Sequencer entity data without applying any state to objects."*——"审讯"通道：不施加状态地读取序列实体数据——烘焙/导出序列的标准姿势

**能做什么**：过场动画与游戏内事件时间线（导演式控制任意 Actor 属性）；技能/交互的时序编排（序列驱动粒子/相机/音效）；虚拟摄制全流程：nDisplay 多屏、VCam 虚拟相机、Composure 实时合成、ICVFX 摄制内视效；自动化出片：Movie Render Queue 批量高质量渲染 + Take Recorder 采集。

#### 音频（18 个模块，R/E/D=18/0/0）

**机制**：AudioMixer 是混音器主框架（设备管理、总线 FMixerAudioBus、源管理），SignalProcessing 是 DSP 基础库，AudioLink 让外部混音器（Wwise 等）接管；音乐系统 Quartz 提供采样级精确的量化时钟（FQuantizedOtherClockStart 等）；分析与采集走 AudioAnalyzer/AudioCapture。上层内容体系在插件里：MetaSound（DSP 图式声音资产，官方描述"让声音设计师完全掌控声音源的 DSP 图生成"）、AudioModulation（参数调制）、SoundFields/ResonanceAudio（空间化）。编解码器（Opus/Vorbis/Bink/ADPCM/Rad）按平台接入。

**代表 API（官方 Remarks 原文）**：

- `FMixerAudioBus`（AudioMixer）：*"Bus instance data. Holds source id bus instances and bus sends data."*——总线实例数据：源与发送关系的运行时载体
- `FQuantizedOtherClockStart`（AudioMixer）：*"starts a second clock on a sample-accurate boundary"*——在采样级精确边界启动第二个时钟——Quartz 程序化音乐的精度基础
- `FOnSynthEnvelopeValue`（AudioMixer）：*"Called by a synth component and returns the sound's envelope value (using an envelope follower in the audio renderer)."*——包络跟随器回调：音频驱动的视觉反馈（如 UI 随音起舞）的数据源

**能做什么**：MetaSound 搭建可参数化的程序化音源（替代 SoundCue 的下一代）；Quartz 做节拍同步玩法（音游、随节拍生成敌人）；Submix/效果链处理与录音输出；对话与本地化配音管理；空间化与混响（Resonance Audio 房间声学）。

#### AI 与导航（3 个模块，R/E/D=3/0/0）

**机制**：AIModule 提供 AI 三件套：AAIController 驱动 AI Pawn（大脑组件 BrainComponent 挂行为树/HTN），UAIPerceptionComponent 注册为感知系统的监听者收集刺激，UBTTaskNode 等构成行为树节点体系（Task 是"执行动作的叶子节点"）。导航侧 NavigationSystem 管理导航数据（ANavigationData 抽象出 NavMesh/NavGraph），Navmesh 模块是 Recast 生成器，ANavModifierVolume 可用体积动态改 NavMesh 区域属性。环境查询 EQS、人群 MassCrowd、机器学习 LearningAgents 都挂在这套地基上。

**代表 API（官方 Remarks 原文）**：

- `AAIController`（AIModule）：*"AIController is the base class of controllers for AI-controlled Pawns."*——AI 控制 Pawn 的控制器基类
- `UAIPerceptionComponent`（AIModule）：*"is used to register as stimuli listener in AIPerceptionSystem and gathers registered stimuli…"*——注册为感知系统监听者并收集刺激（视觉/听觉/伤害感知的接收端）
- `UBTTaskNode`（AIModule）：*"Task are leaf nodes of behavior tree, which perform actual actions"*——行为树叶子节点：执行实际动作
- `ANavigationData`（NavigationSystem）：*"Represents abstract Navigation Data (sub-classed as NavMesh, NavGraph, etc). Used as a common interface for all navigation types…"*——导航数据抽象：NavMesh/NavGraph 的公共接口
- `ANavModifierVolume`（NavigationSystem）：*"Allows applying selected AreaClass to navmesh, using the shape of the Volume"*——用体积形状给 NavMesh 施加区域属性（动态成本/禁区）

**能做什么**：行为树 AI（巡逻/追击/逃跑的经典栈：BT + 黑板 + EQS 选点）；感知型 AI（视觉锥/听觉半径触发行为切换）；动态导航（破坏桥后重生成 NavMesh、用 NavModifier 改通行成本）；大规模人群（MassCrowd 样条人群 + 避障）；强化学习角色控制（LearningAgents 训练后运行时推理）。

#### 网络与在线服务（41 个模块，R/E/D=41/0/0）

**机制**：复制栈：NetCore 管理 NetDriver/连接（FConnectionHandle 每 NetDriver 唯一），对象引用跨机器以 NetGUID 复制（FGuidReferences 的官方说明直接点明原因："字面内存指针在不同机器上不同"），PacketHandler 做包处理链，IrisCore 是 5.x 在研的新一代复制系统（按状态描述符序列化，更细粒度的脏跟踪）。通信设施：Sockets/HTTP/HttpServer/WebSockets/Stomp/XMPP，Messaging 系是引擎内部消息总线。回放系统 NetworkReplayStreaming 有五种后端实现（本地文件/内存/HTTP/存档/空）。在线服务走 OnlineServices 体系（EOS 等插件）。

**代表 API（官方 Remarks 原文）**：

- `FGuidReferences`（NetCore）：*"References to Objects (including Actors, Components, etc.) are replicated as NetGUIDs, since the literal memory pointers will be different across machines."*——对象引用复制为 NetGUID——因为裸指针在每台机器上都不同
- `FConnectionHandle`（NetCore）：*"The handle is unique per netdriver."*——每 NetDriver 唯一的连接句柄
- `FHttpModule`（HTTP）：*"Use FHttpFactory to create a new Http request"*——HTTP 请求工厂入口
- `IHttpResponse`（HTTP）：*"Interface for Http responses that come back after starting an Http request"*——HTTP 响应接口
- `ISocketSubsystem`（Sockets）：*"This is the base interface to abstract platform specific sockets API differences."*——套接字子系统基接口：抹平平台 Socket API 差异
- `FInternetAddr`（Sockets）：*"Represents an internet address. All data is in network byte order"*——网络字节序的地址表示
- `IMessageBridge`（Messaging）：*"Interface for message bridges."*——消息桥接口：进程间/网络消息总线的接驳点

**能做什么**：多人游戏：属性复制（DOREPLIFETIME 宏）+ RPC + 相关性（每帧只发玩家附近的）；专用服务器与回放（DemoNetDriver + 流后端选择）；对接账号/好友/成就/匹配（OnlineServices + EOS/Steam/谷歌插件）；游戏内 Web 面板（HttpServer + WebSockets 推送，Pixel Streaming 远程操控同源）；DDoS 检测与限流（FDDoSDetection 直接可用）。

#### 媒体播放（4 个模块，R/E/D=4/0/0）

**机制**：Media/MediaAssets/MediaUtils 构成媒体框架三件套：UMediaPlayer 是播放器资产，视频轨渲染到 UMediaTexture，音频走 UMediaSoundComponent，ImageDownload 支撑运行时图片拉取。具体解码/协议由插件提供：ElectraPlayer（跨平台流媒体主力）、AvfMedia/WebMMedia/WindowsMoviePlayer（平台原生）、ImgMedia（EXR 序列，虚拟摄制视频墙主力）、AjaMedia（采集卡 I/O）。

**代表 API（官方 Remarks 原文）**：

- `UMediaPlayer`（MediaAssets）：*"Implements a media player asset that can play movies and other media sources."*——媒体播放器资产
- `UMediaTexture`（MediaAssets）：*"Implements a texture asset for rendering video tracks from UMediaPlayer assets."*——把视频轨渲染成纹理——视频贴到任意材质的通道
- `UMediaSoundComponent`（MediaAssets）：*"Implements a sound component for playing a media player's audio output."*——播放媒体音频输出的组件

**能做什么**：游戏内视频屏幕（监控器/电视机/巨幕，MediaTexture 贴材质）；虚拟摄制 LED 墙内容播放（ImgMedia EXR 序列 + nDisplay 同步）；过场视频与开场动画（平台原生解码器保证兼容）；直播流/网络视频接入（Electra 支持 HLS/DASH 流）。

#### 地形与植被（2 个模块，R/E/D=2/0/0）

**机制**：Landscape 是高度场地形系统：组件化分块、多层材质混合、支持编辑层（FEditLayerRenderItem 描述每层能渲染什么）、与 World Partition 深度联动（按地块流送）；Foliage 是实例化植被（一株资产刷 N 个实例，GPU 实例化渲染）。程序化生成可接 PCG 插件（图驱动散布）与 Landmass（地形侵蚀）。

**代表 API（官方 Remarks 原文）**：

- `FEditLayerRenderItem`（Landscape）：*"Each edit layer render item represents the capabilities of what a given edit layer can render in terms of landscape data…"*——编辑层渲染项：描述该编辑层能渲染的地形数据能力——非破坏性地形分层编辑的机制核心

**能做什么**：大世界地形（World Partition 分块流送 + HLOD）；多层非破坏编辑（每层可独立开关/回滚的雕塑与绘制）；植被/岩石散布（刷绘或 PCG 规则化散布 + 运行时节裁）；程序化地形（Landmass 侵蚀 + 水系 Water 插件联动雕刻河道）。

#### Mass 实体系统（5 个模块，R/E/D=5/0/0）

**机制**：Mass 是 UE 的 ECS 式框架：实体=纯 ID+分块存储的组件数据，Processor 在多线程上处理队列（FProcessorWorker/FChunkWorker 是其工作单元），UMassEntitySubsystem 作为世界子系统承载实体管理器。它与传统 Actor 世界通过 Spawner/Representation 处理器桥接（远处的车是 Mass 实体，近了才生成真 Actor）。配套：ZoneGraph（样条路网）、StateTree（行为）、MassCrowd/MassAI 插件。

**代表 API（官方 Remarks 原文）**：

- `UMassEntitySubsystem`（MassEntity）：*"The sole responsibility of this world subsystem class is to host the default instance of FMassEntityManager for a given UWorld."*——承载某 UWorld 默认 FMassEntityManager 的世界子系统
- `FProcessorWorker`（MassEntity）：*"A worker to execute queued processors"*——执行排队处理器的工作单元——多线程处理器的运行形态

**能做什么**：大规模人群/车流（万级实体占 CPU 小头）；环境生命模拟（鸟群、鱼群、战场背景单位）；LOD 化玩法代理（远处 ECS、近处真 Actor 的无缝切换）。

#### 资产与内容管线（20 个模块，R/E/D=20/0/0）

**机制**：AssetRegistry 是全项目资产的元数据库（磁盘缓存的 FAssetRegistryState），编辑器内容浏览器、加载校验、按标签/类检索都靠它，且暴露给蓝图/Python。Interchange 是新一代统一导入框架：导入物先转换为通用节点图（UInterchangeBaseNodeContainer），再经管线（UInterchangePipelineBase）喂给各格式工厂——FBX/glTF/USD/OBJ 都走这条路。打包侧：PakFile/IoStoreOnDemand 打包与按需分发，BuildPatchServices 做差分补丁，Zen 是 DDC/构建存储服务。Datasmith 是工业管线（CAD/Revit/SketchUp→引擎）的专用通道。

**代表 API（官方 Remarks 原文）**：

- `FAssetRegistryState`（AssetRegistry）：*"The state of an asset registry, this is used internally by IAssetRegistry to represent the disk cache…"*——资产注册表状态=磁盘缓存——资产查询的数据底座
- `UInterchangeBaseNodeContainer`（InterchangeCore）：*"The Interchange UInterchangeBaseNode graph is a format used to feed factories and writers when they import, reimport, and export"*——Interchange 节点图：导入/重导/导出时喂给工厂与写入器的统一格式
- `UInterchangePipelineBase`（InterchangeCore）：*"Pipeline implementation:"*——管线基类——自定义导入处理的挂点
- `IAssetRegistry`（AssetRegistry）：*"Global singleton interface for accessing a catalog of all packages (and some other content file types) that are stored in any mounted d[irectory]"*——资产注册表全局单例：访问任意挂载目录下全部包的目录清单——按需加载的查询面

**能做什么**：按类/标签/路径批量检索资产做工具（Python EditorAssetLibrary 的底层就是它）；自定义 Interchange 管线处理专有格式导入（重命名/LOD/碰撞预设自动化）；游戏运行时资产发现（不加载资产本体即可枚举：开放世界按区加载、Mod 发现）；补丁/按需分发（BuildPatchServices 差分 + IoStoreOnDemand 流送）。

#### 遥测与性能分析（17 个模块，R/E/D=17/0/0）

**机制**：TraceLog 是低开销埋点数据流（运行时常开），TraceServices/TraceAnalysis 是分析后端，TraceInsights 系即 Unreal Insights 前端（帧/网络/内存/资产加载多维分析）；Analytics* 是可插拔遥测后端（CSV/ET/日志/Swrve/Horde）；PerfCounters 暴露运行时计数器；RewindDebugger 是动画/属性回溯调试器的运行时接口。第三方 RenderDoc/PIX 插件负责 GPU 级抓帧。

**能做什么**：性能回归看板（Insights + Gauntlet 自动化性能测试出报告）；线上问题遥测（Analytics 后端自选落地）；多人同步分析（Concert Insights 让多客户端同起 Trace）；动画逐帧回溯（Rewind Debugger）。

#### 自动化测试（3 个模块，R/E/D=3/0/0）

**机制**：AutomationTest 框架（Runtime 侧）+ AutomationController/Driver/Window（Developer 侧驱动与窗口自动化）+ FunctionalTesting（关卡式功能测试 Actor）。打包后自动化跑 Gauntlet 插件（以测试控制器驱动整包游戏），性能自动化走 AutomatedPerfTesting。CQTest 提供断言库。

**能做什么**：单元/冒烟/功能三级测试金字塔接入 CI；截图比对回归（ScreenShotComparison）；整包自动化与性能基线（Gauntlet + 性能测试控制器）；UI 自动化（AutomationDriver 驱动 Slate 控件）。

#### 新兴与实验技术（6 个模块，R/E/D=6/0/0）

**机制**：五件套：VerseCompiler/uLang（UEFN 的 Verse 语言编译与运行时）、NNE 神经网络引擎（UNNEModelData 资产存模型，运行时由插件提供四种后端：ONNX Runtime、IREE、CoreML、RDG——即 CPU/GPU/苹果/渲染图四种推理路径）、VectorVM（Niagara GPU 仿真的向量虚拟机）、CUDA（NVIDIA 直连）、AutoRTFM（事务内存实验，让"回滚式"并行成为可能）。

**代表 API（官方 Remarks 原文）**：

- `UNNEModelData`（NNE）：*"This class represents assets that store neural network model data."*——存储神经网络模型数据的资产——引擎内跑 AI 推理的载体

**能做什么**：在引擎/游戏内跑 ML 模型（超分、动画混合、NPC 行为，配 NNERuntime 插件选后端）；Verse 脚本生态（UEFN 创作者生态的语言基础）；VectorVM 写数据并行脚本（Niagara Simulation Stage 的执行后端）。

### 1.4 Editor 组逐子域分析（139 个模块，8 个子域）

#### 编辑器框架与工作流（28 个模块）

**机制**：UnrealEd（857 类，Editor 组最大）承载编辑器引擎本体（UEditorEngine：*"Engine that drives the Editor"*）、事务（Undo/Redo 贯穿一切编辑操作）、选择集与 PIE；FAssetEditorToolkit（*"Base class for toolkits that are used for asset editing (abstract)"*）是所有资产编辑器窗口的容器基类；MainFrame/LevelEditor 拼装主界面，ToolMenus 提供统一菜单注册。

- `FAssetEditorToolkit`（UnrealEd）：*"Base class for toolkits that are used for asset editing (abstract)"*——资产编辑器工具包抽象基类

**能做什么**：写编辑器插件的标准路径：EditorSubsystem（全局服务）+ ToolMenus（菜单）+ 注册 Tab；自定义资产编辑器（Toolkit + Tab Spawner + 视口布局 FAssetEditorViewportLayout）；PIE 前后钩子做自动化（配合 Blutility）；事务感知的批量编辑（Scoper 保证可撤销）。

#### 内容浏览器与资产管理（17 个模块）

**机制**：UAssetDefinition（*"Asset Definitions represent top level assets that are known to the editor"*）是新一代资产类型注册面——图标/颜色/菜单/打开行为集中声明；内容浏览器的检索由 FAssetTextFilter（文本过滤）与 FFrontendFilter 系（如 FFrontendFilter_CheckedOut 只显示已检出资产）组成；WorldPartitionEditor 提供大世界分块管理 UI。

- `FFrontendFilter_CheckedOut`（ContentBrowser）：*"A filter that displays only checked out assets"*——前端过滤器示例：只显示已检出——版本感知的资产视图
- `UAssetDefinition`（AssetDefinition）：*"Asset Definitions represent top level assets that are known to the editor."*——资产定义：编辑器认识一种新资产的唯一注册点

**能做什么**：注册自定义资产类型（含缩略图/颜色/操作菜单全套）；内容浏览器自定义过滤器/列；集合（Collection）与标签的批量管理工具；World Partition 地块批量操作。

#### 蓝图与图编辑器（10 个模块）

**机制**：Kismet 系（FBlueprintEditor：*"Main Kismet asset editor"*）+ KismetCompiler 构成蓝图编辑与编译；GraphEditor 是公共图编辑底座，FConnectionDrawingPolicy（*"draws the connections for an UEdGraph composed of pins and nodes"*）这样的绘制策略类让连线样式可定制。材质图、动画蓝图、行为树、RigVM 图全部复用这套底座。

- `FBlueprintEditor`（Kismet）：*"Main Kismet asset editor"*——蓝图主编辑器
- `FConnectionDrawingPolicy`（GraphEditor）：*"This class draws the connections for an UEdGraph composed of pins and nodes."*——连线绘制策略：图可视化定制点（如动画蓝图的运动轨迹连线）

**能做什么**：自定义图节点（材质/动画蓝图/行为树节点的编辑器侧）；图搜索与 Diff 工具（FGraphDiffControl 做版本对比）；蓝图编译器扩展：静态分析/规范校验插件；给自研节点系统复用 GraphEditor 底座。

#### 资产编辑器（40 个模块）

**机制**：每类资产一个编辑器模块（材质 MaterialEditor、动画 Persona/SkeletalMeshEditor、网格 StaticMeshEditor、贴图 TextureEditor、UI UMGEditor、曲线 Curve*Editor、表 DataTable/CurveTable/StringTable Editor、序列 Sequencer、地形 LandscapeEditor……），全部基于 Toolkit + GraphEditor + PropertyEditor 组合搭建。这套"每种资产一个编辑器"的架构让编辑器可按需裁剪。

- `FCameraShakePreviewer`（MovieSceneTracks）：*"A class that owns a gameplay camera shake manager, so that we can use it to preview shakes in editor."*——编辑器内预览相机抖动——"编辑时所见即游戏所得"的细节体现

**能做什么**：定制各资产编辑器（工具栏、细节面板、预览场景 AdvancedPreviewScene）；批量资产处理入口（配合 AssetTools 的动作）；自动化打开/截图资产编辑器做管线校验。

#### 视口与交互模式（13 个模块）

**机制**：专用拾取模式（ActorPickerMode/SceneDepthPickerMode）、VR 编辑（VREditor + ViewportInteraction）、对齐吸附（ViewportSnapping）。交互模式 = 编辑器里临时接管视口输入的标准机制（工具型插件常驻 EdMode）。

**能做什么**：自定义编辑器模式（EdMode）做专用工具（建模模式即此形态）；特殊拾取工作流（从场景/深度选目标）；VR 中的编辑与审查流程。

#### 调试与专项面板（15 个模块）

**机制**：GameplayDebuggerEditor/MassEntityDebugger 挂运行时调试数据的视口叠加；StatsViewer 性能计数；DeviceProfileEditor 管设备配置档；PIEPreviewDeviceSpecification 模拟移动设备分辨率/性能档。

**能做什么**：游戏内调试 HUD（Gameplay Debugger 分类频道）；移动端预览与性能分档验证；设备配置（Device Profile）调优面板。

#### 属性与 UI 定制（5 个模块）

**机制**：PropertyEditor + DetailCustomizations 是"任意 UObject 自动生成属性面板"的引擎：FMathStructCustomization（*"Base class for math struct customization (e.g, vector, rotator, color)"*）这类定制类决定每种类型怎么渲染/编辑；ComponentVisualizers 给组件画视口句柄。这是游戏项目最常碰的编辑器扩展点。

- `FMathStructCustomization`（DetailCustomizations）：*"Base class for math struct customization (e.g, vector, rotator, color)"*——数学结构体的细节面板定制基类
- `FDetailsDisplayManager`（PropertyEditor）：*"provides an API to tweak various settings of your details view"*——细节视图显示设置的管理入口

**能做什么**：为项目自定义类型定制编辑体验（颜色选择器/曲线/滑杆约束）；隐藏/重排引擎属性防止美术误改；组件视口可视化（样条/约束/体积的手柄）。

#### 工具与杂项（10 个模块）

**机制**：Blutility 是"用蓝图写编辑器工具"的体系：UAssetActionUtility（*"Base class for all asset action-related utilities…"*）/UActorActionUtility 让蓝图函数直接出现在资产/Actor 右键菜单；UEditorUtilityDialogLibrary 提供 PIE 事件对话框。AddContentDialog/PluginWarden 管内容新建与插件合规。

- `UAssetActionUtility`（Blutility）：*"Base class for all asset action-related utilities. Any functions/events that are exposed on derived classes that have the correct signat[ure]…"*——资产动作工具基类：派生类上带正确签名的函数自动进右键菜单

**能做什么**：Editor Utility 蓝图：美术自助批量工具（免 C++）；Editor Utility Widget：拖控件搭工具面板；右键菜单动作（资产级/Actor 级）。

### 1.5 Developer 组逐子域分析（109 个模块，8 个子域）

#### 构建/烘焙/DDC（35 个模块）

**机制**：派生数据缓存采用函数式构建模型：FBuildDefinition（*"an immutable reference to a build function and its inputs"*）把"构建=函数+输入"变成可寻址对象——输入相同即命中缓存，这是 DDC 全部魔法的根基。Zen 是配套存储服务，Horde 是分布式调度（FBlobHandle：*"Handle to a blob"* 的对象存储模型）；各类资产烘焙器（MeshBuilder/NaniteBuilder/TextureBuild/ShaderPreprocessor）挂在其上。

- `FBuildDefinition`（DerivedDataCache）：*"A build definition is an immutable reference to a build function and its inputs."*——构建定义=函数+输入的不可变引用——内容寻址缓存的键
- `FBuildContext`（DerivedDataCache）：*"A build context provides the inputs for a build function and saves its outputs."*——构建上下文：供给输入、保存输出的执行环境
- `FBlobHandle`（Horde）：*"Handle to a blob."*——Horde 对象存储的 blob 句柄

**能做什么**：自定义烘焙产物缓存策略（共享 DDC/虚拟化到云存储）；烘焙流水线定制（资产烹饪顺序、依赖预热）；Horde 集群扩容：分布式 shader 编译/DDC 加速。

#### 平台与设备管理（8 个模块）

**机制**：FTargetPlatformBase（*"Base class for target platforms"*）定义目标平台抽象（ cooks/plays 什么格式），TargetDeviceServices 提供设备代理服务（发现/部署/执行），TurnkeyIO 自动下载安装平台依赖（SDK/证书）。

- `FTargetPlatformBase`（TargetPlatform）：*"Base class for target platforms."*——目标平台抽象基类：烹饪格式/纹理压缩/着色器格式的决策点
- `FTargetDeviceId`（TargetPlatform）：*"Implements a target devices identifier."*——目标设备标识

**能做什么**：新平台移植（嵌入式/定制主机）的平台模块；设备农场：批量部署到真机跑自动化；Turnkey 一键补齐平台环境。

#### 自动化与功能测试（10 个模块）

**机制**：FunctionalTesting 提供关卡内测试 Actor（AScreenshotFunctionalTest 系做截图金样比对）；AutomationDriver 是 UI 自动化的流式 API——By（*"a collection of fluent helper functions designed to make accessing and creating element locators easy"*）定位控件、Until/FWaitTimeout 构成等待模型，与 Selenium 同构。

- `By`（AutomationDriver）：*"Represents a collection of fluent helper functions designed to make accessing and creating element locators easy"*——元素定位器的流式构造（类似 Selenium 的 By）
- `AScreenshotFunctionalTest`（FunctionalTesting）：*"No UI"*——无 UI 截图测试（继承基类获得截图比对能力）

**能做什么**：Slate UI 自动化测试（按控件语义而非像素驱动）；关卡功能测试（放置测试 Actor + 断言序列）；截图回归基线管理；CI 冒烟与性能测试编排（配合 Gauntlet 插件）。

#### 分析与调试前端（19 个模块）

**机制**：TraceInsights 系即 Unreal Insights 的前端实现（FTimingEventSearch 做参数化时间轴事件检索），TraceServices/TraceAnalysis 消费 Trace 数据流；SessionFrontend 是远程会话统一面板（消息/测试/性能）；MessageLog/OutputLog 是结构化日志面。

- `FTimingEventSearchParameters`（TraceInsights）：*"Parameters for a timing event search."*——时间轴事件检索参数——Insights 里"找一帧里最贵的调用"背后的查询模型

**能做什么**：帧时间/网络/内存/资产加载四维性能分析；自动化性能报告（Insights 导出+比对）；自定义 Trace 通道的可视化扩展；远程会话调试（连真机/连服务器）。

#### 版本控制与协作（10 个模块）

**机制**：SourceControl 把版本控制操作对象化：FCheckIn（*"Operation used to check files into source control"*）/FCheckOut/FConnect——任何 VCS 后端（Git/Perforce/自研）实现同一套操作接口即可接入编辑器；UncontrolledChangelists 支持"非受控变更单"工作流；SubmitTool 定制提交流水线。

- `FCheckIn`（SourceControl）：*"Operation used to check files into source control"*——检出/提交/连接皆为操作对象——VCS 可插拔的接口设计
- `FAnnotationLine`（SourceControl）：*"A single line of an annotated file"*——文件注解行（blame 信息）

**能做什么**：接自研版本系统/资产审阅平台；提交前自动校验（命名/引用/截图）流水线；多用户同场景协作（Concert/MultiUser 插件的服务端就在这组）。

#### 资产工具与导入导出（12 个模块）

**机制**：AssetTools 的 FAssetTypeActions_Base（*"A base class for all AssetTypeActions"*）是资产右键动作的注册面（与 Editor 组 UAssetDefinition 分工：一个管"是什么资产"，一个管"能对它做什么"）；DatasmithExporter/Facade + DirectLink 支持从引擎反向导出与 DCC 直连实时同步。

- `FAssetTypeActions_Base`（AssetTools）：*"A base class for all AssetTypeActions."*——资产类型动作基类：右键菜单/拖放/颜色/缩略图的一站式注册

**能做什么**：自定义资产批量操作（右键菜单插件）；Datasmith 导出：把 UE 场景送进 DCC/归档；DirectLink：Maya/3ds Max 与编辑器增量同步。

#### 本地化（2 个模块）

**机制**：Localization 模块 + LocalizationDashboard 界面覆盖"采集→翻译→编译→导入导出"全流程；FLocTextHelper（*"High-level access to the non-compiled localization resources (manifests and archives)"*）抽象清单/档案两种资源格式。

- `FLocTextHelper`（Localization）：*"High-level access to the non-compiled localization resources (manifests and archives) in a way that abstracts some of their quirks."*——本地化资源高层访问：抹平清单/档案格式细节

**能做什么**：多语言管线（PO/XLIFF 交接翻译商）；运行时切语言/字体的自动化验证；文化区（Culture）特定的资产替换管线。

#### 编辑器支撑库（14 个模块）

**机制**：Settings/SettingsEditor 让 UDeveloperSettings 派生类自动获得设置面板；SourceCodeAccess 桥接各 IDE；StandaloneRenderer 让独立 Slate 程序能渲染；SlateReflector 提供控件树/样式审查器（F5 调 UI 神器）。

**能做什么**：项目设置面板（UDeveloperSettings 三行代码接入）；独立 Slate 小工具（不带引擎的轻量 GUI）；UI 调试：控件树/继承链/样式来源审查。

### 1.6 速查：域总表与模块全清单

#### 1.6.1 功能域总表

| 功能域 | 模块数 | 代表模块 | 一句话能力 |
|---|---|---|---|
| **核心与运行时基础** | 27 | ApplicationCore, AppFramework, BuildSettings, Core, CoreOnline… | 容器/算法/字符串/线程/内存等基础设施、UObject 反射与序列化、JSON/XML/Verse 语言运行时——一切模块的地基 |
| **游戏框架与玩法** | 13 | Engine, BlueprintRuntime, GameplayMediaEncoder, GameplayTags, GameplayTasks… | Actor/Component/关卡/游戏模式/标签/任务等玩法骨架与运行时游戏逻辑（含启动影片、内置菜单等外围） |
| **输入与 XR 设备** | 7 | InputCore, InputDevice, EyeTracker, HeadMountedDisplay, AugmentedReality… | 输入抽象、设备接口、眼动追踪、HMD/AR/XR 头显与语音 |
| **渲染与图形** | 20 | RenderCore, Renderer, RHI, RHICore, D3D12RHI… | 渲染器、RHI 抽象层与 D3D12/Vulkan/OpenGL 后端、贴图与网格数据转换、材质着色质量设置 |
| **物理与碰撞** | 13 | Chaos, ChaosCore, ChaosSolverEngine, ChaosSpatialPartitions, ChaosVehiclesCore… | Chaos 物理（刚体/载具/布料解算）、碰撞查询、力场与破坏（几何集合）、物理录制回放调试 |
| **几何与建模** | 14 | CADKernel, CADKernelEditor, CADKernelEngine, GeometryCore, GeometryFramework… | 网格描述数据结构、几何内核、CAD 内核、Dataflow 图、交互式建模工具框架（编辑器建模模式的地基） |
| **UI 界面** | 11 | AdvancedWidgets, Slate, SlateCore, SlateBaseRenderer, SlateNullRenderer… | Slate 保留模式 UI 框架 + UMG 蓝图化 UI + 内嵌网页浏览器与控件渲染 |
| **动画与布料** | 9 | AnimGraphRuntime, AnimationCore, ClothingSystemRuntimeCommon, ClothingSystemRuntimeInterface, ClothingSystemRuntimeNv… | 动画图运行时、动画核心数据、Live Link 外部数据流入、布料仿真、面部捕捉 MR 网格 |
| **Sequencer 与影视虚拟制片** | 12 | AVEncoder, AVIWriter, CinematicCamera, LevelSequence, MovieScene… | Sequencer 时间线、关卡序列、影片采集编码、虚拟摄制舞台数据、Cine 摄像机 |
| **音频** | 18 | AdpcmAudioDecoder, AudioAnalyzer, AudioCaptureCore, AudioCaptureRtAudio, AudioChannelAgnosticCore… | 音频混音器、DSP 信号处理、音频分析器/采集、Audio Link、各类音频编解码器（Opus/Vorbis/Bink/ADPCM） |
| **AI 与导航** | 3 | AIModule, Navmesh, NavigationSystem | AI 控制器/行为树/黑板/感知、导航系统与 Navmesh 生成查询 |
| **网络与在线服务** | 41 | BandwidthDebugDelegates, BandwidthMeasurementTool, ClientBandwidthDebugVisualizer, ClientPilot, DownlinkBandwidthManager… | 复制与 PacketHandler、Iris 新一代复制、Socket/HTTP/WebSocket/XMPP 消息总线、Portal 会话服务、网络回放流 |
| **媒体播放** | 4 | ImageDownload, Media, MediaAssets, MediaUtils | 媒体资产/播放器框架与媒体工具（视频源播放、图片下载） |
| **地形与植被** | 2 | Foliage, Landscape | Landscape 地形与 Foliage 植被实例化 |
| **Mass 实体系统** | 5 | MassCore, MassDeveloper, MassEngine, MassEntity, MassSignals | Mass Entity/ECS 式大规模实体框架（人群、环境模拟）与信号 |
| **资产与内容管线** | 20 | AssetRegistry, BackgroundHTTP, BackgroundHTTPFileHash, BuildPatchServices, DatasmithCore… | Asset Registry 资产注册表、Interchange 导入框架、Datasmith、Pak/IO Store 打包、按需下载、补丁分发、网络文件系统 |
| **遥测与性能分析** | 17 | Analytics, AnalyticsCSV, AnalyticsET, AnalyticsHorde, AnalyticsLog… | Analytics 遥测后端、Trace/Insights 追踪、性能计数器、硬件调查、Rewind Debugger 接口 |
| **自动化测试** | 3 | AutomationMessages, AutomationTest, AutomationWorker | 自动化测试框架运行时侧（Automation Test/Worker/Messages） |
| **新兴与实验技术** | 6 | AutoRTFM, CUDA, NNE, VectorVM, VerseCompiler… | Verse 语言编译器、NNE 神经网络推理、VectorVM、CUDA 绑定、AutoRTFM 事务内存、StateStream |

#### 1.6.2 API 面积 Top 25 模块

| # | 模块 | 组 | 总条目 | Classes | Structs | Enums | Functions |
|---|---|---|---|---|---|---|---|
| 1 | Engine | Runtime | 8,796 | 2,456 | 2,440 | 904 | 2,004 |
| 2 | Core | Runtime | 6,277 | 927 | 1,070 | 278 | 2,935 |
| 3 | CoreUObject | Runtime | 2,365 | 392 | 449 | 200 | 1,089 |
| 4 | Chaos | Runtime | 2,162 | 644 | 320 | 131 | 750 |
| 5 | UnrealEd | Editor | 1,840 | 857 | 270 | 159 | 363 |
| 6 | RenderCore | Runtime | 1,648 | 283 | 167 | 78 | 864 |
| 7 | GeometryCore | Runtime | 1,333 | 232 | 142 | 27 | 661 |
| 8 | MovieScene | Runtime | 1,312 | 118 | 656 | 66 | 361 |
| 9 | RHI | Runtime | 1,099 | 124 | 214 | 99 | 556 |
| 10 | SlateCore | Runtime | 853 | 140 | 188 | 82 | 320 |
| 11 | VerseCompiler | Runtime | 662 | 200 | 115 | 41 | 189 |
| 12 | IrisCore | Runtime | 658 | 116 | 228 | 37 | 219 |
| 13 | Slate | Runtime | 567 | 237 | 67 | 65 | 50 |
| 14 | TypedElementFramework | Runtime | 538 | 55 | 185 | 19 | 189 |
| 15 | AIModule | Runtime | 529 | 195 | 147 | 77 | 33 |
| 16 | Renderer | Runtime | 523 | 92 | 61 | 30 | 307 |
| 17 | Navmesh | Runtime | 517 | 25 | 68 | 23 | 311 |
| 18 | InteractiveToolsFramework | Runtime | 450 | 196 | 45 | 32 | 127 |
| 19 | MovieSceneTracks | Runtime | 373 | 179 | 154 | 10 | 22 |
| 20 | Landscape | Runtime | 343 | 92 | 87 | 42 | 93 |
| 21 | CUDA | Runtime | 334 | 1 | 1 | 0 | 3 |
| 22 | uLangCore | Runtime | 331 | 47 | 69 | 14 | 136 |
| 23 | UMG | Runtime | 325 | 203 | 44 | 25 | 37 |
| 24 | SequencerCore | Editor | 324 | 60 | 67 | 25 | 112 |
| 25 | Sequencer | Editor | 323 | 108 | 77 | 30 | 40 |

解读（综合判断）：Engine/Core/CoreUObject 三巨头贡献约 1.7 万条条目，是游戏框架与对象系统的绝对核心；Chaos（物理）与 RenderCore/RHI（渲染）的体量说明二者仍是 5.x 的扩张主战场；VerseCompiler 进入前 11，反映 Verse 语言在引擎内的权重。

#### 1.6.3 重点模块速览

- **Engine**——游戏世界的全部骨架：Actor/Component/关卡/光照/相机/粒子(Cascade)/声音组件、角色移动组件、蓝图运行时桥。官方对 AActor 的描述是"可放置或生成到关卡中的对象基类"，UWorld 为"代表一张地图或沙盒、容纳 Actor 与 Component 的顶层对象"
- **Core**——引擎最底层：容器(TArray/TMap)、字符串(FString)、智能指针、线程与任务图、数学库宿主；API 面积全引擎第二
- **CoreUObject**——UObject 反射/序列化/GC/软引用体系：UObject（"所有 UE 对象的基类"）、UClass、UPackage、委托与属性包装
- **Chaos**（关联：ChaosCore, ChaosSolverEngine, FieldSystemEngine）——Chaos 物理核心：刚体解算器、几何集合（FGeometryCollection，破坏系统的数据结构）、聚类与碰撞
- **PhysicsCore**——物理抽象层：碰撞通道/Profile、BodyInstance 与物理接口的公共定义
- **Renderer**——场景渲染器：延迟着色管线、光照、阴影、后处理的实现层
- **RenderCore**——渲染公共层：着色器绑定、顶点工厂（FVertexFactory："封装可链接进顶点着色器的顶点数据源"）、GPU 统计
- **RHI**（关联：D3D12RHI, VulkanRHI, OpenGLDrv）——渲染硬件接口：FRHICommandList/FRHITexture 等跨 API 抽象；D3D12RHI/VulkanRHI/OpenGLDrv 为平台后端
- **Slate / SlateCore**——保留模式 UI 框架，编辑器全部界面与运行时 HUD 的地基；SWindow 为"平台无关的顶层窗口表示"
- **UMG**——蓝图可视化 UI：UUserWidget（"通过 WidgetBlueprint 实现 UI 可扩展性的控件"）、Button/CanvasPanel 等 UObject 包装控件
- **AIModule**——AI 框架：AAIController（"AI 控制 Pawn 的控制器基类"）、行为树/黑板组件、感知系统
- **NavigationSystem / Navmesh**——导航与寻路：NavMesh 边界体积（"仅阻挡路径构建、无游戏碰撞"）、寻路查询、导航数据生成
- **MovieScene / Sequencer / LevelSequence**（关联：MovieSceneTracks, SequencerCore, Sequencer）——Sequencer 时间线体系：UMovieScene（"影片场景资产"）、轨道求值、关卡序列与录制
- **Landscape / Foliage**——地形高度场渲染与编辑、植被实例化刷绘
- **MassEntity / MassCore**（关联：MassEngine, MassSignals）——ECS 式大规模实体：UMassEntitySubsystem（"承载 FMassEntityManager 默认实例的世界子系统"）、生成器与信号
- **AnimGraphRuntime / AnimationCore**——动画图运行时求值、混合空间、动画姿势数据结构
- **LiveLink 三件套**（关联：LiveLinkInterface, LiveLinkMessageBusFramework）——外部动画/设备数据流入框架（动作捕捉、DCC 联动）
- **AudioMixer / SignalProcessing**——音频混音器主框架与 DSP；配合各编解码器模块与 AudioLink 对接外部混音器
- **NetCore / PacketHandler / IrisCore**——经典复制栈与新一代复制系统 Iris（5.x 官方在研替代方案）
- **AssetRegistry**——资产注册表：编辑器/运行时枚举与查询项目资产（Python/蓝图的资产查询 API 即其暴露面）
- **InterchangeCore / InterchangeEngine**——统一导入管线框架：UInterchangePipelineBase（"管线实现"）——FBX/glTF/USD 等导入器的公共架构
- **UnrealEd**——编辑器主模块（857 类）：UEditorEngine（"驱动编辑器的引擎"）、事务/选择/PIE/工具基类
- **Kismet / BlueprintGraph**——蓝图编辑器与蓝图编译器（Kismet 为蓝图系统内部代号）
- **VerseCompiler / uLang 系列**——Verse 语言（UEFN 背后的新脚本语言）编译器与运行时核心
- **NNE**——神经网络引擎：UNNEModelData（"存储神经网络模型数据的资产"），在引擎内跑推理
- **TypedElementFramework**——类型化元素框架：编辑器中统一表示"任何可被选中/操作的对象"的新抽象
- **InteractiveToolsFramework**——交互式工具框架：建模模式、雕刻等编辑器工具的标准基类
- **GeometryCore / MeshDescription 系列**（关联：GeometryFramework, StaticMeshDescription, SkeletalMeshDescription）——几何处理库与网格数据结构（建模工具链的数据底座）

<details><summary>各域完整模块清单（点开展开）</summary>

- **核心与运行时基础**（27）：ApplicationCore, AppFramework, BuildSettings, Core, CoreOnline, CorePreciseFP, CoreUObject, CrashReportCore, Cbor, DeveloperSettings, EngineSettings, EventLoop, FieldNotification, Json, JsonObjectGraph, JsonUtilities, Launch, MathCore, PropertyPath, Serialization, XmlParser, uLangCore, uLangJSON, uLangUE, Projects, TypedElementFramework, TypedElementRuntime
- **游戏框架与玩法**（13）：Engine, BlueprintRuntime, GameplayMediaEncoder, GameplayTags, GameplayTasks, UELibrary, Advertising, FriendsAndChat, GameMenuBuilder, GameplayDebugger, MoviePlayer, MoviePlayerProxy, PreLoadScreen
- **输入与 XR 设备**（7）：InputCore, InputDevice, EyeTracker, HeadMountedDisplay, AugmentedReality, Overlay, Voice
- **渲染与图形**（20）：RenderCore, Renderer, RHI, RHICore, D3D12RHI, OpenGLDrv, VulkanRHI, NullDrv, ImageCore, ImageWrapper, ImageWriteQueue, IESFile, ISMPool, MaterialShaderQualitySettings, MeshConversion, MeshConversionEngineTypes, MeshUtilitiesCommon, TextureUtilitiesCommon, StreamingPauseRendering, OpenColorIOWrapper
- **物理与碰撞**（13）：Chaos, ChaosCore, ChaosSolverEngine, ChaosSpatialPartitions, ChaosVehiclesCore, ChaosVehiclesEngine, Constraints, FieldSystemEngine, RigidPhysics, PhysicsCore, Voronoi, ChaosVDData, ChaosVDRuntime
- **几何与建模**（14）：CADKernel, CADKernelEditor, CADKernelEngine, GeometryCore, GeometryFramework, GeometryCollectionEngine, MeshDescription, StaticMeshDescription, SkeletalMeshDescription, RawMesh, DataflowCore, DataflowEngine, DataflowSimulation, InteractiveToolsFramework
- **UI 界面**（11）：AdvancedWidgets, Slate, SlateCore, SlateBaseRenderer, SlateNullRenderer, SlateRHIRenderer, UMG, WidgetCarousel, WebBrowser, WebBrowserTexture, CEF3Utils
- **动画与布料**（9）：AnimGraphRuntime, AnimationCore, ClothingSystemRuntimeCommon, ClothingSystemRuntimeInterface, ClothingSystemRuntimeNv, LiveLinkAnimationCore, LiveLinkInterface, LiveLinkMessageBusFramework, MRMesh
- **Sequencer 与影视虚拟制片**（12）：AVEncoder, AVIWriter, CinematicCamera, LevelSequence, MovieScene, MovieSceneCapture, MovieSceneTracks, SequenceRuntimeRecorder, SerializedRecorderInterface, StageDataCore, TimeManagement, VirtualProduction
- **音频**（18）：AdpcmAudioDecoder, AudioAnalyzer, AudioCaptureCore, AudioCaptureRtAudio, AudioChannelAgnosticCore, AudioExtensions, AudioLinkCore, AudioLinkEngine, AudioMixer, AudioMixerCore, AudioPlatformConfiguration, BinkAudioDecoder, NonRealtimeAudioRenderer, OpusAudioDecoder, RadAudioDecoder, SignalProcessing, SoundFieldRendering, VorbisAudioDecoder
- **AI 与导航**（3）：AIModule, Navmesh, NavigationSystem
- **网络与在线服务**（41）：BandwidthDebugDelegates, BandwidthMeasurementTool, ClientBandwidthDebugVisualizer, ClientPilot, DownlinkBandwidthManager, EngineMessages, ExternalRpcRegistry, HTTP, HttpNetworkReplayStreaming, HttpServer, Icmp, InMemoryNetworkReplayStreaming, IPC, IrisCore, LocalFileNetworkReplayStreaming, Messaging, MessagingCommon, MessagingRpc, NetCommon, NetCore, NetworkReplayStreaming, Networking, NullNetworkReplayStreaming, PacketHandler, PortalMessages, PortalRpc, PortalServices, ReliabilityHandlerComponent, RSA, SSL, SaveGameNetworkReplayStreaming, SessionMessages, SessionServices, Sockets, Stomp, WebSockets, WebSocketServer, XMPP, GDKRuntime, GDKSaveGameSystem, GDKPackageManifest
- **媒体播放**（4）：ImageDownload, Media, MediaAssets, MediaUtils
- **地形与植被**（2）：Foliage, Landscape
- **Mass 实体系统**（5）：MassCore, MassDeveloper, MassEngine, MassEntity, MassSignals
- **资产与内容管线**（20）：AssetRegistry, BackgroundHTTP, BackgroundHTTPFileHash, BuildPatchServices, DatasmithCore, DumpPackageToJson, IndexedCacheStorage, InterchangeCore, InterchangeEngine, IoStoreOnDemandCore, NetworkFile, NetworkFileSystem, PakFile, RuntimeAssetCache, SandboxFile, StreamingFile, UniversalObjectLocator, InstallBundleManager, LauncherCheck, LauncherPlatform
- **遥测与性能分析**（17）：Analytics, AnalyticsCSV, AnalyticsET, AnalyticsHorde, AnalyticsLog, AnalyticsSwrve, AnalyticsVisualEditing, HardwareSurvey, Instrumentation, PerfCounters, StudioTelemetry, SynthBenchmark, TelemetryUtils, TraceBasedDebuggers, TraceBasedDebuggersAnalysis, TraceLog, RewindDebuggerRuntimeInterface
- **自动化测试**（3）：AutomationMessages, AutomationTest, AutomationWorker
- **新兴与实验技术**（6）：AutoRTFM, CUDA, NNE, VectorVM, VerseCompiler, StateStream

</details>

#### 1.6.4 各域学习路径（先读哪三个类）

| 域 | 模块 | 阅读顺序 |
|---|---|---|
| 游戏框架 | Engine | AActor → UActorComponent → AGameModeBase → UGameplayStatics |
| 对象系统 | CoreUObject | UObject → UClass → FSoftObjectPath → FObjectInitializer |
| 物理 | Chaos + ChaosSolverEngine | UChaosSolver → FGeometryCollection → UFieldSystemComponent |
| 渲染 | RenderCore + Renderer | FVertexFactory → FSceneInterface → FSceneRenderer 系 |
| UI | Slate + UMG | SWidget → SWindow → UWidget → UUserWidget |
| AI | AIModule | AAIController → UBehaviorTreeComponent → UAIPerceptionComponent |
| Sequencer | MovieScene + LevelSequence | UMovieSceneSequence → ULevelSequence → ULevelSequencePlayer |
| 网络 | NetCore | UNetDriver → FGuidReferences(NetGUID 机制) → FConnectionHandle |
| 资产管线 | AssetRegistry + InterchangeCore | IAssetRegistry → FAssetRegistryState → UInterchangePipelineBase |
| 编辑器扩展 | UnrealEd + EditorSubsystem 模块 | UEditorSubsystem → FAssetTypeActions_Base(AssetTools) → UAssetDefinition |
| Mass | MassEntity | UMassEntitySubsystem → UMassSpawner → Processor 模式 |
| 音频 | AudioMixer | UQuartzSubsystem → FMixerAudioBus → MetaSound 插件 |

#### 1.6.5 核心模块内部导览（类与官方 Remarks）

**Engine**

- `AController`：*"Controllers are non-physical actors that possess a Pawn to control its actions."*——控制器的本质：非物理 Actor，占有 Pawn 来驱动它
- `AInfo`：*"Info, the root of all information holding classes."*——所有"信息载体"类的根（GameMode/PlayerState 等挂在它下面）
- `APlayerState`：*"A PlayerState is created for every player on a server"*——每个玩家一份的服务器侧状态（名字/分数的归所）
- `UCheatManager`：*"Cheat Manager is a central blueprint to implement test and debug code and actions that are not to ship…"*——作弊/调试命令的集中地——"不随游戏发行"的测试动作
- `UInstancedStaticMeshComponent`：*"A component that efficiently renders multiple instances of the same StaticMesh."*——高效渲染同网格多实例——植被/森林/人群的标准件
- `UCapsuleComponent / USphereComponent / UBoxComponent`：*"generally used for simple collision. Bounds are rendered as lines in the editor."*——三大碰撞基元——角色胶囊体的老家
- `UMaterial`：*"A Material is an asset which can be applied to a mesh to control the visual look of the scene."*——材质资产定义
- `UExponentialHeightFogComponent`：*"Used to create fogging effects…with a density that is related to the height of the fog."*——指数高度雾

**Core**

- `FArchive`：*"Base class for archives that can be used for loading, saving, and garbage collecting in a byte order neutral way"*——归档器：一个抽象同时服务序列化/存档/垃圾回收三件事——引擎最经典的接口复用
- `FRunnable / FThread`：*"Interface for "runnable" objects. / Simple API for system threads."*——线程的官方姿势：Runnable 接口 + FThread 包装
- `TArray / FString / FName`：*"Templated dynamic array / A dynamically sizeable string / Public name, available to the world."*——三大基础类型；FName 走全局名表（"对世界公开的名字"）
- `FColor / FGuid / FDateTime`：*"Stores a color with 8 bits…/ Implements a globally unique identifier / Implements a date and time"*——常用值类型的家

**CoreUObject**

- `FProperty`：*"An UnrealScript variable."*——属性反射类——Remarks 仍写着历史名 UnrealScript：反射系统从 UE3 脚本时代一路演化而来
- `UObjectBase`：*"Low level implementation of UObject, should not be used directly in game code"*——UObject 的低层实现（游戏代码不应直用）

**Chaos**

- `FBasicBroadPhase`：*"…pass them onto the collision detector if their AABBs overlap."*——宽相筛对
- `FCCDModifier`：*"…modify the results of CCD collision detection prior to the CCD rewind being applied."*——CCD 修正点
- `FGeometryCollection`：*"( FTransformCollection )"*——可破坏资产的分层网格数据结构（继承自变换集合）

**UnrealEd**

- `UEditorEngine`：*"Engine that drives the Editor."*——编辑器引擎本体
- `FAssetEditorToolkit`：*"Base class for toolkits that are used for asset editing (abstract)"*——资产编辑器容器基类
- `FAssetDeleteModel`：*"The model behind a delete operation, which is an asynchronous process because of all the checks…against the GC"*——删资产是异步的——引用与 GC 检查决定了编辑器的每次删除

**MovieScene**

- `UMovieScene`：*"Implements a movie scene asset."*——序列资产
- `FInterrogationChannels（MovieSceneTracks）`：*"…interrogating Sequencer entity data without applying any state to objects."*——无副作用审讯序列数据

**AIModule**

- `AAIController`：*"AIController is the base class of controllers for AI-controlled Pawns."*——AI 控制器
- `UAIPerceptionComponent`：*"…register as stimuli listener in AIPerceptionSystem and gathers registered stimuli"*——感知监听
- `UBTTaskNode`：*"Task are leaf nodes of behavior tree, which perform actual actions"*——行为树叶节点

#### 1.6.6 核心类成员面（叶级抽样，32 类）

再往下一层抽样：直接抓取 32 个核心类的**类页面**（叶级），统计其文档化的函数/变量/派生类数量。这一层能看到模块页看不到的东西——引擎真正的"重量都压在哪几个类上"。

| 类 | 模块 | 函数 | 变量 | 派生类 | 类 | 模块 | 函数 | 变量 | 派生类 |
|---|---|---|---|---|---|---|---|---|---|
| AActor | Engine | 643 | 117 | 210 | UGameInstance | Engine | 99 | 10 | 3 |
| UEditorEngine | UnrealEd | 497 | 129 | 1 | AAIController | AIModule | 80 | 12 | 2 |
| UWorld | Engine | 450 | 196 | 0 | UPackage | CoreUObject | 78 | 20 | 0 |
| UCharacterMovementComponent | Engine | 354 | 236 | 1 | AGameModeBase | Engine | 74 | 15 | 5 |
| UNavigationSystemV1 | NavigationSystem | 277 | 22 | 0 | FGeometryCollection | Chaos | 59 | 26 | 2 |
| UUserWidget | UMG | 250 | 38 | 12 | FRHICommandList | RHI | 58 | 0 | 3 |
| UMaterial | Engine | 224 | 145 | 2 | UAIPerceptionComponent | AIModule | 54 | 9 | 0 |
| SWidget | SlateCore | 205 | 35 | 7 | UMovieSceneSequence | MovieScene | 54 | 2 | 8 |
| UStaticMeshComponent | Engine | 183 | 62 | 17 | UInterchangeBaseNodeContainer | InterchangeCore | 39 | 2 | 0 |
| UObject | CoreUObject | 179 | 0 | 2,001 | FVertexFactory | RenderCore | 29 | 6 | 11 |
| SWindow | SlateCore | 175 | 11 | 18 | FDDoSDetection | NetCore | 27 | 1 | 0 |
| ACharacter | Engine | 173 | 88 | 3 | ULevelSequencePlayer | LevelSequence | 20 | 8 | 1 |
| UGameplayStatics | Engine | 164 | 0 | 0 | FAssetRegistryModule | AssetRegistry | 20 | 0 | 0 |
| FArchive | Core | 152 | 44 | 26 | UNNEModelData | NNE | 15 | 7 | 0 |
| ALandscape | Landscape | 138 | 30 | 0 | UMassEntitySubsystem | MassEntity | 3 | 0 | 1 |
| UBehaviorTreeComponent | AIModule | 105 | 0 | 0 | UChaosSolver | ChaosSolverEngine | 1 | 0 | 0 |

- **AActor 是引擎最胖的玩法类**：643 个文档化函数 + 117 变量 + **210 个文档化派生类**——可放置物的家族树。
- **UObject 的派生类清单有 2,001 个**——"一切之根"第一次有了量化数字（该清单还只是文档页直接列出的直接派生）。
- **UCharacterMovementComponent 是"配置之王"**：354 函数 + **236 个变量**——移动手感全靠参数堆出来的实证。
- **UEditorEngine 有 497 个函数**，直逼 AActor——编辑器引擎本体的类面与游戏核心同量级。
- **薄壳模式**：UChaosSolver（1 函数）、UMassEntitySubsystem（3 函数）这类"上层包装类"在文档面极薄——真实工作全在 F 层（Chaos 解算器内核/FMassEntityManager），印证 1.2.3 反射密度谱的结论：U 类只是壳。
- UUserWidget 250 函数/12 派生、SWidget 205 函数/7 派生——UI 两层基类的家族规模。

类页还带完整版类注释（模块页只给一行截断）。AActor 页官方完整说明包含 **Actor 初始化顺序**：*"Actor initialization has multiple steps, here's the order of important virtual functions that get called"*——从 UObject::PostLoad（仅静态放置的 Actor）→ UActorComponent::OnComponentCreated（生成时）开始的完整虚函数调用次序，这是生命周期问题的权威出处（比模块页 Remarks 详细得多）。

### 1.7 官方插件生态：842 个插件按类能给什么能力

文档站 PluginIndex 收录 842 个官方插件（1375 个插件模块）；本机 5.8 安装版实测 893 个 `.uplugin`（抽 8 个与文档页逐字节比对一致，见附录）。287 个位于 Experimental/Beta 目录（约三分之一，选用需评估）。主要分类的能力画像（描述为官方原文）：

**Animation（83 个）**——动画生产链全覆盖：压缩（ACLPlugin）、程序化绑定（ControlRig "Framework for animation driven by user controls"）、重定向（IKRig）、外部流入（LiveLink）、性能（AnimationBudgetAllocator 动画预算分配）、共享姿势（AnimationSharing）。做角色动画技术方案基本绕不开这一类。

**Virtual Production（73 个）**——虚拟摄制全家桶：nDisplay 多屏（DisplayClusterLaunch）、虚拟相机（VCam/CineCameraRigs）、实时合成（Composite/Composure）、远程控制（RemoteControl）、关卡快照（LevelSnapshots）、Switchboard 统一启动器。是片场级虚拟化拍摄的工具箱。

**Editor（67 个）**——编辑器生产力：建模模式（ModelingToolsEditorMode）、PCG 程序化内容生成（"Visual scripting framework for procedurally populating worlds"）、电子表格式批量编辑（ObjectMixer "Edit any properties of scene objects in a spreadsheet format"）、多用户协作（MultiUserClient）、崩溃恢复（DisasterRecoveryClient）。

**Media Players（41 个）**——按平台/格式的播放器矩阵：ElectraPlayer（跨平台流媒体主力）、ImgMedia（EXR 序列/LED 墙）、平台原生（AvfMedia/WindowsMoviePlayer/WebMMedia）、采集卡（AjaMedia）。配合 Media 框架三件套选用。

**Online Platform（36 个）**——在线服务矩阵：OnlineSubsystemUtils + 各平台实现（EOS/GooglePlay/iOS/Xbox），覆盖账号/好友/成就/匹配/语音。新一代统一入口是 OnlineServices 体系。

**Audio（33 个）**——音频高阶体系：MetaSound（DSP 图式音源，"complete control over audio DSP graph generation"）、参数调制（AudioModulation）、空间声场（ResonanceAudio/SoundFields）、采集（AudioCapture）、调优（AudioInsights）。

**Gameplay（29 个）**——玩法框架级组件：GAS（GameplayAbilities "Adds GameplayEffect and GameplayAbility classes to handle complicated gameplay interactions"）、模块化玩法（ModularGameplay + GameFeatures 插件化内容）、通用状态机（StateTree "General purpose hierarchical state machine"）、智能对象（SmartObjects）、对话树（CommonConversation）。

**Rendering（26 个）**——渲染扩展与调试：自定义/程序化网格组件（CustomMeshComponent/ProceduralMeshComponent）、色彩管理（OpenColorIO）、GPU 调试（RenderDocPlugin/PixWinPlugin/DumpGPUServices）、体渲染工具（Volumetrics）。

**Physics（24 个）**——Chaos 专用玩法层：解算器（ChaosSolverPlugin）、布料（ChaosCloth/ChaosClothAsset 板型布料资产）、物理控制（PhysicsControl）、破碎辅助（PlanarCut 平面切割）。

**Importers（22 个）**——数据进口：Datasmith 工业管线（CAD/C4D/Revit）、Alembic/USD/SpeedTree/AxF 专用导入器。配合 Interchange 框架自定义扩展。

**Testing（20 个）**——测试基建：Gauntlet 整包自动化（"helper class for creating and managing tests in your game"）、自动化性能测试（AutomatedPerfTesting）、自动化 RPC（AutomationControllerRpc）。

**FX（10 个）**——特效全家桶：Niagara 本体 + 流体（NiagaraFluids "Fluid simulation toolkit for Niagara"）、Nanite 渲染器（NiagaraNanite）、仿真缓存回放（NiagaraSimCaching）、旧系统 Cascade 与迁移器（CascadeToNiagaraConverter）、AI 工具（NiagaraToolsets）。

**AI（11 个）**——AI 增强：Mass 人群/交通（MassAI/MassCrowd）、环境查询编辑器、HTN 规划器（实验）、机器学习（LearningAgents "machine learning library for AI character control"、MLAdapter RPC 训练桥）。

**UI（11 个）**——UI 体系增强：CommonUI（"A repository for game independent UI elements" 主机级 UI 库）、MVVM（SlateModelViewViewModel/ModelViewViewModelPreview）、即时模式（SlateIM "immediate mode wrapper for Slate"）、预览调试（UMGWidgetPreview）、AI 操控（UMGToolSet）。

**Geometry（11 个）**——几何/毛发：GeometryScripting（蓝图几何函数库）、毛发渲染模拟（HairStrands "Rendering and simulation of grooms"）、发卡生成（HairCardGenerator）、几何集合（GeometryCollectionPlugin）、几何数据流（GeometryDataflow/GeometryFlow）。

**Scripting（9 个）**——脚本与数据科学：PythonScriptPlugin（编辑器 Python）、EditorScriptingUtilities、SequencerScripting（序列脚本化）、ML Python 包（PyTorch/TensorBoard/MLflow 自动装）。

**MetaHuman（12 个）**——数字人官方套件：MetaHuman 本体、生成器（MetaHumanGenerator "AI-driven character creation and editing"）、校准诊断、动画工具、UAF 支持。

**Virtual Reality（12 个）**——XR 标准与外设：OpenXR 标准（"OpenXR is an open VR/AR standard"）+ 手部追踪/眼动/面捕扩展、MixedRealityCapture 混合现实采集框架。

**ML（5 个）**——NNE 推理后端矩阵：ONNX Runtime（CPU/GPU）、IREE（MLIR 编译栈）、CoreML（苹果）、RDG（渲染图内推理）——同一 NNE 模型资产四种部署路径。

**Input Devices（10 个）**——输入外设：RawInput（飞行摇杆/方向盘）、GameInput（新一代统一输入 API）、MIDI/OSC（音乐与演出控制）、数位笔（StylusInput）。

**Water（4 个）**——水系统：Water 主体（"oceans, river, lakes or custom water bodies that carve landscape and interacts with gameplay"）、浮力（Buoyancy）、高级模拟（WaterAdvanced 基于 Niagara Fluids）。

**Compositing（7 个）**——实时合成：新一代 Composite/CompositeCore（带默认 holdout 管线）、镜头畸变（OpenCVLensDistortion 校准与置换图）。

其余分类：Messaging 15、Insights 13、Platform 9、Codecs 6、Mobile 6、Blueprints 5、Performance 5、Device Profile Selectors 5、Augmented Reality 5、Content Browser 4、Build Distribution 4、Database 4、Examples 3、Accessibility 3、Compression 2、Localization 2、Learning 2、Dataprep 2、Telemetry 2、2D 1（Paper2D "tools and assets to help create 2D games"）等。全量计数表见附录数据文件。

#### 1.7.1 插件模块反射面排行（本地源码口径）

插件生态的"重量"用另一把尺子量：在本机 UE_5.8 安装版源码里统计每个插件模块的**反射面**（UCLASS/USTRUCT/UENUM/UINTERFACE 声明计数）。这不是文档页条目口径（文档 Classes 表含非反射的纯 C++ 类，本地无法稳定复现），而是"可被蓝图/序列化/编辑器看见的类型面"——对插件而言恰恰是最有意义的度量：插件的价值就在于把能力暴露出来。统计范围：87 个重要插件的 262 个模块（目录定位 262/283）。

锚定对照：引擎 Engine 模块本地 UCLASS 计数 1,326——即最重的官方插件 Niagara（224 个 UCLASS）约为 Engine 的 17%，PCG（443）约为 1/3。**没有任何插件的反射面能比肩引擎核心模块，但头部插件已经是"准引擎级"的体量**。

| 插件模块 | 所属插件 | 实验位 | UCLASS | USTRUCT | UENUM | UINTERFACE | 合计 |
|---|---|---|---|---|---|---|---|
| PCG | PCG |  | 443 | 195 | 207 | 7 | **852** |
| ControlRig | ControlRig |  | 35 | 646 | 46 | 2 | **729** |
| Niagara | Niagara |  | 224 | 286 | 155 | 5 | **670** |
| NiagaraEditor | Niagara |  | 214 | 111 | 27 | 0 | **352** |
| MeshModelingTools | MeshModelingToolset |  | 224 | 2 | 79 | 0 | **305** |
| GameplayAbilities | GameplayAbilities |  | 115 | 116 | 42 | 4 | **277** |
| GeometryScriptingCore | GeometryScripting |  | 46 | 145 | 85 | 0 | **276** |
| CustomizableObjectEditor | Mutable |  | 175 | 38 | 26 | 4 | **243** |
| AvalancheMedia | Avalanche |  | 50 | 151 | 37 | 2 | **240** |
| MovieRenderPipelineCore | MovieRenderPipeline |  | 140 | 41 | 33 | 4 | **218** |
| IKRig | IKRig |  | 55 | 115 | 23 | 1 | **194** |
| StateTreeModule | StateTree |  | 10 | 145 | 35 | 1 | **191** |
| DataflowNodes | Dataflow |  | 0 | 179 | 7 | 0 | **186** |
| Mover | Mover | EXP | 53 | 100 | 15 | 4 | **172** |
| TextureGraph | TextureGraph |  | 97 | 21 | 10 | 0 | **128** |
| ModelingComponents | MeshModelingToolset |  | 72 | 15 | 20 | 8 | **115** |
| PCGEditor | PCG |  | 77 | 23 | 9 | 0 | **109** |
| Chooser | Chooser |  | 15 | 73 | 9 | 7 | **104** |
| DataflowEditor | Dataflow |  | 64 | 21 | 17 | 2 | **104** |
| ControlRigEditor | ControlRig |  | 54 | 37 | 9 | 0 | **100** |

- 模块 Top 3：PCG 852（U443+S195+E207）、ControlRig 729（其中 USTRUCT 646——绑定单位 RigUnit 几乎全是结构体，结构体驱动的框架设计）、Niagara 670
- 插件 Top 5：Niagara 1047（7 模块）、PCG 962（3 模块）、ControlRig 837（3 模块）、Avalanche 682（32 模块——模块数最多但单模块小）、MeshModelingToolset 559（7 模块）
- 实验 vs 稳定：实验插件模块均值 18 条 vs 稳定 37 条——**体量与成熟度正相关**，实验插件确实"还没长大"，选型时值得纳入考量
- GAS（GameplayAbilities 277）与 GeometryScripting（294）、StateTree（311）、IKRig（246）、MovieRenderPipeline（284）构成第二梯队——玩法与管线插件的反射面显著大于一般编辑器工具插件


## 二、Blueprint API：设计师看到的那一面（889 个分类）

蓝图 API 参考是全部蓝图节点的目录树。根页官方声明：*"The Blueprint API reference is an early work in progress — it strives to reflect all available nodes, but it is not guaranteed to be an exhaustive list."*（仍在早期建设，力求全量但不保证穷尽。）规模：889 个分类页**已全量抓取**，合计 14,613 个子条目（子分类+节点页）。子条目最多的分类：

| 分类 | 子条目 | 分类 | 子条目 |
|---|---|---|---|
| AnimDatabase | 527 | LearningAgents | 443 |
| MaterialDesigner | 381 | AnimGen | 297 |
| EventDispatchers | 228 | Cloner | 199 |
| Rendering | 192 | Settings | 187 |
| URigHierarchy | 182 | RigVMController | 178 |
| Niagara | 177 | Mover | 170 |
| Widget | 152 | FXConverterUtilities | 148 |
| MovieGraph | 144 | Animation | 140 |
| MovieRenderPipeline | 137 | Effector | 136 |
| Physics | 136 | DrawDebugLibrary | 133 |

### 2.1 十六个典型工作流（节点名均取自抓取数据）

**生成与查找 Actor**（Actor 分类（32 子项））——SpawnActor 系列 + Get All Actors Of Class / Find Nearest Actor / Actor Has Tag；配合 Game 分类的 Add Component by Class、Construct Object from Class、Get Game Mode / Get Game State / Get Instigator、FindPlayerStart、Flush Level Streaming——从"造一个东西"到"问世界要信息"的第一入口集。

**物理交互**（Physics 分类（136 子项））——力与冲量全家桶：Add Force（At Location/Local/All Bodies Below 变体）、Add Impulse、Add Angular Impulse in Degrees/Radians、Add Torque、Add Radial Force；约束控制 Break Constraint / Add Constrained Bodies；模拟开关 Enable/Disable Simulation；过渡到布娃娃用 Physics Blend Weight 累积。爆炸、抓取、载具漂移、绳桥全在这套节点里。

**碰撞查询**（Collision 分类（83 子项））——Box/Capsule/Sphere 三形状 × Overlap（Actors/Components/With Orientation）× Trace（By Channel/By Profile/For Objects）矩阵 + Break Hit Result 拆命中信息 + Can Character Step Up / Move Ignore 系列控制通行——命中判定、视线遮挡、范围伤害、可攀爬判定的无代码做法。

**AI 行为**（AI（38 子项）+ Blackboard（12）+ EQS）——AI MoveTo 移动 + Get/Set Blackboard 变量读写记忆 + EQS 环境查询选点 + Get Focal Point 控制注视——巡逻/追击/逃跑最小闭环；复杂决策下沉行为树资产，蓝图只做感知响应（配 GameplayDebuggerEditor 实时可视调试）。

**输入响应**（Input 分类（108 子项））——Enhanced Input 体系：Add Mapping Context 按状态切换输入映射（走路/开车/菜单），Break Input Action Value 拆动作值，Create Dynamic/Linked Value Input 动态构造输入值（运行时生成按键绑定）；另有 Create Root Motion Source 等高级入口。一套映射通吃键鼠/手柄/触屏。

**多人判定**（Networking 分类（14 子项））——Has Authority / Is Server / Is Dedicated Server 分支权威逻辑，Get Local/Remote Role 判断角色，Set Replicates / Set Replicate Movement 开复制，Set Net Dormancy / Flush Net Dormancy / Force Net Update 管休眠与刷新，Tear Off 断联——蓝图多人游戏的全部开关，一眼看清"谁有权改什么"。

**特效驱动**（Niagara 分类（177 子项，第一梯队））——Get/Set 全类型参数（Bool/Float/Int/Color/变量）、Parameter Collection 实例与覆盖、Set Desired Age / Advance Simulation by Time 手动步进（配合录屏/逐帧分析）、Get All Emitters / Data Interface 深入发射器内部——不止调特效，还能当 GPU 计算的参数面板。

**相机与过场**（Camera（121）+ Cinematics（9））——Activate Camera 系（含 Camera System/Rig 分层叠加激活）、Deproject Screen to World 屏幕转世界（拾取/瞄准线基础）、Get Aim Dir 拿瞄准方向、Blend Camera Evaluation Data 混合相机求值；Cinematics 分类预测位姿（Predict World Transform at Time）做时间轴精确演出。

**标签驱动玩法**（GameplayTags 分类（42 子项））——Does Container Match Tag Query 容器查询、Bind Event Wrapper to Gameplay Tag Changed 标签变化事件、Get All Actors Of Class Matching Tag Query 按查询拉 Actor——用标签替代字符串/枚举做状态标记，改配置不改代码。

**技能系统（GAS）**（GameplayAbilities（13）+ GameplayEffects/Attributes 分类）——Give Ability / Clear Ability / Find All Abilities with Tags 装卸技能，Input Confirm/Cancel 处理确认流，配 Effect/Attribute 分类节点做数值与状态——ARPG 技能系统的蓝图操作面。

**声音与音乐**（Audio 分类（79 子项））——Create Sound 2D / Reverb Effect 开关、Sound Mix Modifiers 覆盖、Envelope Following 拿包络做视觉反馈、Bus/Bus sends 路由、Bounce 导出渲染——游戏内混音面板的节点形态（上层由 MetaSound 插件接管 DSP 图）。

**动画事件与程序化动画**（Animation 分类（140 子项））——Bind to Animation Started/Finished/Event 生命周期事件、Control Rig Layer 运行时驱动绑定层、Add Socket / Add Node Asset Override 动态改装、Calculate Direction 算移动方向供混合空间用——动画蓝图之外的事件/参数通道。

**智能对象（Smart Objects）**（SmartObject 分类（57 子项））——Add Smart Object / Find Smart Objects in Targeting Request / Add Tag to Slot——把世界里的椅子/工位/掩体登记为"可被 AI 预约使用的资源"，配 StateTree 做占用与排队：环境 AI 交互的标准基建。

**样条与程序化路径**（Spline 分类（97 子项））——Add Spline Point at Index / Convert Spline to Poly Line / Divide Spline into Polyline Recursive——道路中心线、巡逻路径、轨道镜头、河流走向的统一做法：样条定义 + 采样离散化。

**程序化网格构建**（StaticMesh 分类（33 子项））——Create Static Mesh Description / Build from Static Mesh Descriptions / Begin-Finish Assembly Build——蓝图层直接组装静态网格资产（配合 GeometryScripting 插件的几何函数库）：批量化生成道具变体的资产级管线。

**表演采集（Take Recorder）**（TakeRecorder 分类（75 子项））——Add Source for Actor / Compute Next Take Number / Find Takes / Cancel Recording——把运行时表演（动画/音频/粒子状态）录制成 Take 资产再入 Sequencer：虚拟摄制与动作捕捉的录制面。

### 2.2 全分类的功能域覆盖（关键词归纳）

- **动画/骨骼/Rig**：85 个分类，如 ActorMotion, AnimDatabase, AnimGen, AnimModifier, AnimNext, AnimNotify, Animation, AnimationAsset…
- **UI/UMG/控件**：58 个分类，如 ActivatableWidget, ActivatableWidgetContainer, ActivatableWidgetStack, AnimtoTexture, AudioWidgets, BaseButtonGroup, Button, CanvasPanel…
- **物理/碰撞/破坏**：20 个分类，如 Buoyancy, CameraCollision, Chaos, ChaosMover, ChaosPhysics, ChaosVisualDebugger, Collision, Constraint…
- **AI/导航/行为**：9 个分类，如 AI, Behavior, Blackboard, Crowd, EQS, GameplayBehavior, Navigation, Targeting…
- **渲染/材质/贴图**：23 个分类，如 AnimtoTexture, CanvasRenderTarget2D, Lighting, Lights, Material, MaterialDesigner, MaterialEditing, Materials…
- **音频**：48 个分类，如 Audio, AudioAnalysis, AudioAnalyzer, AudioAssetUserDataTags, AudioCapture, AudioComponentGroup, AudioDelegates, AudioEngineSubsystems…
- **Sequencer/影视/虚拟制片**：37 个分类，如 Camera, CameraAnimation, CameraCalibrationMetadata, CameraCollision, CameraDirector, CameraFades, CameraLensEffect, CameraModifier…
- **特效 Niagara**：9 个分类，如 FXConverterUtilities, Niagara, NiagaraActor, NiagaraBaker, NiagaraDataChannel, NiagaraSimCache, NiagaraToolset, ParticleSystem…
- **网络/多人/在线**：15 个分类，如 ControlRigReplay, IOSReplayKit, MultiUserTakes, MultiWorld, Multi_UserClient, Multi_UserPresence, Multi_UserRevisionControl, Multi_UserSourceControl…
- **输入/设备/XR**：15 个分类，如 CommonInputSubsystem, EnhancedInput, Input, InputDevices, Inputs, MIDIDeviceInputController, OpenXR, PixelStreaming2Input…
- **玩法能力系统**：35 个分类，如 ARGameplay, Abilities, Ability, AnimationAttributes, AssetTags, Attribute, AttributeData, Attributes…
- **编辑器脚本/资产工具**：48 个分类，如 AnimationAsset, AnimationEditorExtensions, AssetData, AssetImportData, AssetImportTask, AssetManager, AssetRegistry, AssetTags…
- **数学/通用工具库**：24 个分类，如 ARSettings, AddMathExpression, ControlRotation, DMXPixelMapping, GenericArchiveDeviceSettings, Guid, GuidConverterTest, InterchangeSettings…

### 2.3 节点详情页抽样（叶级，18 个）

最后一层叶子——**节点详情页**抽样 18 个（跨 AI/碰撞/标签/工具/游戏/物理/输入/网络/Niagara/音频/网格 11 个分类）。节点页格式高度统一：Navigation + **Inputs/Outputs 引脚表**（类型 + 引脚名 + 逐引脚悬浮提示），页均不到 2.5KB。

- **"Target is X"是 BP→C++ 的溯源锚点**：节点页描述的第二行几乎总在声明宿主——Box Trace By Channel →*"Target is Kismet System Library"*（即 UKismetSystemLibrary）、Add Impulse →*"Target is Primitive Component"*、Add Mapping Context →*"Target is Enhanced Input Subsystem Interface"*、Clear Focus →*"Target is AIController"*。想知道一个蓝图节点背后的 C++ 函数在哪，节点页第一屏就有答案。
- **逐引脚有独立说明**：引脚表的第二列携带 tooltip 原文（如 Box Trace 的 Start 引脚：*"Start of line segment."*；Add Mapping Context 的 Mapping Context：*"A set of key to action mappings to apply to this player"*）——比编辑器悬浮提示更完整的参数文档。
- 15/18 抽样节点带描述；**少数"子目录"页面混在节点层**（Utilities/Array、Game/Damage 实为更深一级的分类目录）——蓝图目录树实际有 3 层以上，14,613 个子条目里目录页与节点页混编。
- 异步节点形态可见：Async Load Asset 页只有 Inputs+Outputs 而无"Target is"——它挂的是潜在节点（Latent action）而非某库函数。

### 2.4 节点宿主分布（Target is 统计）

用节点页的 "Target is X" 行做宿主普查（BP→C++ 暴露树的量化）。当前样本 1296 个节点页（覆盖分类：Utilities 91、Physics 91、Game 88、Collision 66、Animation 64、Spline 64、TakeRecorder 63、MovieRenderPipeline 63、Effector 63、Cloner 63、DrawDebugLibrary 63、Mover 63、SmartObject 57、GameplayTags 42、LevelSequence 39、AI 38、Input 34、Niagara 34、Camera 34、Audio 34、Widget 34、StaticMesh 33、Sequencer 19、Material 15、Networking 14、StateTree 14、Landscape 9、SkeletalMesh 4；其中 100 个为目录页无宿主，1160 个带 Target 声明）：

| C++ 宿主 | 节点数 | C++ 宿主 | 节点数 |
|---|---|---|---|
| Kismet System Library | 84 | Audio Capture Blueprint Library | 2 |
| Gameplay Statics | 66 | Blueprint Camera Evaluation Data Function Library | 2 |
| Spline Component | 64 | Mock Root Motion Component | 2 |
| Draw Debug Library | 63 | Controller | 2 |
| Primitive Component | 61 | Blueprint Camera Context Data Table Function Library | 2 |
| Take Recorder Subsystem | 41 | Deformable Constraints Component | 2 |
| Level Sequence Shot Meta Data Library | 35 | Blackboard Asset Provider | 2 |
| Static Mesh | 30 | Deformable Collisions Component | 2 |
| Blueprint Gameplay Tag Library | 27 | Sky Atmosphere Component | 2 |
| Movie Pipeline Blueprint Library | 27 | Geometry Collection Component | 2 |
| Niagara Particle System Component | 25 | Game Maps Settings | 2 |
| Skeletal Mesh Component | 24 | Deformable Tetrahedral Component | 2 |
| Smart Object Blueprint Function Library | 23 | Scene Component | 2 |
| Mover Component | 23 | State Tree Editor Data | 2 |
| Smart Object Subsystem | 19 | CEEffector Cull Mode | 2 |
| Actor | 18 | Movie Scene Bound Object Proxy | 2 |
| Movement Utils | 17 | Gameplay Interaction Smart Object Behavior Definition | 2 |
| CEEffector Force Effect | 16 | State Tree Node Blueprint Base | 2 |
| Game Mode Base | 13 | Anim Sequence | 2 |
| Material Validation Library | 13 | CEEffector Bound Type | 2 |
| CECloner Displacement Extension | 12 | Movie Pipeline Primary Config | 2 |
| AIBlueprint Helper Library | 11 | Animation Asset | 2 |
| Motion Design Effector Component | 11 | Skinned Asset | 2 |
| Motion Design Cloner Component | 11 | CEEffector Box Type | 2 |
| Smart Object Definition | 10 | CEEffector Sphere Type | 2 |
| Widget | 9 | Multi Anim Asset | 2 |
| CECloner Collision Extension | 9 | CEEffector Offset Mode | 2 |
| AIController | 8 | Animation Warping Library | 2 |
| Take Recorder Blueprint Library | 8 | Widget Animation | 2 |
| Anim Instance | 8 | Take Recorder Sources | 2 |
| Game Mode | 7 | CECloner Progress Extension | 2 |
| Movie Pipeline Editor Blueprint Library | 7 | Anim Single Node Instance | 2 |
| Gameplay Cameras Player Camera Manager | 6 | CEEffector Push Mode | 2 |
| Widget Blueprint Library | 6 | Metahuman Mass Crowd Actor Blueprint Interface | 2 |
| Level Streaming | 6 | CECloner Range Extension | 2 |
| Gameplay Tag Asset Interface | 6 | Pawn | 1 |
| Movie Pipeline Executor Base | 6 | Gameplay State Tree Blueprint Function Library | 1 |
| CECloner Texture Extension | 6 | Water Body Component | 1 |
| CEEffector Procedural Mode | 6 | Parametric Movement Component | 1 |
| Niagara Function Library | 5 | Horizontal Box | 1 |
| Enhanced Input Subsystem Interface | 5 | Player Input | 1 |
| Player Camera Manager | 5 | Overlay | 1 |
| Ability System Blueprint Library | 5 | Player Controller | 1 |
| Movie Pipeline Executor Job | 5 | Uniform Grid Panel | 1 |
| Movie Pipeline Config Base | 5 | Niagara Clipboard Editor Scripting Utilities | 1 |
| CECloner Constraint Extension | 5 | Text Box | 1 |
| CEEffector Delay Effect | 5 | Net Push Model Helpers | 1 |
| CECloner Mesh Renderer Extension | 5 | Widget Preview | 1 |
| Animated Sparse Volume Texture Controller | 5 | Common Widget Carousel | 1 |
| Avoidance Manager | 4 | Check Box | 1 |
| Enhanced Input Library | 4 | Rich Text Block | 1 |
| Gameplay Camera Component Base | 4 | Camera Component | 1 |
| Niagara Parameter Collection Instance | 4 | Cine Camera Actor | 1 |
| Blueprint Camera Variable Table Function Library | 4 | Editable Text | 1 |
| Sound Wave Timecode Utils | 4 | Editable Text (Multi-Line) | 1 |
| Physics Spring Component | 4 | Text Box (Multi-Line) | 1 |
| Movie Pipeline Executor Shot | 4 | Scroll Box | 1 |
| State Tree Task Blueprint Base | 4 | Input Key Selector | 1 |
| Skeletal Mesh | 4 | Physics Thread Library | 1 |
| Level Sequence | 4 | Ability System Component | 1 |
| SequencerTrackInstance | 4 | VPViewport Tickable Actor Base | 1 |
| Takes Core Blueprint Library | 4 | Physics | 1 |
| Mover Simulation | 4 | Geometry Collection Actor | 1 |
| Character Mover Component | 4 | Deformable Solver Component | 1 |
| Chaos Mover Simulation | 4 | UDIMTexture Function Library | 1 |
| Modify Curve Anim Library | 4 | Landscape Proxy | 1 |
| CECloner Step Extension | 4 | Animation Modifiers Asset User Data | 1 |
| Movie Pipeline | 4 | Material Validation Group | 1 |
| Smart Object Component | 4 | Movie Pipeline Setting | 1 |
| Mover Data Model Blueprint Library | 4 | Motion Design Cloner Actor | 1 |
| CECloner Lifetime Extension | 4 | Landscape Heightfield Collision Component | 1 |
| Gameplay Camera System Component | 3 | Landscape Blueprint Brush Base | 1 |
| Audio Mixer Blueprint Library | 3 | Ava Shape Actor | 1 |
| Simple Audio Encoder | 3 | Anim Montage | 1 |
| Blueprint Camera Pose Function Library | 3 | Air Movement Utils | 1 |
| Sound Wave | 3 | MoviePipeline Runtime Subsystem | 1 |
| Kismet Math Library | 3 | Motion Design Effector Actor | 1 |
| Deformable Physics Component | 3 | Water Movement Utils | 1 |
| Nanite Assembly Skeletal Mesh Builder | 3 | CEEffector Extension Base | 1 |
| Animation Blueprint Library | 3 | Character | 1 |
| Nanite Assembly Static Mesh Builder | 3 | Gameplay Ability | 1 |
| Landscape | 3 | CECloner Effector Extension | 1 |
| User Widget | 3 | Take Recorder Actor Source | 1 |
| Take Recorder | 3 | CECloner Extension Base | 1 |
| Ground Movement Utils | 3 | CEEffector Plane Type | 1 |
| CEEffector Radial Type | 3 | Movie Pipeline Python Host Executor | 1 |
| CEEffector Step Mode | 3 | Proxy Table Function Library | 1 |
| Raw Anim Sequence Track Extensions | 3 | CEEffector Target Mode | 1 |
| CEEffector Torus Type | 3 | Base Movement Mode Transition | 1 |
| Grid Panel | 2 | | |

**宿主的模块归属**（把 78 个宿主类名反查回引擎模块/插件）：**Engine 仍是最大承接方**（扩容样本中约六成），插件生态承接约两成（Niagara/TakeRecorder/Mover/SmartObjects 系为主），其余分给 GameplayTags/UMG/AIModule/Splines 等专项模块。蓝图的动作面高度依赖 Engine 这个“万能门户”+ 各域自己的插件。

解读（1,296 节点/28 分类样本）：**两种宿主形态平分秋色——函数库与组件/对象**。库侧：Kismet System Library 84、Gameplay Statics 66、Draw Debug Library 63、Level Sequence Shot Meta Data Library 35；对象侧：Spline Component 64、Primitive Component 61、Take Recorder Subsystem 41、Static Mesh 30、Niagara Particle System Component 25。**“领域库+领域对象”配对在每个域成立**：GameplayTags=库 27+接口 6、Niagara=组件 25+库 5、Game=Game Mode Base 13+Level Streaming 6+GAS 库 5、AI=AIController 8+辅助库 11。全部 1,160 个带声明的节点仅由 179 个 C++ 宿主承接（Top3 占 18%——扩容后长尾更明显：门户类仍集中，但各域专属宿主大量涌现）——蓝图的动作面在 C++ 侧高度集中于少数“门户类”。

### 2.5 蓝图动词词表（零网络分析）

从 889 个分类页的子条目名中提取**蓝图动词词表**（11,595 个截断子条目、去重 10,637 个节点名）——这是蓝图"词汇表"的全貌，无需再抓任何页面。**Get 一个动词就占 3,692 个节点（35%）**，加 Set 1,404（13%）——蓝图 API 近半是"读+写"：它本质上是一个巨大的属性访问器网络。

| 动词 | 节点数 | 动词 | 节点数 | 动词 | 节点数 |
|---|---|---|---|---|---|
| Get | 3692 | Clear | 91 | Start | 37 |
| Set | 1404 | Make | 64 | Delete | 36 |
| Is | 448 | Stop | 59 | Read | 36 |
| Add | 445 | Reset | 57 | Frame | 36 |
| On | 327 | Apply | 56 | Database | 35 |
| Remove | 240 | Convert | 51 | Assert | 35 |
| Create | 194 | Update | 44 | Niagara | 34 |
| Find | 150 | Load | 44 | Enable | 34 |
| Draw | 108 | Can | 41 | Send | 34 |
| Has | 103 | Request | 38 | Play | 34 |

- **读：写 ≈ 3:2**——Get 系 3,859 个（36%）vs Set/Add/Create 系 2,310 个（21%）：蓝图暴露的"查询面"比"操作面"更大，这是"可观测优先于可控"的设计哲学
- **Is/Has/Can 判定面占 5%**（631 个）——布尔判断是蓝图的第三大类动词，配合 Branch 节点构成流程控制的基本单元
- **事件面仅 3%**（364 个 On*/Bind*）——事件节点虽少但每个都关联一个 Delegate（Python 侧 618 个委托类型的 BP 端对应）
- **跨分类重名 589 个**——Top：Event（14 分类）、Is Valid（12）、Stop（11）、Reset（10）：通用操作在不同域有同名节点（各域的 Stop/Reset/Play），它们是"领域方言"中的"共同词汇"
- 词汇长尾极长：Top 30 动词覆盖 72%，其余 28% 由数百个领域专用动词分食（Niagara 34 个、Database 35 个、Frame 36 个…）
- **蓝图词表 ≈ 自然语言子集**：Get/Set/Add/Remove/Is/Can/On/Find/Play/Stop 构成一个约 30 词的"迷你语言"——蓝图可读性高的根本原因

### 2.6 结构体命名模式（零网络分析）

C++ 类的前缀/后缀已分析（1.2 节），现在看另一半——**10,671 个 Structs 的命名模式**（零网络分析）。F 前缀占 **85%**（9,090 个），T 模板 10%，其余 5% 零星——结构体命名比类更整齐（没有 U/A 反射前缀的分裂）。

- **后缀分布极其分散**：Top 1 后缀 SerializerConfig 仅 70 个（0.7%）——与类的 Top 后缀 Component 199 个（1.7%）相比更散，结构体没有一个"统帅型"后缀
- **数据描述类后缀合计 23%**（Params/Desc/Info/Data/Config/Settings/Init）：四分之一的结构体是"纯数据描述体"——印证了 1.2.4 节"结构体=数据编排系统"的定性
- **各域有鲜明的结构体方言**：网络域的 SerializerConfig/SerializerInfo（序列化描述符密集，对应 Iris 新复制系统的状态描述符设计）；物理域的 DataWrapper（21 个，Chaos 解算器数据包装）；Sequencer 域的 KeyStruct/ComponentData/PropertyTraits（轨道键值与属性求值）；AI 域的 DecoratorMemory/TaskMemory（行为树节点记忆体）——结构体后缀就是各域的"设计签名"
- **序列化/版本相关结构体极多**：SerializerConfig 70 + SerializerInfo 65 + ObjectVersion 37 + CustomVersion 16 = 188 个——引擎的版本管理与数据迁移占了结构体的近 2%
- **委托签名类结构体 150 个**（Delegate/Signature/Handler 后缀）——BP 动态委托在 C++ 侧以结构体形式存在，与 Python 侧的 618 个 Delegate 类型形成对应
- **结构体的 Remarks 列显示"100% 覆盖"是假象**——多数 Remarks 只写了类型定义语法（如 "( FTransformCollection )"）而非实际说明——这是文档质量的又一个元发现：**覆盖率和信息量不是同一件事**

### 2.7 接口与枚举的命名模式（零网络分析）

1,709 个接口的 **100% 以 I 开头**——接口是全引擎命名最整齐的类别。但后缀分布极散（Top 1 EditorModule 仅 29 个），说明接口命名没有统一模板。

- **接口/类比值=“扩展开放度”**——Developer 组的子域普遍高于 Runtime 组：平台与设备管理 177%、媒体 68%、资产管线 60%、分析前端 56%、属性定制 52%——这些是“邀请你注入实现”的域；而物理 3%、AI 5%、渲染 7%、游戏框架 8%——这些是“封闭实现、只暴露调用”的域。**扩展开放度与反射密度谱（1.2.3）形成正交维度**：高反射+低接口（Engine/AIModule）=“给设计师用但不给程序员扩展”；高接口+低反射（平台/管线）=“给程序员扩展但设计师不直接碰”。
- **Provider/Handler 模式**：ProfilerProvider 7、DataProvider 5、ProviderInterface 5、EventHandler 5——这些接口后缀标出了引擎的“插件位”：实现 IProfilerProvider 就能接入性能分析后端，实现 IDataProvider 就能注入数据源
- **ModularFeature 7 个**：IModularFeature 是引擎的模块化特性注册机制的入口接口——不常用但关键
- 接口最集中的模块：TraceServices 61、DatasmithCore 59、SequencerCore 47、PropertyEditor 45、InteractiveToolsFramework 44——正好对应 1.2.4 节的“扩展点优先”模块清单（数据交叉验证）

3,778 个枚举的命名揭示了一个令人意外的事实：**EE\* 开头的枚举占 71%**（2,703 个）——这不是“E + 领域词”的预期格式，而是“EE”双 E 前缀（如 EEnvQueryStatus、EExpressionType）。这是因为 Doxygen 会把 E 前缀去掉后取首词，很多枚举的领域词本身以 E 开头（Env/Expression/Editor…），加上前缀 E 就成了 EE。

- **领域专属枚举首词 Top**：EE\*（通用）、EUE\*（引擎全局 371）、EChaos\*（物理 90）、EAudio\*（音频 46）、EERHI\*（渲染 30）、ETrace\*（追踪 27）——这些首词直接标出了“该域有多少种‘模式/状态/开关’需要枚举”
- **各域枚举方言**：物理域 EChaos\* 92 个（Chaos 子系统的模式极多）；游戏框架 EE\* 817 个（Engine 模块的枚举大户）；渲染域 EERHI\* 30 + EERDG\* 17（RHI 和 RDG 的状态/格式枚举）
- **E 前缀占 77%**（2,941/3,778），其余 23% 以 U 开头（390 个）——U 开头的枚举其实是“反射可见的枚举”（UENUM 标注的蓝图可用枚举），它们在文档站被归入 Enums 节但保留了 U 前缀

## 三、Python API：编辑器自动化面（unreal 模块，Experimental）

整站即一个 `unreal` 模块（Sphinx 文档，标题自带 *Unreal Python 5.8 (Experimental)*）。类型面：Class 5,149、Struct 4,106、Enum 1,776、Delegate 618、Native 26，合计 11675 个类型页。

常用入口类（均已核验存在）：`unreal.EditorAssetLibrary`（资产增删改查）、`unreal.AssetEditorSubsystem`、`unreal.LevelEditorSubsystem`、`unreal.UnrealEditorSubsystem`、`unreal.EditorLevelLibrary`（旧入口）、`unreal.AssetRegistryHelpers`、`unreal.MaterialEditingLibrary`、`unreal.StaticMeshEditorSubsystem` / `SkeletalMeshEditorSubsystem`、`unreal.EditorUtilityLibrary`、`unreal.SystemLibrary`。

### 3.1 八个典型自动化配方（代码行为示意片段，以官方类名为准）

**资产批量治理**（unreal.EditorAssetLibrary + unreal.AssetRegistryHelpers）——按目录/类/标签筛资产，批量改名/迁移/设标签；做命名规范 CI 卡点。

```python
assets = unreal.EditorAssetLibrary.list_assets("/Game/Props", recursive=True)
```

**引用链分析**（unreal.AssetRegistryHelpers.get_asset_registry()）——查谁引用了该资产（删除前安全检查）、生成依赖图谱报表。

```python
refs = reg.get_referencers("/Game/Props/Table.SM_Table", unreal.AssetRegistryDependencyOptions())
```

**关卡批量操作**（unreal.EditorLevelLibrary / unreal.LevelEditorSubsystem）——遍历 Actor 批量替换/移动/改属性；世界分区地块处理。

```python
actors = unreal.EditorLevelLibrary.get_all_level_actors()
```

**材质批量改写**（unreal.MaterialEditingLibrary）——遍历材质图节点改参数/换贴图、批量生成材质实例。

```python
unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(mic, "Rough", 0.5)
```

**骨骼网格批处理**（unreal.SkeletalMeshEditorSubsystem）——批量设置 LOD/骨骼/物理资产元数据，动画资产管线预处理。

```python
unreal.SkeletalMeshEditorSubsystem.set_bone_category_name(mesh, "hand", "UpperBody")
```

**Sequencer 自动化**（unreal.LevelSequence + Sequencer Scripting 插件）——按表格批量生成镜头序列/绑定轨道。

```python
seq = unreal.load_asset("/Game/Cine/Intro"); bindings = seq.get_bindings()
```

**构建前校验钩子**（unreal.EditorLoadingAndSavingUtils / SystemLibrary）——CI 中以 Commandlet 跑 Python：保存全部/校验脏资产/输出报告。

```python
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
```

**数据表驱动生成**（unreal.DataTable / EditorAssetLibrary）——读 CSV/DataTable 驱动批量生成蓝图类资产并填参。

```python
rows = unreal.DataTableFunctionLibrary.get_data_table_row_names(dt)
```

**边界**：仅编辑器进程内可用，打包后的游戏不含 Python 运行时；逐帧/实时逻辑不适用（那是 C++/蓝图的地盘）。

### 3.2 Python 面的形态：数据说了什么

对 5,149 个类的名字做主题前缀统计，能看出 Python 面的倾斜：

| 前缀群 | 类数 | 前缀群 | 类数 |
|---|---|---|---|
| Material** | 470 | Audio** | 50 |
| Anim** | 235 | Nav** | 44 |
| Niagara** | 147 | Control** | 38 |
| Editor** | 71 | Cam** | 37 |
| Meta** | 66 | AI** | 35 |
| Data** | 57 | Gameplay** | 35 |
| Level** | 52 | | |

- Material* 是最大的主题群（470 类）——材质图的程序化读写面在 Python 里最厚，材质管线自动化是 Python API 的第一强项
- 196 个 *Library* 函数库类 + 62 个 *Subsystem 结尾类——C++ 侧的"函数库暴露模式"与"子系统服务模式"在 Python 面原样复现
- 618 个 Delegate 类型是 C++ 动态委托的直接映射（ActorBeginOverlapSignature / ActorComponentActivatedSignature 等）——意味着 Python 脚本也能挂引擎事件回调（编辑器场景下做监听式自动化）
- 4,106 个 Struct 让"传参"几乎都有类型化载体（Vector/Transform/各资产导入设置），写脚本不必拼字典

### 3.3 主力类成员数排行（28 类叶级抽样）

Python 侧同样下探一层：逐页抓取 28 个主力类/资产类的类型页，统计成员数（dt 条目，含方法与属性）。排行揭示了编辑器脚本面的真实形状：

| unreal 类 | 成员数* | 基类 | 备注 |
|---|---|---|---|
| SystemLibrary | 273 | BlueprintFunctionLibrary | box/capsule trace 全家桶 + timer/delay/事务 + draw_debug |
| Actor | 197 | Object | spawn/attach/input/bounds/标签/网络休眠全套 |
| GameplayStatics | 147 | BlueprintFunctionLibrary | 伤害/音效/玩家/存档/弹道预测/屏幕投影 |
| UserWidget | 115 | Widget | 动画绑定 + 全套输入/拖拽/焦点事件 |
| PlayerController | 110 | Controller | 输入轴/相机震动/点击命中/鼠标投影 |
| NiagaraComponent | 98 | FXSystemComponent | get/set_variable 全类型 + sim cache/期望年龄 |
| MaterialEditingLibrary | 77 | BlueprintFunctionLibrary | 材质图程序化编辑主力（建/连/删表达式） |
| StaticMeshEditorSubsystem | 64 | EditorSubsystem | LOD/碰撞/UV/Section/Nanite/合并代理 |
| Material | 57 | MaterialInterface | 多为一排 used_with_* 用途属性而非方法 |
| SkeletalMesh | 48 | SkinnedAsset | 骨骼/socket/morph/布料/物理资产 |
| Character | 47 | Pawn | 跳跃/蹲伏/Montage/根运动 + 事件 |
| EditorAssetLibrary | 39 | BlueprintFunctionLibrary | checkout/delete/duplicate/save/list_assets |
| ActorComponent | 39 | Object | activate/tick/标签/复制/事件 |
| EditorLevelLibrary | 37 | BlueprintFunctionLibrary | （旧入口）actor 选择/合并/试飞/pilot |
| SkeletalMeshEditorSubsystem | 37 | EditorSubsystem | LOD/socket/物理资产/截面属性 |
| StaticMesh | 36 | StreamableRenderAsset | socket/材质槽/Nanite 统计/描述构建 |
| LevelEditorSubsystem | 36 | EditorSubsystem | 关卡加载保存/视口相机/PIE/编辑器事件 |
| AssetRegistryHelpers | 20 | Object | 资产数据/过滤器/蓝图类检索 |
| EditorUtilityLibrary | 17 | BlueprintFunctionLibrary | 选中集/内容浏览器路径/选择变换 |
| SoundWave | 16 | SoundBase | 字幕/cue 点/循环区/压缩类型 |
| DataTable | 15 | Object | CSV/JSON 双向导入导出 |
| Landscape | 9 | LandscapeProxy | 编辑层/草开关/渲染高度图权重图 |
| LevelSequence | 7 | MovieSceneSequence | 仅元数据操作（序列本体走 Sequencer Scripting 插件） |
| UnrealEditorSubsystem | 7 | EditorSubsystem | 编辑器/游戏世界获取 + 屏幕世界互投 |
| MaterialInstanceConstant | 5 | MaterialInstance | 标量/纹理/向量参数读写 |
| AnimSequence | 4 | AnimSequenceBase | 仅重定向源资产操作 |
| AssetEditorSubsystem | 3 | EditorSubsystem | 打开/关闭资产编辑器 + 调试委托 |
| World | 2 | Object | 仅 data layer manager 与 world settings——运行时核心在编辑器脚本侧是薄壳 |

（*dt 条目计数，含方法与属性；资产类以属性为主，函数库/子系统类以方法为主。）

- **SystemLibrary 以 273 个成员居首**——Box/Capsule/Sphere 的 Trace/Overlap 全家桶 + Timer/Delay + DrawDebug 全在里面：它就是"蓝图工具箱"的 Python 镜像。
- **Actor 197 / GameplayStatics 147**——运行时操作面在编辑器脚本里依然可用（修改场景里的 Actor 不受"仅编辑器"限制，只是不能在打包后跑）。
- **World 只有 2 个成员**（get_data_layer_manager / get_world_settings）——运行时最核心的对象在编辑器脚本侧是薄壳：操作世界要走 LevelEditorSubsystem（36）与 EditorLevelLibrary（37）。这是"运行时面 ≠ 脚本面"的最好例证。
- **序列资产是 Python 的洼地**：LevelSequence 7 个、AnimSequence 4 个——官方把序列/动画脚本化的重担交给了专用插件（Sequencer Scripting / 各 EditorSubsystem），核心类只留元数据操作。
- Material 的 57 个"成员"大半是 used_with_* 用途属性而非方法——资产类的 Python 面以**属性直读写**为主，函数库类（*Library/*Subsystem）才是动作面。
- editor 侧双子星：MaterialEditingLibrary 77（建/连/删表达式全套）+ StaticMeshEditorSubsystem 64（LOD/碰撞/UV/Nanite）——材质与网格是脚本化自动化投入产出比最高的两个领域。

### 3.4 Python 动作类全量普查（250 个 Library/Subsystem）

把 3.3 节的 28 类抽样升级为**全量普查**：Python 侧 5,149 个类中所有以 *Library / *Subsystem 结尾的 250 个动作类逐页测完。结果：217 个有效页面、28 个 0 成员（几乎全是抽象基类：Subsystem/EngineSubsystem/EditorSubsystem/WorldSubsystem 等——模板类没有可调成员）、**5 个 404**（SynthesisUtilitiesBlueprintLibrary/BehaviorTreeLibrary/BlueprintMaterialLibrary/BlueprintPathsLibrary/CameraLibrary——引擎注册了暴露名册但文档站没生成页面，属于 Python 暴露名册与实际页面的已知差集）。

| unreal 动作类 | 成员数 | unreal 动作类 | 成员数 | unreal 动作类 | 成员数 |
|---|---|---|---|---|---|
| MathLibrary | 705 | PluginBlueprintLibrary | 13 | TurnBasedLibrary | 4 |
| SystemLibrary | 273 | StringTableLibrary | 13 | TypedElementHandleLibrary | 4 |
| UsdConversionLibrary | 166 | UAFRigVMAssetLibrary | 13 | UserObjectListEntryLibrary | 4 |
| ControlRigSequencerLibrary | 131 | VisualLoggerLibrary | 13 | ImportSubsystem | 4 |
| AnimationLibrary | 119 | BlueprintMaterialTextureNodesBPLibrary | 12 | AssetEditorSubsystem | 3 |
| BlueprintSpringMathLibrary | 103 | CachedAnimDataLibrary | 12 | AndroidFileServerBPLibrary | 3 |
| BlueprintEditorLibrary | 80 | DataflowBlueprintLibrary | 12 | AnimNodeControlRigLibrary | 3 |
| StringLibrary | 80 | GlobalConfigurationDataBlueprintLibrary | 12 | AnimNodeRigidBodyLibrary | 3 |
| MaterialEditingLibrary | 77 | NamingTokensEngineSubsystem | 12 | EngineCameraAnimationFunctionLibrary | 3 |
| StaticMeshEditorSubsystem | 64 | AnimGraphLibrary | 11 | HealthSnapshotBlueprintLibrary | 3 |
| LevelSequenceEditorBlueprintLibrary | 62 | ControlRigBlueprintLibrary | 11 | JsonObjectGraphFunctionLibrary | 3 |
| TakeRecorderSubsystem | 58 | PlatformLibrary | 11 | LayersBlueprintLibrary | 3 |
| ConstraintInstanceBlueprintLibrary | 56 | WorldPartitionBlueprintLibrary | 11 | MediaLibrary | 3 |
| VariantManagerLibrary | 56 | AnimationStateMachineLibrary | 10 | MeshVertexPainterLibrary | 3 |
| InputLibrary | 54 | ProceduralMeshLibrary | 10 | SequenceRecorderLibrary | 3 |
| TextLibrary | 52 | InputDeviceSubsystem | 10 | UAnimNotifyStateMachineInspectionLibrary | 3 |
| WidgetLibrary | 52 | InterchangeEditorScriptLibrary | 9 | UserListEntryLibrary | 3 |
| DataLayerEditorSubsystem | 52 | PyTestStructLibrary | 9 | MetaSoundCacheSubsystem | 3 |
| LayersSubsystem | 46 | SequenceEvaluatorLibrary | 9 | ViewportStatsSubsystem | 3 |
| NiagaraDataInterfaceArrayFunctionLibrary | 44 | ContentBrowserDataSubsystem | 9 | AchievementLibrary | 2 |
| EditorAssetSubsystem | 43 | MVVMSubsystem | 9 | AndroidPermissionFunctionLibrary | 2 |
| AudioMixerLibrary | 40 | AnimExecutionContextLibrary | 8 | AudioCaptureLibrary | 2 |
| EditorStaticMeshLibrary | 40 | MVVMFontConversionLibrary | 8 | AudioInsightsBlueprintLibrary | 2 |
| EditorAssetLibrary | 39 | MVVMSlateBrushConversionLibrary | 8 | CustomizableObjectEditorFunctionLibrary | 2 |
| LevelSequenceEditorSubsystem | 38 | EditorValidatorSubsystem | 8 | DNAImporterLibrary | 2 |
| EditorLevelLibrary | 37 | GameViewportSubsystem | 8 | FieldNotificationLibrary | 2 |
| SkeletalMeshEditorSubsystem | 37 | MetaSoundEditorSubsystem | 8 | LegacyCameraShakeFunctionLibrary | 2 |
| GameplayTagLibrary | 37 | UnrealEditorSubsystem | 7 | LightWeightInstanceBlueprintFunctionLibrary | 2 |
| LevelEditorSubsystem | 36 | ConstraintsScriptingLibrary | 7 | NiagaraSimCacheFunctionLibrary | 2 |
| AutomationLibrary | 35 | EditorFilterLibrary | 7 | NiagaraWaterFunctionLibrary | 2 |
| LevelSequenceShotMetaDataLibrary | 35 | EnhancedInputLibrary | 7 | ResonanceAudioBlueprintFunctionLibrary | 2 |
| LiveLinkBlueprintLibrary | 35 | GuidLibrary | 7 | RetargetProfileLibrary | 2 |
| EditorActorSubsystem | 35 | ImportanceSamplingLibrary | 7 | SkeletalMergingLibrary | 2 |
| RenderingLibrary | 34 | KismetArrayLibrary | 7 | UAnimNotifyMirrorInspectionLibrary | 2 |
| CollectionManagerSubsystem | 31 | MirrorAnimLibrary | 7 | UserWidgetFunctionLibrary | 2 |
| EnhancedInputEditorSubsystem | 31 | ModifyCurveAnimLibrary | 7 | WidgetAnimationHandleFunctionLibrary | 2 |
| EnhancedInputLocalPlayerSubsystem | 30 | ToolsetLibrary | 7 | WorldPartitionDestructibleInHLODSupportLibrary | 2 |
| AnalyticsLibrary | 29 | UAnimNotifyLibrary | 7 | WorldPartitionHLODBlueprintLibrary | 2 |
| SubobjectDataBlueprintFunctionLibrary | 29 | DatasmithContentLibrary | 6 | CompositeCoreSubsystem | 2 |
| BTFunctionLibrary | 28 | MaterialLibrary | 6 | ConstraintSubsystem | 2 |
| AssetTagsSubsystem | 28 | NiagaraDataChannelLibrary | 6 | LiveLinkDeviceSubsystem | 2 |
| EnhancedInputWorldSubsystem | 28 | PythonScriptLibrary | 6 | MetaSoundOutputSubsystem | 2 |
| MetaSoundBuilderSubsystem | 28 | AudioDeviceNotificationSubsystem | 6 | WorldPartitionSubsystem | 2 |
| DataTableFunctionLibrary | 26 | MetaSoundAssetSubsystem | 6 | AudioCaptureFunctionLibrary | 1 |
| SubobjectDataSubsystem | 25 | ReplaySubsystem | 6 | BatchProcessLibrary | 1 |
| UsdStageEditorLibrary | 24 | BlueprintCameraEvaluationDataFunctionLibrary | 5 | BuiltInDynamicBindingResolverLibrary | 1 |
| WidgetLayoutLibrary | 24 | BlueprintInstancedStructLibrary | 5 | CameraShakeInstanceFunctionLibrary | 1 |
| NiagaraFunctionLibrary | 22 | ChaosVDRuntimeBlueprintLibrary | 5 | ChaosBlueprintLibrary | 1 |
| InputDeviceLibrary | 21 | EditorUtilityDialogLibrary | 5 | ChaosSolverEngineBlueprintLibrary | 1 |
| EditorUtilitySubsystem | 21 | GeometryCollectionLibrary | 5 | CookFunctionLibrary | 1 |
| MVVMEditorSubsystem | 21 | GroomLibrary | 5 | FunctionalTestUtilityLibrary | 1 |
| AssetRegistryHelpers | 20 | MobilePatchingLibrary | 5 | ImageWriteBlueprintLibrary | 1 |
| BlueprintCameraPoseFunctionLibrary | 20 | RigVMFunctionLibrary | 5 | InterchangeTestsBlueprintFunctionLibrary | 1 |
| SlateLibrary | 20 | TypedElementSelectionSetLibrary | 5 | LeaderboardLibrary | 1 |
| TimeManagementLibrary | 20 | EngineCamerasSubsystem | 5 | MVVMBlueprintLibrary | 1 |
| TypedElementListLibrary | 20 | AutomationUtilsBlueprintLibrary | 4 | MVVMConversionLibrary | 1 |
| DataLayerSubsystem | 20 | BlueprintPostProcessSettingsCollectionFunctionLibrary | 4 | ModularSynthLibrary | 1 |
| QuartzSubsystem | 20 | CameraLensEffectInterfaceClassSupportLibrary | 4 | MovieSceneFadeTrackTestLibrary | 1 |
| BlueprintCameraVariableTableFunctionLibrary | 18 | ContentBrowserItemLibrary | 4 | NiagaraBakerFunctionLibrary | 1 |
| WaterSubsystem | 18 | DataflowEditorBlueprintLibrary | 4 | NiagaraDIRigidMeshCollisionFunctionLibrary | 1 |
| EditorUtilityLibrary | 17 | EditorSubsystemBlueprintLibrary | 4 | PaperSpriteLibrary | 1 |
| GooglePADFunctionLibrary | 17 | EngineElementsLibrary | 4 | PhysicsThreadLibrary | 1 |
| TakeRecorderBlueprintLibrary | 17 | LandmassBlueprintFunctionLibrary | 4 | PyTestObjectLibrary | 1 |
| InternationalizationLibrary | 16 | LayeredBoneBlendLibrary | 4 | StateTreeFunctionLibrary | 1 |
| PCGDataFunctionLibrary | 16 | LinkedAnimGraphLibrary | 4 | TransformTrajectoryBlueprintLibrary | 1 |
| PhysicsControlBPLibrary | 16 | LocalizableMessageLibrary | 4 | UAFInjectionLibrary | 1 |
| AIHelperLibrary | 15 | MotionExtractorUtilityLibrary | 4 | UDIMTextureFunctionLibrary | 1 |
| BlueprintGraphPinLibrary | 15 | MusicalTimeFunctionLibrary | 4 | UsdDynamicBindingResolverLibrary | 1 |
| RigVMBlueprintLibrary | 15 | PhysicsObjectBlueprintLibrary | 4 | DataDrivenCVarEngineSubsystem | 1 |
| ConsoleVariablesEditorFunctionLibrary | 14 | ProceduralFoliageEditorLibrary | 4 | MVVMGameSubsystem | 1 |
| SequencePlayerLibrary | 14 | SkeletalControlLibrary | 4 | SlateFXBaseSubsystem | 1 |
| TraceUtilLibrary | 14 | TakesCoreBlueprintLibrary | 4 |  |  |
| EditorSkeletalMeshLibrary | 13 | TileMapLibrary | 4 |  |  |

- **MathLibrary 以 705 个成员登顶**（第二名 SystemLibrary 273 的 2.6 倍）——KismetMathLibrary 的 Python 面：数学工具箱是 unreal 模块里动作最密集的区域，做数值处理脚本几乎绕不开它。
- **两种模式密度相当**：Library 171 个有效类合计 3,479 方法（均值 20）vs Subsystem 45 个合计 830（均值 18）——函数库偏静态工具集、子系统偏有状态服务，但动作面厚度同级。
- **互操作管线厚得惊人**：UsdConversionLibrary 166（USD 转换面）+ ControlRigSequencerLibrary 131 + AnimationLibrary 119 + RigVMBlueprintLibrary 15——程序化动画与 USD 数据管线是 Python 自动化的第二大聚集区（仅次于资产/网格线）。
- **编辑器子系统第一梯队**：StaticMeshEditorSubsystem 64、TakeRecorderSubsystem 58、DataLayerEditorSubsystem 52、LayersSubsystem 46、EditorAssetSubsystem 43、LevelSequenceEditorSubsystem 38、EditorActorSubsystem 35——大世界分区（DataLayer/Layers）与录制/序列高居前列。
- **长尾极长**：171 个有效 Library 里 86 个只有 ≤5 个成员（一半是插件为蓝图暴露的单门面工具函数，Python 侧同样名存实亡）；全体 ≥50 成员的动作类仅 18 个——**Python 动作面高度头部集中**（4,329 个方法中 Top18 类占约四成）。

## 四、三套 API 选型与组合

| 维度 | C++ | Blueprint | Python |
|---|---|---|---|
| 运行环境 | 游戏+编辑器 | 游戏+编辑器 | 仅编辑器 |
| 性能 | 原生 | 有 VM 开销（逐帧逻辑敏感） | 脚本级（不适合逐帧） |
| 适合 | 引擎改造/底层系统/性能热点 | 玩法组装/原型/设计师协作 | 批处理/资产管线/自动化 |
| 入口形态 | 模块+类 | 889 个节点分类 | unreal 模块 11675 个类型 |
| 学习曲线 | 高 | 低 | 低（会 Python 即可） |

**组合模式（工程常态）**：C++ 写能力层（UFUNCTION/UPROPERTY 反射暴露）→ 蓝图组装玩法与调参 → Python 做资产管线与 CI。同一件事的三种做法——给关卡内所有 StaticMesh 设置碰撞：C++ 遍历 `UStaticMeshComponent`；蓝图用 `Static Mesh` 分类设置节点；Python 用 `unreal.LevelEditorSubsystem` 取关卡遍历设置。

### 4.1 同一功能的三层对照表（20 个高频功能）

| 功能 | C++ 侧 | Blueprint 侧 | Python 侧 |
|---|---|---|---|
| **静态网格** | Engine: UStaticMeshComponent / UStaticMesh | Static Mesh（BP 分类） | unreal.StaticMesh / StaticMeshEditorSubsystem |
| **骨骼网格与动画** | Engine: USkeletalMeshComponent；AnimGraphRuntime | Animation（140 子项）/ Skeletal Mesh | unreal.SkeletalMesh* / AnimSequence* / SkeletalMeshEditorSubsystem |
| **材质** | Engine: UMaterial；RenderCore: 顶点工厂 | Materials / Material（BP 节点） | unreal.Material*（470 类最大群）/ MaterialEditingLibrary |
| **物理与破坏** | Chaos / ChaosSolverEngine: UChaosSolver；FieldSystemEngine | Physics（136）/ Chaos / Destruction | unreal.GeometryCollection* / PhysicsUtils（插件） |
| **碰撞查询** | Engine: UPrimitiveComponent；PhysicsCore | Collision（83 子项：Overlap/Trace 全家桶） | unreal.SystemLibrary（Box Trace 等） |
| **特效** | Niagara 插件（引擎外） | Niagara（177 子项） | unreal.Niagara*（147 类） |
| **AI 行为** | AIModule: AAIController/BT/Perception | AI（38）/ Blackboard / Behavior Tree | unreal.AISystem / AIBlueprintHelperLibrary |
| **导航** | NavigationSystem / Navmesh | Navigation / Nav Mesh | unreal.NavigationSystemV1 |
| **输入** | InputCore；EnhancedInput 插件 | Input（108）/ Enhanced Input | unreal.EnhancedInput* |
| **UI** | Slate/SlateCore + UMG: UUserWidget | UMG / Widget 各分类 | unreal.UserWidget / WidgetBlueprint*（配 UMGToolSet 插件） |
| **过场/时间线** | MovieScene/LevelSequence: ULevelSequencePlayer | Sequencer / Level Sequence / Cinematics | unreal.LevelSequence*（配 Sequencer Scripting 插件） |
| **网络复制** | NetCore: UNetDriver；IrisCore（新一代） | Networking（14 子项：Has Authority 等） | （运行时系统，Python 面基本不涉及） |
| **音频** | AudioMixer/SignalProcessing；MetaSound 插件 | Audio（79）/ Meta Sound | unreal.Audio*（50 类）/ Metasound* |
| **地形植被** | Landscape / Foliage | Landscape / Foliage | unreal.Landscape*（31 类） |
| **大规模实体** | MassEntity/MassCore: UMassEntitySubsystem | Mass / Mass Spawner | unreal.MassEntity*（部分） |
| **资产管理** | AssetRegistry: IAssetRegistry | Asset Registry / Asset Manager | unreal.AssetRegistry / AssetRegistryHelpers / EditorAssetLibrary |
| **存档** | Engine: USaveGame（+ SaveGame 插件体系） | SaveGame 分类 | unreal.SaveGame |
| **关卡与流送** | Engine: ULevelStreaming；World Partition（插件组） | Level / Level Streaming / World Partition | unreal.LevelEditorSubsystem / EditorLevelLibrary |
| **编辑器工具** | UnrealEd + EditorSubsystem 模块；Blutility | Editor Utility / Editor Scripting | unreal.UnrealEditorSubsystem / EditorUtilityLibrary（+ Python 本身） |
| **脚本自动化** | （C++ 即本体） | Python 分类（BP 桥） | unreal 模块全体（Python 本体） |

### 4.2 域能力矩阵：四路数据按 19 域合流

把四路数据（引擎模块、蓝图分类、Python 类、官方插件）按 19 个功能域合流成一张能力矩阵，回答"每个域在各暴露层的厚度"。C++ 列是精确计数；BP/Python/插件三列是**启发式归类**（关键词/前缀/官方分类映射，一个条目可能计入多个域），看相对量级而非绝对值。

| 功能域 | C++ 模块 | C++ 条目 | BP 分类* | BP 子项* | Python 类* | 插件 |
|---|---|---|---|---|---|---|
| 核心与运行时基础 | 27 | 10,176 | 12 | 380 | 0 | 0 |
| 游戏框架与玩法 | 13 | 8,965 | 65 | 948 | 110 | 29 |
| 输入与 XR 设备 | 7 | 232 | 23 | 299 | 50 | 22 |
| 渲染与图形 | 20 | 3,567 | 24 | 1,208 | 517 | 26 |
| 物理与碰撞 | 13 | 3,055 | 19 | 537 | 43 | 24 |
| 几何与建模 | 14 | 2,587 | 7 | 199 | 94 | 11 |
| UI 界面 | 11 | 1,864 | 45 | 456 | 22 | 11 |
| 动画与布料 | 9 | 499 | 64 | 1,739 | 300 | 83 |
| Sequencer 与影视虚拟制片 | 12 | 2,178 | 39 | 959 | 281 | 73 |
| 音频 | 18 | 674 | 38 | 474 | 169 | 33 |
| AI 与导航 | 3 | 1,213 | 9 | 102 | 79 | 11 |
| 网络与在线服务 | 41 | 1,365 | 15 | 115 | 0 | 55 |
| 媒体播放 | 4 | 201 | 13 | 89 | 14 | 41 |
| 地形与植被 | 2 | 394 | 12 | 161 | 38 | 4 |
| Mass 实体系统 | 5 | 334 | 3 | 7 | 1 | 0 |
| 资产与内容管线 | 20 | 967 | 25 | 216 | 76 | 22 |
| 遥测与性能分析 | 17 | 229 | 17 | 228 | 0 | 20 |
| 自动化测试 | 3 | 41 | 22 | 166 | 0 | 20 |
| 新兴与实验技术 | 6 | 1,133 | 6 | 490 | 4 | 5 |

（带 * 三列为启发式归类：BP 按分类名关键词、Python 按类名前缀、插件按官方分类映射；一个条目可计入多个域，量级可信、绝对值勿较真。C++ 两列为精确计数。）

- 动画域是"编辑器侧最厚"的域：插件 83 个 + Python 300 类 + BP 1,700+ 子项，但引擎 C++ 模块只有 9 个——动画的重头戏全在插件生态（ControlRig/LiveLink/MLDeformer）
- 网络域正相反：C++ 41 个模块（全引擎域第一）但 Python 面 0 类、BP 仅 15 个分类——纯运行时系统，编辑器/脚本侧天然薄
- 渲染域 C++ 3,567 条 + Python 517 类（Material* 470 为主）——程序化材质是编辑器脚本化的最热门入口
- 游戏框架域四面均衡（C++ 8,965 条 + BP 65 分类 + Python 110 类 + 插件 29 个）——离所有使用者都近，所以每层都有面
- 核心基础域（C++ 10,176 条全引擎第一）在其他三层几乎为零——地基不需要被蓝图直接调用
- 特效（Niagara）不在矩阵中：它是插件而非引擎模块，属于插件生态列的 FX 类（10 个插件），BP 侧 177 子项见第 2 章

## 五、版本口径与 4.27 → 5.8 模块演化（数据差分）

文档站 all_versions 实测支持：**5.8（当前默认）/ 5.7 / 5.6 / 5.5 / 5.4 / 5.3 / 5.2 / 5.1 / 5.0 / 4.27**。本文全部数字基于 5.8。用 4.27 的组页名单与 5.8 差分（4.27 组页经 `application_version=4.27` 参数抓取，与 5.8 同接口同口径），可以量化 UE5 时代引擎模块的演化：

**总量**：引擎模块（三组）4.27 共 419 个 → 5.8 共 494 个（Runtime 183→246、Editor 128→139、Developer 108→109）；插件条目 983→842 是**粒度重组**而非缩水：4.27 的 PluginIndex 把插件子模块（*Editor/*Factory/*Core）也当条目列，5.8 拆成"842 插件 + 1375 插件模块"两层，对比新增名单时要过滤这批假新增/假删除。

**模块入场时间线（四快照点仲裁）**：文档站的版本化 API 快照实际只有**四个独立时点：4.27、5.4、5.6、5.8**。`application_version=5.0` 参数经字节级比对确认返回的是 4.27 快照的逐字节副本（站点从未为 5.0 重建 API 页）——这本身是关于"官方文档覆盖度"的元发现：**UE5.0 的模块面在文档站上不可考**，5.1~5.3 的新模块（如 NNE）只能归入"4.27 之后~5.4 之间"的窗口。因此时间线按快照窗口标注，不给单点版本归因。

| 入场窗口 | 模块数 (D/E/R) | 代表模块 | 解读 |
|---|---|---|---|
| **≤4.27** | 384 (88/122/174) | Engine、Core、Slate、UMG、MovieScene、AIModule、Chaos、IrisCore（Iris 早在 4.x 已实验性在册）…… | 78% 的模块是 UE4 时代遗产——UE5 的演进方式是"老模块内部换血"（渲染器重写、物理迁 Chaos）而非另起炉灶 |
| **4.27 → 5.4 窗口** | 40 (7/5/28) | NNE、AudioLinkCore、解码器四件（Opus/Vorbis/Adpcm/Rad）、UniversalObjectLocator、XMPP、Stomp、IPC、BackgroundHTTP、CEF3Utils、CUDA、HardwareSurvey | UE5 前半程的模块化主题：神经网络引擎入场、音频解码器从 Developer 组归位 Runtime、消息协议与后台下载基建 |
| **5.4 → 5.6 窗口** | 38 (10/8/20) | VerseCompiler + uLang 三件、MassEntity（首个 Mass 引擎模块）、AutoRTFM、DataflowSimulation、CADKernelEngine、TraceInsights 拆分三件、MathCore、StateStream | 5.5/5.6 是"新范式入引擎"的一代：Verse 语言、Mass、事务内存并行、TraceInsights 拆分细化同期发生 |
| **5.7 → 5.8 窗口** | 32 (4/4/24) | Mass 家族补全（MassCore/MassEngine/MassDeveloper/MassSignals）、GDK 三件、RigidPhysics、ChaosSpatialPartitions、带宽调试四件、WebSocketServer、TraceBasedDebuggers 两件 | 最新一代是"收尾与配套"：Mass 从单模块长成五件套，Xbox GDK 与观测/调试面补齐 |

窗口期内的**搬家与退场**同样有信息量：SerializedRecorderInterface 从 Editor 组整体搬进 Runtime 组（录制能力运行时化）；ColorManagement 与 VirtualFileCache 一直活到 5.6 快照、5.8 前退场（色彩管理并入 OpenColorIOWrapper 体系、VFC 让位 Zen）。

**Runtime 组 +72 个新模块，按主题成批出现**（UE5 时代的主战场）：

- **Mass 全家入驻 Runtime**（MassCore, MassEngine, MassEntity, MassDeveloper, MassSignals）——ECS 框架从实验插件升格为引擎模块——大规模实体成为一等公民
- **新语言与 AI**（VerseCompiler, uLangCore, uLangJSON, uLangUE, NNE）——Verse 语言编译器与神经网络引擎 NNE 进入 Runtime
- **消息协议矩阵**（XMPP, Stomp, WebSocketServer, IPC, ExternalRpcRegistry）——IM/消息总线类协议模块化，服务化架构准备
- **音频解码器归位**（OpusAudioDecoder, VorbisAudioDecoder, AdpcmAudioDecoder, RadAudioDecoder, AudioChannelAgnosticCore, AudioLinkCore）——解码器从 Developer 的 AudioFormat* 重组为 Runtime 模块 + AudioLink 对外混音器桥
- **GDK/发行三件**（GDKRuntime, GDKSaveGameSystem, GDKPackageManifest）——Xbox/商店生态的运行时支撑入模块
- **遥测与观测**（Instrumentation, StudioTelemetry, HardwareSurvey, TraceBasedDebuggers, TraceBasedDebuggersAnalysis, BandwidthDebugDelegates, BandwidthMeasurementTool）——运行时观测面持续加厚
- **内容分发**（IoStoreOnDemandCore, BackgroundHTTP, BackgroundHTTPFileHash, RuntimeAssetCache, IndexedCacheStorage）——按需流送/热更基建下沉为引擎模块
- **CAD 与几何**（CADKernelEditor, CADKernelEngine, DataflowSimulation）——CAD 内核全链路 + Dataflow 仿真的引擎化

**Developer 组换代**：Developer 组 +21/-20，数字平稳但**换代剧烈**：老 Profiler 系（ProfilerClient/ProfilerService/ProfilerMessages/RealtimeProfiler）整体退场，被 Trace 系（TraceInsightsCore/TraceInsightsFrontend/TraceTools）取代——这就是 Unreal Insights 取代旧 Profiler 的模块级证据；TextureFormat*/AudioFormat* 等"格式模块"从 Developer 组消失（挪入平台层）；新增全是协作与构建加速（SlackIntegrations/SubmitToolCore/UbaCoordinatorHorde/ZenOplogUtils）。

**Editor 组**：Editor 组 +17/-6：Cascade（旧粒子编辑器模块）退场（转为插件形态保遗留资产）、SettingsViewer/ProjectSettingsViewer 合并进新配置体系；新增 MassEntityDebugger/Editor、ZenEditor、UniversalObjectLocatorEditor、WorldBookmark——大世界与新存储的编辑器配套。

**插件层新生与死亡**：4.27 没有而 5.8 出生的标志性插件（按主题）：**MetaHuman 全家**（MetaHuman/Generator/Calibration*/AnimationTools/Crowd/SDK）、**Electra 播放器矩阵**（ElectraPlayer/ElectraCodecs + 各解码器）、**新动画框架 UAF**（UAF/UAFAnimGraph/UAFControlRig/UAFMass/UAFPoseSearch/UAFChooser 等 13 个）、**Chaos 玩法化**（ChaosOutfitAsset/ChaosFleshGenerator/ChaosModularVehicle/ChaosRigidAsset）、**Mover 移动新框架**、**StateTree/SmartObjects 引擎化前的插件生态**、**OnlineServices 新在线体系**（OnlineServices* + EOSVoiceChat）、**Pixel Streaming 2**、**OpenXR 全面接管 XR**、**CaptureManager/虚拟摄制扩容**（Composite/ComposureShared/StageMonitoring）、以及 **ModelContextProtocol/CmdLinkServer**（AI 工具链接口，5.8 很新的动向）。

**确认退役**：确认真死亡的代表性插件：Oculus 系（OculusAudio/OnlineSubsystemOculus→Meta 迁移 OpenXR+EOS）、GoogleARCore 系（被 OpenXR 吸收）、旧在线体系（Party/Lobby/Qos/Rejoin→OnlineServices）、MegascansPlugin（并入 Fab 生态）、SteamAudio、AzureSpatialAnchors、PlasticSourceControl（4.27 收录、5.8 移除）。

## 附录：数据与核验

**数据文件**（`_work/`）：`engine_modules_merged.json`（494 模块页完整提取，条目带官方 Remarks）、`local_uplugins.json`（本机 5.8 版 893 个 .uplugin）、`bp_categories_full.json`（889 蓝图分类页全量）、`python_sections.json`（Python API 类型清单）、`diff_427_58.json` + `groups_427.json` + `groups_versions.json` + `module_timeline.json`（版本组页/差分/入场时间线；5.0 实测回退 4.27 快照）、`plugin_mods_local.json`（插件模块反射面 262 个）、`cpp_leaf_summary.json` + `py_leaf.json` + `py_sweep_full.json`（叶级：32 C++ 类 + 28 Python 类 + 250 动作类普查）、`bp_node_leaf.json` + `bp_nodes_all.json`（节点页 600 个含宿主声明）、`doc_data*.py`/`build_doc.py`（生成器，含 494 模块恰好归一域校验）。

**核验方式**：

1. 数据经真实浏览器会话从文档站 `document.json` 接口逐页提取，494 个引擎模块页全量命中、零失败；
2. 插件：抽 8 个文档页描述/分类与本机 UE_5.8 `.uplugin` 逐字节比对，8/8 一致，统计采用本地全量；
3. 正文所有类名与英文引文（AActor/UFunction/FSoftObjectPath/AGameModeBase/FDynamicRHI/FVertexFactory/SWindow/UUserWidget/UMovieScene/AAIController/FGuidReferences/UMassEntitySubsystem/UInterchangeBaseNodeContainer/UNNEModelData 等）均直接取自提取数据；
4. 蓝图 889 个分类页**全量抓取完成**（含 Add* 系列实测 0 子项的图菜单占位分类），合计 14,613 个子条目（子分类+节点页）；
5. 机制/能做什么/工作流为综合归纳（官方无此维度），模块域归属经脚本校验（494 恰好各归一域）。
