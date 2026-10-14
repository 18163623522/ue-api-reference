# UE 5.8 控制台命令（CVar）分类总览

> 数据来源：dev.epicgames.com 官方 Console Variables Reference 页全量提取（2026-10-14）  
> 规模：**6,581 个变量 / 159 个分类**，每条含名称/默认值/官方描述  
> 配套数据文件：`_work/cvar_data.json`（结构化 JSON，可直接查询）

## 一、规模与分布

| 分类 | 变量数 | 占比 | 分类 | 变量数 |
|---|---|---|---|---|
| **Rendering** | 3,007 | 45% | Grass | 32 |
| **Physics** | 958 | 14% | IAS | 32 |
| **FX** | 296 | 4% | Editor | 31 |
| **Networking** | 223 | 3% | AI | 28 |
| **Show Flag** | 215 | 3% | Niagara | 26 |
| **Audio** | 198 | 3% | Scalability Quality | 26 |
| **Slate** | 140 | 2% | Foliage | 24 |
| **Virtual Reality Editor** | 103 | 1% | CSV | 21 |
| **Animation** | 71 | 1% | Interchange | 20 |
| **VI** | 70 | 1% | RHI | 19 |
| **Scalability** | 68 | 1% | Log | 18 |
| **Networked Physics** | 64 | 0% | Time | 18 |
| **Landscape** | 61 | 0% | Control Rig | 17 |
| **D3D12** | 56 | 0% | Voice | 16 |
| **World Partition** | 52 | 0% | Modeling | 15 |
| **Demo** | 44 | 0% | Tick | 14 |
| **Garbage Collection** | 44 | 0% | Virtual Memory | 14 |
| **Blueprint** | 41 | 0% | Cook | 13 |
| **Sequencer** | 40 | 0% | Online Subsytem | 11 |
| **Task Graph** | 35 | 0% | Render Doc | 11 |
| 其余 119 个分类 | 389 | | | |

**前缀分布**（变量名第一段）：r.* 渲染 3,004 个、p.* 物理 949、fx.* 特效 269、ShowFlag.* 显示开关 215、net.* 网络 201、au.* 音频 190——**渲染占了近半**，是引擎可调参数最密集的子系统。

**渲染变量的二级前缀**（r.XXX.* 的 XXX 部分，标出 UE5.x 渲染特性权重）：

| 二级前缀 | 数量 | 对应子系统 |
|---|---|---|
| r.Lumen.* | 328 | Lumen 全局光照/反射 |
| r.Shadow.* | 182 | 阴影（CSM/VSM/各类） |
| r.RayTracing.* | 154 | 硬件光线追踪 |
| r.HairStrands.* | 143 | 毛发渲染 |
| r.Nanite.* | 123 | Nanite 虚拟几何 |
| r.LumenScene.* | 108 | Lumen 场景细节 |
| r.PathTracing.* | 73 | 路径追踪 |
| r.HeterogeneousVolumes.* | 71 | 异构体积 |
| r.VT.* | 69 | 虚拟纹理 |
| r.Mobile.* | 58 | 移动端渲染 |
| r.Streaming.* | 56 | 纹理/网格流送 |
| r.VolumetricCloud.* | 36 | 体积云 |
| r.ManyLights.* | 30 | 多光源（许多灯场景优化） |

**默认值类型**：0/1 整型开关 3,196（49%）、布尔 true/false 995（15%）、浮点 445（7%）、其他（字符串/枚举/路径）1,945（29%）——**近半是开关型**，控制台命令的核心用途是"打开/关闭引擎特性"。

## 二、各大类核心命令速查

### Rendering（渲染 · 3,007 个）

渲染是 CVar 最多的域，覆盖 AA/Lumen/Nanite/阴影/光线追踪/后处理/流送等全部渲染管线开关。

| 命令 | 默认值 | 说明 |
|---|---|---|
| `r.AntiAliasingMethod` | `4` | Engine default (project setting) for AntiAliasingMethod is (postprocess volume/camera/game setting still can override)   |
| `r.BackbufferQuantizationDitheringOverride` | `0` | Override the bitdepth in bits of each channel of the backbuffer targeted by the quantization dithering. Disabled by defa |
| `r.BadDriverWarningIsFatal` | `false` | If non-zero, trigger a fatal error if a denylisted driver is detected.  For the fatal error to occur, r.WarnOfBadDrivers |
| `r.BasePassWriteDepthEvenWithFullPrepass` | `0` | 0 to allow a readonly base pass, which skips an MSAA depth resolve, and allows masked materials to get EarlyZ (writing t |
| `r.CompileShadersForDevelopment` | `1` | Setting this to 0 allows to ship a game with more optimized shaders as some  editor and development features are not lon |
| `r.CookOutUnusedDetailModeComponents` | `0` | If set, components which are not relevant for the current detail mode will be cooked out.   0: keep components even if n |
| `r.DBuffer` | `1` | Enables DBuffer decal material blend modes.  DBuffer decals are rendered before the base pass, allowing them to affect s |
| `r.DeferUniformExpressionCaching` | `1` | Whether to defer caching of uniform expressions until a rendering command needs them up to date.  Deferring updates is m |
| `r.DeferUpdateRenderStates` | `1` | Whether to defer updating the render states of material parameter collections when a paramter is changed until a renderi |
| `r.DetailMode` | `3` | Current detail mode; determines whether components of actors should be updated/ ticked.   0: low, show objects with Deta |
| `r.DisableEngineAndAppRegistration` | `0` | If true, disables engine and app registration, to disable GPU driver optimizations during debugging and development  Cha |
| `r.DrawRectangleOptimization` | `1` | Controls an optimization for DrawRectangle(). When enabled a triangle can be used to draw a quad in certain situations ( |
| `r.DriverDetectionMethod` | `5` | Defines which implementation is used to detect the GPU driver (to check for old drivers, logs and statistics)    0: Iter |
| `r.DynamicGlobalIlluminationMethod` | `1` | 0 - None.  Global Illumination can be baked into Lightmaps but no technique will be used for Dynamic Global Illumination |
| `r.Filter.LoopMode` | `0` | Controls when to use either dynamic or unrolled loops to iterates over the Gaussian filtering.  This passes is used for  |
| `r.Filter.SizeScale` | `1` | Allows to scale down or up the sample count used for bloom and Gaussian depth of field (scale is clamped to give reasona |
| `r.Forward.MaxCulledLightsPerCell` | `32` | Controls how much memory is allocated for each cell for light culling.  When r.Forward.LightLinkedListCulling is enabled |
| `r.ForwardShading` | `0` | Whether to use forward shading on desktop platforms - requires Shader Model 5 hardware.  Forward shading has lower const |
| `r.FramesToExpandNewlyOcclusionTestedBBoxes` | `2` | If we don't occlusion test a primitive for r.GFramesNotOcclusionTestedToExpandBBoxes frames, then we expand the BBox whe |
| `r.FullScreenMode` | `1` | Defines how we do full screen when requested (e.g. command line option -fullscreen or in ini [SystemSettings] fullscreen |

### Physics（物理 · 958 个）

Chaos 物理、碰撞、载具、布料、破坏、异步物理的完整参数面。

| 命令 | 默认值 | 说明 |
|---|---|---|
| `p.AddFormerBaseVelocityToRootMotionOverrideWhenFalling` | `true` | To avoid sudden velocity changes when a root motion source moves the pawn from a moving base to free fall, this CVar wil |
| `p.AsyncPhysicsBlockMode` | `0` | Setting to 0 blocks on any physics steps generated from past GT Frames, and blocks on none of the tasks from current fra |
| `p.bUseUnifiedHeightfield` | `1` | Whether to use the PhysX unified heightfield. This feature of PhysX makes landscape collision consistent with triangle m |
| `p.Chaos.CCD.AxisThresholdMode` | `2` | Change the mode used to generate CCD axis threshold bounds for particle geometries.  0: Use object bounds  1: Find the t |
| `p.Chaos.Collision.Manifold.ForceOneShotManifoldEdgeEdgeCaseZeroCullDistance` | `false` | If enabled, if one shot manifold hits edge/edge case, we will force a cull distance of zero. That means edge/edge contac |
| `P.Chaos.SyncKinematicOnGameThread` | `-1` | If set to 1, kinematic bodies will always send their transforms back to the game thread, following the simulation step/r |
| `p.Chaos.VD.Tool.PlayAllPreviousFrameSteps` | `true` | If true, each time we get playback a solver frame in a specific stage, we will play all the previous steps from that fra |
| `p.Chaos.XPBDSpring.SplitDamping` | `4` | Test xpbd spring split damping mode. 0 = single lambda, 1 = interleaved with damping after (non-ispc only), 2 interleave |
| `p.Cloth.MaxVelocityScale` | `1` | The maximum amount of the component induced velocity allowed on all cloths.  Use 1.0 for fully induced velocity(default) |
| `p.Cloth.TeleportRotationThreshold` | `0` | Require p.Cloth.TeleportOverride. Rotation threshold in degrees, ranging from 0 to 180.   Conduct teleportation if the c |
| `p.DeferCharacterMeshMovement` | `false` | Optimization - When enabled, defers CharacterMesh move propagation until the end of larger scoped moves. The mesh will s |
| `p.gc.RemoveImplicitsInDynamicCollections` | `false` | This cvar has an impact only if geometry are not added for children. It removes implicits from the Dynamic Collections,  |
| `p.GeometryCollection.ForceOverrideGCCollisionSetupForTraces` | `-1` | Force the usage of a specific type of collision for traces on the game thread when creating new GC physics representatio |
| `p.MoveIgnoreFirstBlockingOverlap` | `0` | Whether to ignore the first blocking overlap in SafeMoveUpdatedComponent (if moving out from object and starting in pene |
| `p.NetForceClientAdjustmentPercent` | `0` | Percent of ServerCheckClientError checks to return true regardless of actual error.  Useful for testing client correctio |

### FX / Niagara（特效 · 296+26 个）

特效预算（fx.Budget）、Niagara GPU/CPU 仿真、Cascade 兼容、粒子管理。

| 命令 | 默认值 | 说明 |
|---|---|---|
| `fx.Budget.GameThread` | `2` | Budget (in ms) for all combined FX work that runs only on the gamethread. As this budget is approached or exceeded, vari |
| `fx.Budget.GameThreadConcurrent` | `2` | Budget (in ms) for all combined FX work that runs on the gamethread or on a concurrent task spawned from the game thread |
| `fx.Budget.RenderThread` | `2` | Budget (in ms) for all combined FX work that runs on the Render Thread.  As this budget is approached or exceeded, vario |
| `fx.Cascade.SkipZeroDeltaTime` | `true` | When enabled a delta tick time of nearly 0.0 will cause us to skip the component update.  This fixes issue like PSA_Velo |
| `fx.EnableNiagaraCRHandler` | `0` | If > 0 Niagara will push some state into the crash reporter. This is not free so should not be used unless actively trac |
| `fx.LWCTileRecache` | `2` | When we cross this number of LWC tiles from where we started the FX we need to recache the LWC tile to avoid artifacts.  |
| `fx.Niagara.Batcher.TickFlush.MaxQueuedFrames` | `3` | The number of unprocessed frames with queued ticks before we process them.  The larger the number the more data we proce |
| `fx.Niagara.Batcher.TickFlush.Mode` | `1` | What to do when we go over our max queued frames.  0 = Keep ticks queued, can result in a long pause when gaining focus  |
| `fx.Niagara.CompileHashAllDataInterfaces` | `1` | Forces Niagara to include all data interfaces as part of compile hash generation.  0 = Disabled.  1 = Enabled, but hash  |
| `fx.Niagara.Emitter.ComputePSOPrecacheMode` | `1` | Controlls how PSO precaching should be done for Niagara compute shaders  0 = Disabled (Default).  1 = Enabled if r.PSOPr |
| `fx.Niagara.Emitter.MaxGPUBufferElements` | `0` | Maximum elements per GPU buffer, for example 4k elements would restrict a float buffer to be 16k maximum per buffer.  No |
| `fx.Niagara.LegacyDeviceProfile` | `-1` | This is a special case CVar that allows us to use CVar conditions to maintain behavior with legacy device profiles.  Do  |

### Networking（网络 · 223 个）

复制频率、包处理、加密、回放、带宽控制的网络层参数。

| 命令 | 默认值 | 说明 |
|---|---|---|
| `n.IpNetDriverMaxFrameTimeBeforeAlert` | `1` | Time to spend processing networking data in a single frame before an alert is raised (in seconds)  It may get called mul |
| `net.AllowAsyncLoading` | `0` | Allow async loading of unloaded assets referenced in packets. If false the client will hitch and immediately load the as |
| `net.AllowEncryption` | `1` | If true, the engine will attempt to load an encryption PacketHandler component and fill in the EncryptionToken parameter |
| `net.AlwaysUpdateGuidReferenceMapForNetSerializeObjectStruct` | `false` | Requires net.TrackNetSerializeObjectReferences. If true, entries in the GuidReferenceMap for NetSerialize struct propert |
| `net.ClientIncomingBunchFrameTimeLimitMS` | `0` | Time in milliseconds to limit client incoming bunch processing to. If 0, no limit. As long as we're below the limit, wil |
| `net.DelayUnmappedRPCs` | `0` | If true delay received RPCs with unmapped object references until they are received or loaded, if false RPCs will execut |
| `net.DelinquencyNumberOfTopOffendersToTrack` | `10` | When > 0 , this will be the number of 'TopOffenders' that are tracked by the PackageMap and GuidCache for Queued Actors  |
| `net.InstantReplayProcessQueuedBunchesMillisecondLimit` | `8` | Time threshold for processing queued bunches during instant replays. If it takes longer than this in a single frame, wai |
| `net.IpNetDriverReceiveThreadPollTimeMS` | `250` | If net.IpNetDriverUseReceiveThread is true, the number of milliseconds to use as the timeout value for FSocket::Wait on  |
| `net.Iris.DispatchUnresolvedPreviouslyReceivedChanges` | `false` | Whether to include previously received changes with unresolved object references to data received this frame when applyi |

### Show Flag（显示开关 · 215 个）

视口级别的渲染特性开关（showflag.* 前缀），控制单个渲染 Pass 的显示/隐藏。

| 命令 | 默认值 | 说明 |
|---|---|---|
| `ShowFlag.ActorColoration` | `2` | Allows to override a specific showflag (works in editor and game, show" only works in game and UI only in editor)  Usefu |
| `ShowFlag.AmbientCubemap` | `2` | Allows to override a specific showflag (works in editor and game, show" only works in game and UI only in editor)  Usefu |
| `ShowFlag.AmbientOcclusion` | `2` | Allows to override a specific showflag (works in editor and game, show" only works in game and UI only in editor)  Usefu |
| `ShowFlag.AntiAliasing` | `2` | Allows to override a specific showflag (works in editor and game, show" only works in game and UI only in editor)  Usefu |
| `ShowFlag.Atmosphere` | `2` | Allows to override a specific showflag (works in editor and game, show" only works in game and UI only in editor)  Usefu |
| `ShowFlag.AudioRadius` | `2` | Allows to override a specific showflag (works in editor and game, show" only works in game and UI only in editor)  Usefu |
| `ShowFlag.BillboardSprites` | `2` | Allows to override a specific showflag (works in editor and game, show" only works in game and UI only in editor)  Usefu |
| `ShowFlag.Bloom` | `2` | Allows to override a specific showflag (works in editor and game, show" only works in game and UI only in editor)  Usefu |
| `ShowFlag.Bones` | `2` | Allows to override a specific showflag (works in editor and game, show" only works in game and UI only in editor)  Usefu |
| `ShowFlag.Bounds` | `2` | Allows to override a specific showflag (works in editor and game, show" only works in game and UI only in editor)  Usefu |

### Audio（音频 · 198 个）

混音器、MetaSound、Quartz 时钟、流送缓存、空间化的音频参数。

| 命令 | 默认值 | 说明 |
|---|---|---|
| `au.MaxRandomBranches` | `0` | Sets the max amount of branches to play from for any random node. The rest of the branches will be released from memory. |
| `au.MetaSound.AutoUpdate.NativeClassesOfEqualVersion` | `1` | If true, node references to native classes that share a version number will attempt to auto-update if the interface is d |
| `au.Quartz.bAlwaysTakeVoiceSlot` | `1` | Always take voice slot immediately without trying to cache the request on the component  default = 1: always forward the |
| `au.Quartz.TimeToTakeUpVoiceSlot` | `6` | TheEQuartzCommandQuantization type (default: EQuartzCommandQuantization::EighthNote) before playing that a queued sound  |
| `au.resonance.quality` | `0` | Override the quality of resonance sound sources. Will not increase quality levels. The quality used will be min of the q |
| `au.streamcache.BlockOnChunkLoadCompletion` | `0` | When set to 1, USoundWaves we will always attempt to synchronously load a chunk after a USoundWave request has finished. |
| `au.streamcache.DispatchToGameThreadOnChunkRequest` | `1` | When set to 1, we will always dispatch a callback to the game thread whenever a USoundWave request has finished. This ma |
| `au.streamcache.SoundWaveDefaultLoadingBehavior` | `3` | This can be set to define the default behavior when a USoundWave is loaded.  1: Retain audio data on load, 2: prime audi |
| `au.streamcaching.BlockForPendingLoadOnCacheOverflow` | `0` | This cvar sets the default request priority for audio chunks that are about to play back, but aren't in the cache.  0: W |
| `au.streamcaching.KeepCacheMissBufferOnFlush` | `1` | If set to 1, this will maintain the buffer of recorded cache misses after calling AudioMemReport. Otherwise, calling aud |

### Animation（动画 · 71 个）

动画蓝图求值、URO 优化、蒙皮权重、Sequencer 动画。

| 命令 | 默认值 | 说明 |
|---|---|---|
| `a.EnableQueuedAnimEventsOnServer` | `1` | Whether to enable queued anim events on servers. In most cases, when the server is doing a full anim graph update, queue |
| `a.SkinWeightProfile.LoadByDefaultMode` | `-1` | Enables/disables run-time optimization to override the original skin weights with a profile designated as the default to |
| `a.CacheLocalSpaceBounds` | `1` | If 1 (default) local-space bounds are calculated and cached, otherwise worldspace bounds are built and cached (and inver |
| `a.AnimSequencer.DirectControlRigMode` | `1` | 1 = FKControl rig uses Direct method for setting Control transforms. 0 = FKControl rig uses Replace method (transform of |
| `a.Compression.ValidateCompressedRichCurveEvaluation` | `0` | 1 = runs validation, evaluating the compressed rich curve at animation its sampling rate comparing against the MaxCurveE |
| `a.URO.ForceAnimRate` | `0` | Non-zero to force anim rate. 10 = eval anim every ten frames for those meshes that can do it. In some cases a frame is c |
| `a.MotionTrajectory.Options` | `0` | Toggle motion trajectory sample information:   0. Disable Text   1. Index  2. Accumulated Time   3. Position   4. Veloci |
| `a.OutputMontageFrameRateWarning` | `false` | If true will warn the user about Animation Montages/Composites composed of incompatible animation assets (incompatible f |

### Blueprint（蓝图 · 41 个）

蓝图编译、搜索、库加载、字节码优化的蓝图系统参数。

| 命令 | 默认值 | 说明 |
|---|---|---|
| `bp.EnableAutomaticLibraryAssetLoading` | `1` | Should opening the BP editor load all macro and function library assets or not?  0: Disable, 1: Enable (defaults to enab |
| `bp.ForceOldSearchDataFormatVersionOnSave` | `false` | Force Blueprint search metadata to use an old format version on save (for QA/testing purposes only). On an editor relaun |
| `bp.DisableSearchDataUpdateOnSave` | `false` | Don't update Blueprint search metadata on save (for QA/testing purposes only). On an editor relaunch, it should include  |
| `BP.bForceAllDependenciesToRecompile` | `false` | If true all dependencies will be bytecode-compiled even when all referenced functions have no signature changes. Intende |
| `BP.bEnableSkelReinstUpdate` | `true` | If true the Reinstancing of SKEL classes will use the new FBlueprintCompileReinstancer::MoveDependentSkelToReinst(o(n))  |
| `BP.ActionMenuFilterCacheLeafCapacity` | `32` | The number of action menu contexts to cache simultaniously. raising this number will increase the memory footprint but d |
| `bp.BlamePrintString` | `false` | When true, prints the Blueprint Asset and Function that generated calls to Print String. Useful for tracking down screen |
| `Blueprint.PC_Real.DisplayMode` | `1` | Real naming mode  	0: Real  	1: Float (default)  	2: Number    Note the editor needs to be restarted for this to fully t |

### AI / 导航（AI · 28 个）

NavMesh 生成/压缩/分区、AI 感知系统的参数。

| 命令 | 默认值 | 说明 |
|---|---|---|
| `ai.nav.NavmeshUseOodleCompression` | `true` | Use Oodle for run-time tile cache compression/decompression. Optimized for size in editor, optimized for speed in standa |
| `ai.nav.UseTightBoundExpansion` | `true` | Active by default. Use an expansion of one AgentRadius. Set to false to revert to the previous behavior (2 AgentRadius). |
| `ai.DestroyNavDataInCleanUpAndMarkPendingKill` | `1` | If set to 1 NavData will be destroyed in CleanUpAndMarkPendingKill rather than being marked as garbage. |
| `ai.NavCollisionAvailable` | `1` | If set to 0 NavCollision won't be cooked and will be unavailable at runtime. |
| `ai.nav.RecentlyBuildTileDisplayTime` | `0.2` | Time (in seconds) to display tiles that have recently been built. |
| `ai.nav.EnableSpanHeightRasterizationFix` | `true` | Active by default. Enable rasterization fix for span height. |
| `ai.nav.EnableNavMeshResolutions` | `true` | When set to false, navmesh resoutions will be ignored. |
| `ai.nav.bNavmeshAllowPartitionedBuildingFromEditor` | `false` | Enable experimental navmesh partition building. |

### Garbage Collection（GC · 44 个）

垃圾回收频率、增量 GC、低内存策略。

| 命令 | 默认值 | 说明 |
|---|---|---|
| `gc.GarbageReferenceTrackingEnabled` | `0` | Causes the Garbage Collector to track and log unreleased garbage objects. If 1, will dump every reference. If 2, will du |
| `gc.VerifyUObjectsAreNotFGCObjects` | `0` | If true, the engine will throw a warning when it detects a UObject-derived class which also derives from FGCObject or an |
| `gc.LowMemory.TimeBetweenPurgingPendingKillObjects` | `30` | Time in seconds (game time) we should wait between purging object references to objects that are pending kill when we're |
| `gc.LowMemory.TimeBetweenPurgingPendingLevels` | `15` | Time in seconds (game time) we should wait between GC when we're low on memory and there are levels pending unload |
| `gc.ContinuousIncrementalGC` | `0` | Used to debug garbage collection...Kicks off Incremental Garbage Collection as soon as the previous one finishes. |
| `gc.ForceEnableGCProcessor` | `false` | Force garbage collection to use the debug processor which may provide additional information during GC crashes. |
| `gc.TimeBetweenPurgingPendingKillObjects` | `61.1` | Time in seconds (game time) we should wait between purging object references to objects that are pending kill. |
| `gc.DelayReachabilityIterations` | `0` | Causes the Garbage Collector to delay incremental reachability iterations by the provided number of frames. |

### World Partition（世界分区 · 52 个）

大世界流送、空间哈希、网格对齐、服务器流出的参数。

| 命令 | 默认值 | 说明 |
|---|---|---|
| `wp.Runtime.RuntimeSpatialHashCellToSourceAngleContributionToCellImportance` | `0.4` | Value between 0 and 1 that modulates the contribution of the angle between streaming source-to-cell vector and source-fo |
| `wp.Runtime.UseMakingInvisibleTransactionRequests` | `false` | Whether the client should wait for the server to acknowledge visibility update before making partitioned world streaming |
| `wp.Runtime.UseMakingVisibleTransactionRequests` | `false` | Whether the client should wait for the server to acknowledge visibility update before making partitioned world streaming |
| `wp.Runtime.PlayerController.ForceUsingCameraAsStreamingSource` | `0` | Whether to force the use of the camera as the streaming source for World Partition. By default the player pawn is used.  |
| `wp.Runtime.RuntimeSpatialHashSnapNonAlignedGridLevelsToLowerLevels` | `true` | Set RuntimeSpatialHashSnapNonAlignedGridLevelsToLowerLevels to false to avoid snapping higher levels cells to child cell |
| `wp.Runtime.RuntimeSpatialHashUseAlignedGridLevels` | `true` | Set RuntimeSpatialHashUseAlignedGridLevels to false to help break the pattern caused by world partition promotion of act |
| `wp.Runtime.RuntimeSpatialHashPlaceSmallActorsUsingLocation` | `false` | Set RuntimeSpatialHashPlaceSmallActorsUsingLocation to true to place actors smaller than a cell size into their correspo |
| `wp.Runtime.EnableServerStreamingOut` | `false` | Turn on/off to allow or not the server to stream out levels (only relevant when server streaming is enabled)  Changing t |

### Sequencer（时间线 · 40 个）

序列编译、运动更新、确定性围栏的参数。

| 命令 | 默认值 | 说明 |
|---|---|---|
| `Sequencer.AddKeepStateDeterminismFences` | `true` | Whether the Sequencer compiler should auto-add determinism fences for the last frame of KeepState sections. This ensures |
| `Sequencer.AutoTangentNew` | `2` | If 2 Sequencer will flatten tangents with no overshoot, if 1 Auto Tangent will use new algorithm to gradually flatten ma |
| `Sequencer.DeferMovementUpdates` | `false` | (Default: false) Enables deferring all Scene Component movement updates to the end of a sequencer evaluation to avoid ex |
| `Sequencer.MaterialParameterEntityLifetimeTracking` | `false` | (Default: false) Ensure on destruction that all entities have been cleaned up. This can report false positives (when the |
| `Sequencer.OutputDeferredMovementMode` | `0` | Integer value specifying how to output Scene Components with deferred movement updates from Sequencer: (0 - Default) No  |
| `Sequencer.TickIntervalGroupingResolutionMs` | `50` | Defines the maximum resolution for actor tick interval groupings. Bigger numbers will group more actors together when th |
| `Sequencer.VolatileSequencesInEditor` | `1` | (Default: 1) When non-zero, all assets will be treated as volatile in editor. Can be disabled to bypass volatility check |
| `Sequencer.DuplicateLinkedAnimSequence` | `false` | When true when we duplicate a level sequence that has a linked anim sequence it will duplicate and link the anim sequenc |

## 三、高频实用命令（跨分类精选）

### 性能调试

| 命令 | 说明 |
|---|---|
| `stat fps` | 显示帧率 |
| `stat unit` | 显示各线程耗时（Game/Draw/RHI/GPU） |
| `stat scenerendering` | 场景渲染统计 |
| `stat memory` | 内存概览 |
| `stat gc` | GC 统计 |
| `stat net` | 网络统计 |
| `stat particles` | 粒子系统统计 |
| `stat animation` | 动画统计 |
| `stat streaming` | 纹理/网格流送统计 |
| `freeze` | 冻结渲染（检查被剔除的对象） |
| `slomo 0.1` | 慢动作（0.1 倍速） |

### 渲染调试

| 命令 | 说明 |
|---|---|
| `r.ScreenPercentage 50` | 渲染分辨率 50% |
| `r.AntiAliasingMethod 0/1/2/4` | AA 切换（无/FXAA/TAA/TSR） |
| `r.Lumen.ScreenProbeGather 0` | 关闭 Lumen |
| `r.Nanite 0` | 关闭 Nanite |
| `r.ShadowQuality 0` | 关闭阴影 |
| `r.RayTracing 0/1` | 开关硬件光追 |
| `r.PathTracing 0/1` | 开关路径追踪 |
| `r.VT.PoolSize 512` | 虚拟纹理池大小 |
| `r.BufferVisualization 1` | 缓冲可视化模式 |
| `viewmode unlit` | 无光照模式 |
| `viewmode wireframe` | 线框模式 |
| `viewmode lit` | 光照模式（恢复） |
| `r.VisualizeGC 1` | 可视化 GC 对象 |

### 物理调试

| 命令 | 说明 |
|---|---|
| `p.Chaos.DebugDraw.Enabled 1` | Chaos 物理调试绘制 |
| `show Collision` | 显示碰撞体 |
| `pxvis collision` | PhysX 碰撞可视化 |
| `p.AsyncPhysicsBlockMode 0` | 异步物理阻塞模式 |

### 特效（Niagara）

| 命令 | 说明 |
|---|---|
| `fx.Budget.GameThread 0` | 禁用 GT 特效预算 |
| ` Niagara.System.DebugDraw 1` | Niagara 调试绘制 |
| `fx.Niagara.DebugSimulateGPU 1` | GPU 仿真调试 |

### 编辑器/开发

| 命令 | 说明 |
|---|---|
| `t.MaxFPS 60` | 限制最大帧率 |
| `r.VSync 0/1` | 垂直同步 |
| `gamemode` | 显示当前 GameMode |
| `open [LevelName]` | 打开关卡 |
| `quit` | 退出 |
| `DumpConsoleCommands` | 导出全部命令到文件 |

## 四、怎么查全部 6,581 个变量

结构化数据已保存在 `_work/cvar_data.json`（按分类组织的 JSON）。可以用以下方式查：

```python
import json
cvars = json.load(open("_work/cvar_data.json"))
# 搜名称含 "lumen" 的所有变量
for cat, items in cvars.items():
    for it in items:
        if "lumen" in it["name"].lower():
            print(it["name"], "=", it["default"], it["desc"][:60])
```

或在 UE 编辑器/PIE 的控制台（~ 键）中直接输入变量名前缀自动补全。

---

*本文档由 UE 5.8 官方 Console Variables Reference 页全量提取生成，6,581 个变量 / 159 个分类，数据口径 2026-10-14。*