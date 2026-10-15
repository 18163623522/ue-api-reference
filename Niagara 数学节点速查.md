---
title: Niagara 数学节点速查
created: 2026-10-15 00:30
updated: 2026-10-15 00:30
source: UE 5.7.4 Niagara 源码 NiagaraEditorCommon.cpp 全量提取
tags:
  - UE
  - Niagara
  - math
  - HLSL
  - reference
---

# Niagara 数学节点速查

> 在 Niagara Stack 编辑器的表达式（Expression）中可用的全部数学运算节点，从引擎源码 `NiagaraEditorCommon.cpp` 全量提取。
> 每个节点列出：显示名、内部名、输入参数、输出、实用说明。

## 基础四则运算

| 节点名 | 内部名 | 输入 | 输出 | 公式 |
|---|---|---|---|---|
| **Add** `+` | `Add` | A, B（任意数值类型） | 同类型 | `A + B` |
| **Subtract** `−` | `Subtract` | A, B | 同类型 | `A - B` |
| **Multiply** `×` | `Mul` | A, B | 同类型 | `A * B` |
| **Divide** `÷` | `Div` | A, B | 同类型 | `A / B` |
| **MultiplyAdd** | `Madd` | A, B, C | 同类型 | `(A × B) + C`（融合乘加，比分开做快） |
| **Negate** | `Negate` | A | 同类型 | `-A` |
| **One Minus** `1-A` | `OneMinus` | A（标量） | float | `1 - A`（翻转 0~1 范围） |

## 插值与范围

| 节点名 | 内部名 | 输入 | 输出 | 实用说明 |
|---|---|---|---|---|
| **Lerp** | `Lerp` | A, B（同类型）, Alpha（float） | 同类型 | `A × (1-α) + B × α`。Alpha 0=A，1=B。支持标量/向量/颜色/位置插值 |
| **Clamp** | `Clamp` | A, Min, Max | 同类型 | `clamp(A, Min, Max)`。将值限制在 [Min, Max] 范围内 |
| **Min** | `Min` | A, B | 同类型 | `min(A, B)` 取较小值 |
| **Max** | `Max` | A, B | 同类型 | `max(A, B)` 取较大值 |
| **Saturate** | — | A（float） | float [0,1] | `saturate(A)` = clamp(A, 0, 1)，用于锁定到 0~1 |
| **SmoothStep** | — | A, Min, Max | float | 平滑阶梯：`t=clamp((A-Min)/(Max-Min),0,1); t*t*(3-2t)`。在 Min/Max 处有平滑过渡 |
| **Step** | `Step` | A（float） | 0 或 1 | `step(0, A)`。A ≥ 0 返回 1，A < 0 返回 0 |

## 指数与对数

| 节点名 | 内部名 | 输入 | 输出 | 实用说明 |
|---|---|---|---|---|
| **Pow** | `Pow` | Base（float）, Exp（float） | float | `pow(A, B)`。⚠️ A < 0 时会被 clamp 到 0（不支持负底数） |
| **Exp** | `Exp` | A | float | `e^A`（自然指数，e ≈ 2.718） |
| **Exp2** | `Exp2` | A | float | `2^A`（二进制指数，比 Exp 快） |
| **Log** | `Log` | A（>0） | float | `log_e(A)`（自然对数）。⚠️ A ≤ 0 会产生 NaN |
| **Log2** | `Log2` | A（>0） | float | `log_2(A)`（以 2 为底的对数） |
| **Sqrt** | `Sqrt` | A（≥0） | float | `√A`。⚠️ A < 0 会产生 NaN |
| **Reciprocal Sqrt** | `RSqrt` | A | float | `1 / √A`。比 `1 / Sqrt(A)` 快（硬件指令） |
| **Reciprocal** | `Rcp` | A | 同类型 | `1 / A`（精确版） |
| **Reciprocal Fast** | `RcpFast` | A | 同类型 | `1 / A`（快速近似，12 位精度，用 Newton-Raphson） |

> [!tip] 性能提示
> `RcpFast` 和 `RSqrt` 使用 GPU 硬件指令，在 GPU Sim 中比精确版本快数倍。精度损失在大多数视觉效果中不可察觉。

## 三角函数

所有三角函数都有三种角度模式：**周期**（默认）、**弧度**、**角度**。

| 节点名 | 内部名 | 输入 | 输出 | 公式 |
|---|---|---|---|---|
| **Sine** | `Sine` | Angle, Period | float [-1,1] | `sin(Angle × 2π/Period)` |
| **Sine (Radians)** | `Sine(Radians)` | AngleInRadians | float | `sin(A)` |
| **Sine (Degrees)** | `Sine(Degrees)` | AngleInDegrees | float | `sin(A × π/180)` |
| **Cosine** | `Cosine` | Angle, Period | float [-1,1] | `cos(Angle × 2π/Period)` |
| **Cosine (Radians)** | `Cosine(Radians)` | AngleInRadians | float | `cos(A)` |
| **Cosine (Degrees)** | `Cosine(Degrees)` | AngleInDegrees | float | `cos(A × π/180)` |
| **Tangent** | `Tangent` | Angle, Period | float | `tan(Angle × 2π/Period)` |
| **Tangent (Radians)** | `Tangent(Radians)` | AngleInRadians | float | `tan(A)` |
| **Tangent (Degrees)** | `Tangent(Degrees)` | AngleInDegrees | float | `tan(A × π/180)` |

### 反三角函数

| 节点名 | 内部名 | 输入 | 输出 | 说明 |
|---|---|---|---|---|
| **ArcSine** | `ArcSine` | A [-1,1], Period | float | `asin(A) × Period/2π` |
| **ArcSine (Radians)** | `ArcSine(Radians)` | A [-1,1] | float [−π/2, π/2] | `asin(A)` |
| **ArcSine (Degrees)** | `ArcSine(Degrees)` | A [-1,1] | float [−90, 90] | `asin(A) × 180/π` |
| **ArcCosine** | `ArcCosine` | A [-1,1], Period | float | `acos(A) × Period/2π` |
| **ArcCosine (Radians)** | `ArcCosine(Radians)` | A [-1,1] | float [0, π] | `acos(A)` |
| **ArcCosine (Degrees)** | `ArcCosine(Degrees)**` | A [-1,1] | float [0, 180] | `acos(A) × 180/π` |
| **ArcTangent** | `ArcTangent` | A | float | `atan(A) × Period/2π` |
| **ArcTangent (Radians)** | `ArcTangent(Radians)` | A | float [−π/2, π/2] | `atan(A)` |
| **ArcTangent (Degrees)** | `ArcTangent(Degrees)` | A | float | `atan(A) × 180/π` |
| **ArcTangent2** | `ArcTangent2` | A (Y), B (X) | float | `atan2(Y, X)`。根据 XY 确定 quadrant，输出完整 [−π, π] |
| **ArcTangent2 (Radians)** | `ArcTangent2(Radians)` | A (Y), B (X) | float [−π, π] | `atan2(Y, X)` |
| **ArcTangent2 (Degrees)** | `ArcTangent2(Degrees)` | A (Y), B (X) | float [−180, 180] | `atan2(Y, X) × 180/π` |

### 角度转换

| 节点名 | 内部名 | 输入 → 输出 | 说明 |
|---|---|---|---|
| **DegreesToRadians** | `DegreesToRadians` | float → float | `A × π / 180` |
| **RadiansToDegrees** | `RadiansToDegrees` | float → float | `A × 180 / π` |
| **PI** | `PI` | 无输入 → float | 常量 π ≈ 3.14159 |
| **TWO_PI** | `TWO_PI` | 无输入 → float | 常量 2π ≈ 6.28318 |

> [!tip] ATan2 用法
> `ArcTangent2(Y, X)` 是最常用的反三角函数——传入方向向量的 Y 和 X 分量，返回该向量的角度。比 `atan(Y/X)` 好，因为它能正确处理 X=0 和所有象限。常用于：粒子朝向计算、风场方向、螺旋运动。

## 取整与取模

| 节点名 | 内部名 | 输入 | 输出 | 说明 |
|---|---|---|---|---|
| **Floor** | `Floor` | A | float | 向下取整。`floor(3.7) = 3`，`floor(-3.2) = -4` |
| **Ceil** | `Ceil` | A | float | 向上取整。`ceil(3.2) = 4`，`ceil(-3.7) = -3` |
| **Round** | `Round` | A | float | 四舍五入到最近整数 |
| **Trunc** | `Trunc` | A | float | 截断小数部分（朝零取整）。`trunc(3.7)=3`，`trunc(-3.7)=-3` |
| **Frac** | `Frac` | A | float [0,1) | 取小数部分。`frac(3.7) = 0.7`。常用于循环/闪烁效果 |
| **Modulo** `%` | `FMod` | A, B | float | `A % B`（浮点取模，保留符号） |
| **Modulo Fast** | `FModFast` | A, B | float | `A % B`（快速版，精度略低） |

> [!tip] Frac 实用技巧
> `Frac(NormalizedTime)` 可以把 0~1 的归一化时间变成锯齿波——配合 `Abs(Frac(T) * 2 - 1)` 得到三角波，再配合 Sine 得到平滑脉冲。这是制作闪烁/脉冲效果的基础。

## 向量运算

| 节点名 | 内部名 | 输入 | 输出 | 实用说明 |
|---|---|---|---|---|
| **Dot** | `Dot` | A（vec2/3/4）, B（同类型） | float | **点积**：`A·B = |A||B|cos(θ)`。=0 垂直，>0 同向，<0 反向 |
| **Cross** | `Cross` | A（vec3）, B（vec3） | vec3 | **叉积**：`A×B`。结果垂直于 A 和 B 构成的平面。用于计算法线/旋转轴 |
| **Normalize** | `Normalize` | A（vec2/3/4） | 同类型（单位长度） | **归一化**：`A / |A|`。⚠️ 零向量输入会产生 NaN |
| **Length** | `Length` | A（vec2/3/4） | float | **长度**：`|A| = √(x² + y² + z²)` |
| **Distance** | `DistancePos` | A（Position）, B（Position） | float | **两点距离**：`|B - A|` |

### Direction and Length Safe

这是 Niagara 中最常用的复合向量节点之一（不是基础运算而是 Dynamic Input）：

| 输入 | 输出 | 说明 |
|---|---|---|
| Vector（vec3） | **Direction**（vec3，归一化） | 输入向量的方向（单位向量） |
| Vector（vec3） | **Length**（float） | 输入向量的长度 |
| Vector（vec3） | **b Was Zero**（bool） | 输入是否为零向量（Safe 版本特有） |

> [!warning] Normalize vs Direction and Length Safe
> `Normalize` 在输入为零向量时会产生 NaN（0/0）。`Direction and Length Safe` 检测零向量并返回安全值（方向=默认方向，长度=0）。在 GPU Sim 中处理可能为零的速度/力向量时，**始终用 Safe 版本**。

### 其他向量操作（通过 Dynamic Input 或 Custom HLSL）

| 操作 | 输入 | 输出 | HLSL 等价 |
|---|---|---|---|
| **Reflect** | V（入射方向）, N（法线） | vec3（反射方向） | `reflect(V, N)` |
| **Refract** | V, N, eta（折射率比） | vec3（折射方向） | `refract(V, N, eta)` |
| **DistanceSq** | A, B（vec3） | float（距离平方） | `dot(B-A, B-A)`，比 Distance 快（省 Sqrt） |
| **InverseLerp** | A, B, V（vec3） | float [0,1] | `(V-A)/(B-A)`，Lerp 的逆运算 |
| **Transform Position** | Pos（vec3）, Matrix | vec3 | `mul(Matrix, float4(Pos,1))` 含平移 |
| **Transform Vector** | Vec（vec3）, Matrix | vec3 | `mul(Matrix, float4(Vec,0))` 不含平移（方向向量） |

## 矩阵运算

| 节点名 | 内部名 | 输入 | 输出 | 说明 |
|---|---|---|---|---|
| **Matrix Multiply** | `MatrixMultiply` | A（Matrix）, B（Matrix） | Matrix | 矩阵 × 矩阵 |
| **Matrix × Vector4** | `MatrixVectorMultiply` | Matrix, Vector4 | Vector4 | 矩阵 × 四维向量 |
| **Matrix Transform Position** | `TransformPosition` | Matrix, Position（vec3） | vec3 | 用矩阵变换位置点（含平移分量） |
| **Matrix Transform Vector** | `TransformVector` | Matrix, Vector（vec3） | vec3 | 用矩阵变换方向向量（不含平移） |
| **Transpose** | `Transpose` | Matrix | Matrix | 矩阵转置 |
| **Row 0-3** | `Row0`~`Row3` | Matrix | vec4 | 提取矩阵的第 N 行 |

## 随机与噪声

| 节点名 | 内部名 | 输入 | 输出 | 说明 |
|---|---|---|---|---|
| **Random** | `Rand` | Max | float [0, Max) | 非确定性随机。每次播放结果不同 |
| **Random Integer** | `Rand Integer` | Max | int [0, Max) | 非确定性随机整数 |
| **Random Float** | `Rand Float` | Max | float [0, Max] | 非确定性随机浮点数 |
| **Seeded Random** | `SeededRand` | Max, Seed | float [0, Max) | **确定性随机**：同 Seed 同结果。用于可复现的效果 |
| **Seeded Integer Random** | `SeededRand Integer` | Max, Seed | int | 确定性随机整数 |
| **Seeded Float Random** | `SeededRand Float` | Max, Seed | float | 确定性随机浮点数 |
| **Hash Integer** | `Hash Integer` | 任意输入组合 | int [0, 2³¹-1] | 将任意输入哈希为整数 |
| **Hash Float** | `Hash Float` | 任意输入组合 | float [0, 1) | 将任意输入哈希为归一化浮点数 |
| **Noise** | `Noise` | Position（vec3） | float [-1,1] | 连续伪随机噪声。输入相近时输出相近（不是纯随机） |

> [!tip] Seeded vs Non-Seeded
> **Seeded Random** = 确定性（deterministic），同 Seed 同结果——用于网络同步、可回放的效果。
> **Random** = 非确定性，每次不同——用于纯视觉变化，不关心复现。
> 实际项目中推荐优先用 Seeded 版本，除非明确不需要复现。

## 比较与选择

| 节点名 | 符号 | 输入 | 输出 | 说明 |
|---|---|---|---|---|
| **Less Than** | `<` | A, B | bool | `A < B` |
| **Less Than Or Equal** | `<=` | A, B | bool | `A ≤ B` |
| **Greater Than** | `>` | A, B | bool | `A > B` |
| **Greater Than Or Equal** | `>=` | A, B | bool | `A ≥ B` |
| **Equal** | `==` | A, B | bool | `A == B` |
| **Not Equal** | `!=` | A, B | bool | `A ≠ B` |
| **Select** | — | Condition（bool）, TrueVal, FalseVal | 同类型 | `Condition ? TrueVal : FalseVal`（三元运算符） |

## 逻辑运算（布尔）

| 节点名 | 符号 | 输入 | 输出 | 说明 |
|---|---|---|---|---|
| **Logic AND** | `&&` | A（bool）, B（bool） | bool | A 且 B |
| **Logic OR | `\|\|` | A, B | bool | A 或 B |
| **Logic NOT** | `!` | A | bool | 非 A |
| **Bool Equal** | `==` | A, B | bool | A == B |
| **Bool Not Equal** | `!=` | A, B | bool | A ≠ B |

## 位运算（整数）

| 节点名 | 符号 | 输入 | 输出 | 说明 |
|---|---|---|---|---|
| **Bitwise AND** | `&` | A, B（int） | int | 按位与 |
| **Bitwise OR** | `\|` | A, B | int | 按位或 |
| **Bitwise XOR** | `^` | A, B | int | 按位异或 |
| **Bitwise NOT** | `~` | A | int | 按位取反 |
| **Left Shift** | `<<` | A, B（0-31） | int | A 左移 B 位 |
| **Right Shift** | `>>` | A, B（0-31） | int | A 右移 B 位（带符号） |

## 常量

| 节点名 | 值 | 说明 |
|---|---|---|
| **PI** | 3.14159... | 圆周率 |
| **TWO_PI** | 6.28318... | 2 × 圆周率 |

## Niagara 专用工具

| 节点名 | 内部名 | 输出 | 说明 |
|---|---|---|---|
| **Execution Index** | `ExecIndex` | int | 当前粒子在本次执行中的索引号。在 Spawn Script 中可用于插值 |
| **Spawn Interpolation** | `SpawnInterp` | float [0,1] | 插值生成时的归一化进度（0=上一帧位置, 1=当前位置） |
| **Abs** | `Abs` | 同输入类型 | `|A|` 绝对值 |
| **Sign** | `Sign` | -1, 0, 或 1 | 取符号 |

## Custom HLSL 中可用的额外函数

在 Niagara 的 Custom HLSL 节点中，除了上述所有操作外，还可以直接使用 HLSL 内置函数：

| 函数 | 输入 | 输出 | 说明 |
|---|---|---|---|
| `saturate(x)` | float | float [0,1] | clamp(x, 0, 1) |
| `smoothstep(a, b, x)` | 三个 float | float [0,1] | 平滑阶梯函数 |
| `mad(a, b, c)` | 三个 float | float | a×b + c（融合乘加） |
| `lerp(a, b, t)` | 三个同类型 | 同类型 | 线性插值 |
| `reflect(I, N)` | vec3, vec3 | vec3 | 反射向量 |
| `refract(I, N, eta)` | vec3, vec3, float | vec3 | 折射向量 |
| `faceforward(N, I, Ng)` | vec3 ×3 | vec3 | 使法线朝向入射方向的反面 |
| `mul(M, v)` | Matrix, Vector | Vector | 矩阵×向量 |
| `determinant(M)` | Matrix | float | 矩阵行列式 |
| `transpose(M)` | Matrix | Matrix | 矩阵转置 |
| `isfinite(x)` | float | bool | 检查是否有限（非 NaN/Inf） |
| `isnan(x)` | float | bool | 检查是否 NaN |

> [!warning] Custom HLSL 注意事项
> - 不能使用 `discard`、`clip` 等像素着色器指令（Niagara 是 compute shader）
> - `texture.Sample()` 不可用，要用 Niagara Data Interface 提供的采样函数
> - 所有输入必须通过节点的输入引脚传入，不能直接访问外部变量

---

# 补充：Dynamic Input 复合节点

> 以下是从引擎 DynamicInputs 资产目录全量提取的复合节点（250+ 个），按功能分类列出最实用的。

## 向量工具

| 节点名 | 输入 | 输出 | 实用说明 |
|---|---|---|---|
| **Safe Normalize Vector** | Vector | vec3（单位长度） | 安全归一化：零向量返回默认方向而不是 NaN。**永远优先用这个** |
| **Normalize Vector** | Vector | vec3 | 标准归一化（零向量产生 NaN） |
| **Vector Length** | Vector | float | 向量长度 `|V|` |
| **Vector Length Safe** | Vector | float + bool | 安全长度 + 是否为零向量 |
| **Cross Product** | A, B（vec3） | vec3 | 叉积 `A × B`，结果垂直于 A 和 B |
| **Dot Product** | A, B | float | 点积 `A · B` |
| **Negate Vector** | V | vec3 | `-V` 反方向 |
| **Scale and Bias A Vector** | V, Scale, Bias | vec3 | `V × Scale + Bias`（一步完成缩放+偏移） |
| **Rotate Vector** | V, Axis（vec3）, Angle（rad） | vec3 | 绕指定轴旋转向量 |
| **Rotate Vector by Quaternion** | V, Quat | vec3 | 用四元数旋转向量 |
| **Find Mid Point Between Positions** | A, B（Position） | Position | 两点的中点 `(A+B)/2` |
| **Find Quat Between Two Vectors** | From, To（vec3） | Quat | 计算从 A 方向旋转到 B 方向的四元数 |
| **Orient Mesh To Vector** | Direction（vec3） | Matrix | 生成朝向指定方向的旋转矩阵（让 mesh 面向某方向） |
| **Derive Z** | X, Y | float | 根据单位向量的 XY 分量推导 Z 分量 `√(1-x²-y²)` |

## 相机相关

| 节点名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Camera Position** | 无 | Position | 当前相机世界坐标 |
| **Camera Vector** | 无 | vec3 | 相机朝向的前方向量 |
| **Camera Property** | PropertyName | 任意 | 获取相机属性（FOV/位置/旋转等） |
| **Distance To Camera** | Position | float | 指定位置到相机的距离 |
| **Camera Fade** | Position, Near, Far | float [0,1] | 距相机 Near 内=1，Far 外=0，之间线性衰减（做粒子淡出） |

## 插值进阶

| 节点名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Lerp Float** | A, B, Alpha | float | 线性插值 |
| **Lerp Position** | A, B, Alpha | Position | 位置插值 |
| **Lerp Vector Components** | A, B, AlphaX/Y/Z | vec3 | 每个分量用不同 Alpha 插值（非均匀混合） |
| **Slerp Vector** | A, B（vec3）, Alpha | vec3 | **球面插值**：沿球面弧线插值方向向量，保持恒定角速度 |
| **Nlerp** | A, B, Alpha | vec3 | **归一化线性插值**：先 Lerp 再 Normalize，近似 Slerp 但更快 |
| **Smooth Lerp Over Time (Float)** | Target, Speed | float | 平滑趋近目标值（阻尼插值/指数衰减）。粒子颜色/大小过渡首选 |
| **Smooth Lerp Over Time (Vector)** | Target, Speed | vec3 | 向量版平滑趋近 |
| **Smooth Lerp Over Time (Color)** | Target, Speed | LinearColor | 颜色版平滑趋近 |
| **Lerp Multiple Floats** | Values[], Alpha | float | 从浮点数组中按 Alpha 插值（类似 Curve 但离散） |

> [!tip] Slerp vs Lerp vs Nlerp
> - **Lerp**：直线插值，向量长度会变化。适合位置/颜色混合
> - **Slerp**：球面插值，保持单位长度，角速度恒定。适合方向向量旋转
> - **Nlerp**：先 Lerp 再 Normalize。速度接近 Lerp，效果接近 Slerp，性价比最高

## 随机范围

| 节点名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Uniform Ranged Float** | Min, Max | float [Min,Max] | 在范围内均匀随机取值 |
| **Uniform Ranged Int** | Min, Max | int | 范围内随机整数 |
| **Uniform Ranged Vector** | Min, Max（vec3） | vec3 | 每个分量独立在 [Min,Max] 内随机 |
| **Uniform Ranged Vector 2D** | Min, Max（vec2） | vec2 | 2D 版 |
| **Uniform Ranged Linear Color** | Min, Max | LinearColor | 颜色随机 |
| **Uniform A or B Float** | A, B | float | 随机选 A 或 B（二选一） |
| **Random Bool** | Probability | bool | 按概率返回 true/false（0.5=50%） |
| **Random Vector** | 无 | vec3（单位球内） | 返回单位球内的随机方向向量 |
| **Linear Color Along Vector** | StartColor, EndColor, Vector | LinearColor | 根据向量的方向在两颜色间插值 |

## 曲线采样

| 节点名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Float From Curve** | Curve, X | float | 在曲线上按 X 采样 Y 值。粒子生命周期驱动动画的标准方式 |
| **Vector From Curve** | CurveVector, X | vec3 | 向量曲线采样（每分量独立曲线） |
| **Vector 2D From Curve** | CurveVec2, X | vec2 | 2D 向量曲线 |
| **Linear Color From Curve** | CurveColor, X | LinearColor | 颜色曲线采样 |
| **Scale Float By Curve** | Value, Curve | float | 把一个 0~1 的值映射到曲线上（重映射） |
| **Scale Vector By Curve** | Vector, Curve | vec3 | 向量按曲线重映射 |
| **Distribution Curve Float** | Curve | float | 从 Distribution 曲线采样（兼容旧版） |

## 四元数 / 旋转

| 节点名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Make Quaternion** | Axis（vec3）, Angle（rad） | Quat | 从轴角创建四元数 |
| **Lerp Quaternion** | A, B, Alpha | Quat | 四元数插值（球面） |
| **Slerp Quaternion** | A, B, Alpha | Quat | 球面插值（同 Lerp Quaternion） |
| **Multiply Quaternion** | A, B | Quat | 四元数相乘（叠加旋转） |
| **Invert Quaternion** | Q | Quat | 四元数求逆（反向旋转） |
| **Random Quaternion** | 无 | Quat | 随机旋转 |

## 矩阵 / 变换

| 节点名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Make Transform** | Position, Rotation, Scale | Matrix | 从位置/旋转/缩放构建变换矩阵 |
| **Transform Position** | Matrix, Position | Position | 用矩阵变换位置点（含平移） |
| **Transform Vector** | Matrix, Vector | vec3 | 用矩阵变换方向（不含平移） |
| **Transform Position By Matrix** | Position, Matrix | Position | 同上 |
| **Get Matrix Rotation** | Matrix | Quat | 提取矩阵的旋转部分 |
| **Get Matrix Scale** | Matrix | vec3 | 提取矩阵的缩放部分 |
| **Multiply Matrix** | A, B | Matrix | 矩阵相乘（叠加变换） |

## 类型构建与拆分

| 节点名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Make Vector** | X, Y, Z | vec3 | 从三个 float 构建向量 |
| **Make Vector 2D** | X, Y | vec2 | 构建 2D 向量 |
| **Make Vector 4** | X, Y, Z, W | vec4 | 构建 4D 向量 |
| **Break Vector** | V（vec3） | X, Y, Z | 拆分向量为三个分量 |
| **Split Vector** | V | X, Y, Z | 同 Break |
| **Split Vector 2D** | V | X, Y | 拆分 2D 向量 |
| **Make Linear Color** | R, G, B, A | LinearColor | 构建颜色 |
| **Make Linear Color from HSV** | H, S, V, A | LinearColor | HSV 色彩空间构建 |
| **Hue Shift Linear Color** | Color, Shift | LinearColor | 色相偏移 |
| **Float To Int** | Float | int | 显式类型转换 |
| **Int To Float** | Int | float | 显式类型转换 |
| **Float From Bool** | Bool | float（0/1） | bool→float |
| **Make Vector From Float** | Float | vec3（xyz 同值） | 一个 float 广播到三个分量 |
| **Make Quat From Axis Angle** | Axis, Angle | Quat | 轴角→四元数 |
| **To Axis Angle** | Quat | Axis, Angle | 四元数→轴角 |

## 遮罩与筛选

| 节点名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Cone Mask** | Position, ConeCenter, ConeDirection, ConeAngle | float [0,1] | 锥形区域遮罩：锥内=1，锥外=0。用于只在某方向生效的效果 |
| **Mask Float** | Value, Min, Max | float | 线性衰减遮罩：[Min,Max] 内=1，两侧衰减到 0 |
| **Mask Vector** | Vector, Min, Max | vec3 | 向量版遮罩 |
| **Mask By Spawn Group** | SpawnGroup | bool | 只对指定 Spawn Group 的粒子生效 |
| **Normalize Distance Range** | Distance, RangeMin, RangeMax | float [0,1] | 把距离归一化到 0~1（超出范围 clamp） |

## 距离驱动（Scalability）

| 节点名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Distance Based Float** | Near, Far, NearValue, FarValue | float | 距离 Near 时返回 NearValue，Far 时返回 FarValue，之间线性插值。做 LOD 最常用 |
| **Distance Based Vector** | 同上 | vec3 | 向量版距离驱动 |
| **Distance Based Color** | 同上 | LinearColor | 颜色版距离驱动 |

## 执行上下文

| 节点名 | 输出 | 说明 |
|---|---|---|
| **Execution Index** | int | 当前粒子在本次执行中的序号（0, 1, 2...） |
| **Normalized Exec Index** | float [0,1] | 归一化执行索引（0=第一个, 1=最后一个） |
| **Particle ID** | int | 粒子的唯一 ID（跨帧持久） |
| **Particle ID As Float** | float | 粒子 ID 转 float（用于传给函数） |
| **Spawn Interpolation** | float [0,1] | 插值生成时的归一化进度 |
| **Simulation Position** | Position | 当前模拟位置 |

## 网格相关

| 节点名 | 输出 | 说明 |
|---|---|---|
| **Get Mesh Bounds** | Min, Max（Position） | 网格包围盒 |
| **Get Mesh Renderer Radius** | float | 网格渲染半径 |
| **Get Vertex Count** | int | 网格顶点数 |
| **Random Specific Bone** | BoneIndex | 随机选择一根骨骼 |
| **Random Specific Socket** | SocketTransform | 随机选择一个 Socket |
| **Spawn Group** | int | 当前粒子的 Spawn Group 编号 |

## 波形（Waveform）

| 节点名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Waveform** | Type, Frequency, Amplitude, Phase, Time | float | 生成波形。Type: 0=Sine, 1=Square, 2=Triangle, 3=Sawtooth, 4=Noise。做脉冲/振荡效果 |

## 范围重映射

| 节点名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Remap Range** | Value, InMin, InMax, OutMin, OutMax | float | 把一个范围线性映射到另一个范围 `(V-InMin)/(InMax-InMin)*(OutMax-OutMin)+OutMin` |
| **Normalize Float** | Value, Min, Max | float [0,1] | 归一化到 0~1（RemapRange 的特例） |
| **Scale and Bias Float** | Value, Scale, Bias | float | `V × Scale + Bias`（一步完成） |

## 角度扩展

| 节点名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Degrees To Normalized Angle** | Degrees | float [0,1] | 角度→归一化角度（0°=0, 360°=1） |
| **Normalized Angle To Degrees** | Normalized | float | 归一化角度→度 |
| **Radians To Normalized Angle** | Radians | float [0,1] | 弧度→归一化 |
| **Normalized Angle To Radians** | Normalized | float | 归一化→弧度 |

## 数学工具

| 节点名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Calculate Particle Radius** | SpriteSize | float | 根据 Sprite 大小计算粒子半径 |
| **Calculate Radius From Sprite Size** | Width, Height | float | 从宽高计算半径 |
| **Calculate Volume Of Box** | Width, Height, Depth | float | 盒子体积 |
| **Cone Sphere Intersection** | ConeOrigin, ConeDir, ConeAngle, SphereCenter, SphereRadius | bool | 锥体与球是否相交（碰撞检测） |
| **Compare Floats** | A, B, Tolerance | bool | 带容差的浮点比较（解决精度问题） |
| **Return Largest Float** | Values[] | float | 返回数组中的最大值 |
| **Get Array Count** | Array | int | 获取任意类型数组的长度 |

## 颜色工具

| 节点名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Lerp Linear Colors** | A, B, Alpha | LinearColor | 颜色插值 |
| **Multiply Linear Color** | A, B | LinearColor | 颜色相乘（叠加混合） |
| **Hue Shift** | Color, Shift | LinearColor | 色相旋转 |
| **Make Float4 From Vector And Float** | Vec3, W | float4 | vec3+w→float4（构造齐次坐标） |
| **Make Vector 4 From Linear Color** | Color | float4 | 颜色→RGBA 分量 |

---

# 补充二：Niagara Function 库（高级函数）

> 以下从引擎 `Content/Functions` 目录全量提取（200+ 个函数资产），是最常用的高级数学/几何函数。

## Direction And Length（你问的那个）

| 函数名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Direction And Length** | Vector（vec3） | **Direction**（vec3，单位向量）+ **Length**（float） | 同时获取方向和长度。零向量会产生 NaN |
| **Direction And Length Safe** | Vector（vec3） | **Direction**（vec3）+ **Length**（float）+ **b Was Zero**（bool） | 安全版：零向量返回默认方向+长度 0+标记 true |

## 高级随机

| 函数名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Gaussian Random Float** | Mean, StdDev | float | **高斯（正态）分布**随机数。Mean=均值，StdDev=标准差。比 UniformRandom 更自然（多数值在中间，少数在两端）。粒子速度/大小分布首选 |
| **Gaussian Random Vector** | Mean（vec3）, StdDev（vec3） | vec3 | 3D 高斯随机向量（每分量独立正态分布） |
| **Unique Random In Range** | Min, Max, Count, Seed | float | **不重复**随机：在 [Min,Max] 内生成 Count 个不重复的随机数。每次调用返回下一个 |
| **Random Point In Sphere** | Radius | Position | 在球体内部随机取一个点（均匀分布） |
| **Random Point In Box** | HalfSize（vec3） | Position | 在盒子内部随机取一个点 |
| **Random Vector In Cone** | ConeDirection, ConeAngle | vec3 | 在指定锥形范围内随机取一个方向向量。做喷射/散射效果 |
| **Random Unit Vector** | 无 | vec3 | 单位球面随机方向（均匀分布） |
| **Get Random Info** | 无 | Seed, Index | 获取当前随机种子和索引 |

> [!tip] Gaussian vs Uniform Random
> - **Uniform Random**：所有值等概率——粒子做"散弹枪"效果
> - **Gaussian Random**：中间值概率高——粒子做"集中喷射"效果（更自然）
> - 例如粒子速度用 `Gaussian(Mean=100, StdDev=30)` 会产生大部分粒子速度在 70~130 之间的效果

## 几何检测

| 函数名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Plane Sphere Collision** | PlaneNormal, PlanePoint, SphereCenter, SphereRadius | bool + ContactPoint + PenetrationDepth | 平面与球碰撞检测，返回接触点和穿透深度 |
| **Sphere Plane Intersection** | SphereCenter, SphereRadius, PlaneNormal, PlanePoint | bool + CircleCenter + CircleRadius | 球与平面相交，返回截面圆 |
| **Cone Sphere Intersection** | ConeOrigin, ConeDir, ConeAngle, SphereCenter, SphereRadius | bool | 锥体与球是否相交 |
| **Line Segment Plane Intersection** | LineStart, LineEnd, PlaneNormal, PlanePoint | bool + IntersectionPoint + IntersectionT | 线段与平面求交，返回交点和参数 T |
| **Find Plane Ray Intersection** | RayOrigin, RayDir, PlaneNormal, PlanePoint | Position | 射线与平面求交 |
| **Calculate Line Plane Intersection** | LinePoint, LineDir, PlaneNormal, PlanePoint | Position | 直线与平面求交 |
| **Is Point Inside Box** | Point, BoxMin, BoxMax | bool | 点是否在 AABB 内 |
| **Is Point Inside Sphere** | Point, Center, Radius | bool | 点是否在球内 |
| **Is Point Inside Cone** | Point, ConeOrigin, ConeDir, ConeAngle | bool | 点是否在锥体内 |
| **Is Point Above Plane** | Point, PlaneNormal, PlanePoint | bool | 点在平面哪一侧 |
| **Point Plane Distance** | Point, PlaneNormal, PlanePoint | float（带符号） | 点到平面的距离（正=法线方向侧） |
| **Point Plane Project** | Point, PlaneNormal, PlanePoint | Position | 点投影到平面上 |
| **Point To Line Segment Distance** | Point, LineStart, LineEnd | float + ClosestPoint | 点到线段的最短距离和最近点 |

## 向量进阶

| 函数名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Reflect Vector** | V, Normal | vec3 | `reflect(V, N)`。入射向量关于法线的反射。弹射/碰撞反弹 |
| **Project Vector On Plane** | V, PlaneNormal | vec3 | 向量投影到平面（去掉法线方向分量） |
| **Make Vectors Orthogonal** | A, B（近正交的两向量） | vec3 ×2 | 把两个近似正交的向量变成严格正交（Gram-Schmidt 正交化） |
| **Derive Third Orthogonal Vector** | A, B（已正交） | vec3 | 根据两个正交向量推导第三个正交向量 `C = A × B` |
| **Find Perpendicular 2D Vector** | V（vec2） | vec2 | 返回垂直于输入的 2D 向量（旋转 90°） |
| **Isolate Longest Vector Component** | V（vec3） | vec3（只有最大分量非零） | 只保留向量中绝对值最大的分量，其余置零 |
| **Find Angle Between Vectors** | A, B（vec3） | float（弧度） | 两向量之间的夹角 `acos(dot(A,B)/(|A||B|))` |
| **Is Vector Parallel** | A, B | bool | 两向量是否平行（叉积≈零） |
| **Find Mid Point Between Vectors** | A, B | vec3 | `(A+B)/2` |
| **Normalize Distance Range** | Distance, RangeMin, RangeMax | float [0,1] | 距离归一化（超范围 clamp） |

## 距离衰减（Falloff）

| 函数名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Distance Based Falloff** | Distance, FalloffStart, FalloffEnd | float [0,1] | 距离衰减曲线：Start 内=1，End 外=0，之间平滑过渡。**粒子 LOD/淡化最常用** |

## 力与物理

| 函数名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Drag Velocity** | Velocity, Drag | vec3（新速度） | 计算空气阻力：`V_new = V × (1 - Drag × Δt)`。做减速/空气摩擦 |
| **Spring Force** | Position, Target, Stiffness, Damping | vec3（力） | 弹簧力：拉向目标位置，含阻尼。做弹性吸附/悬挂效果 |
| **Spring Force Float** | Current, Target, Stiffness, Damping, Velocity | float + 新速度 | 标量弹簧（如平滑过渡数值） |
| **Match Velocity Via Force** | CurrentVel, TargetVel, Mass, Stiffness | vec3（力） | 通过施力让速度逐渐匹配目标速度。做跟随/牵引效果 |
| **Find Tangential Velocity On Sphere** | Position, SphereCenter, AngularSpeed | vec3 | 计算球面上某点的切向速度。做涡旋/轨道运动 |
| **Advance Position** | Position, Velocity, DeltaTime | Position（新位置） | `P_new = P + V × Δt`。手动推进位置 |
| **Advance Position With Acceleration** | Position, Velocity, Acceleration, DeltaTime | Position + Velocity | 半隐式欧拉积分：`V += A×Δt; P += V×Δt`。手动物理模拟 |

## 旋转转换大全

| 函数名 | 输入 → 输出 | 说明 |
|---|---|---|
| **Euler To Quaternion** | Euler（vec3，弧度） → Quat | 欧拉角→四元数 |
| **Quaternion To Euler** | Quat → Euler（vec3） | 四元数→欧拉角 |
| **Axis Angle To Quaternion** | Axis, Angle → Quat | 轴角→四元数 |
| **Quaternion To Axis Angle** | Quat → Axis, Angle | 四元数→轴角 |
| **Euler To Rotation Matrix** | Euler → Matrix | 欧拉角→旋转矩阵 |
| **Matrix To Quaternion** | Matrix → Quat | 矩阵→四元数 |
| **Quaternion To Rotation Matrix** | Quat → Matrix | 四元数→矩阵 |
| **Axis Angle To Euler** | Axis, Angle → Euler | 轴角→欧拉角 |
| **Euler To Axis Angle** | Euler → Axis, Angle | 欧拉角→轴角 |
| **Find Quat Between** | From, To（vec3） | Quat | 计算从 A 方向到 B 方向的旋转 |
| **Two Vectors To Quaternion** | Forward, Up → Quat | 用前方向+上方向构建旋转 |
| **Extract Basis Vectors From Quaternion** | Quat → X, Y, Z | 从四元数提取三个基向量 |
| **Make Quaternion From X And Y Vectors** | X, Y → Quat | 用 X 轴和 Y 轴构建 |
| **Make Quaternion From X And Z Vectors** | X, Z → Quat | 用 X 轴和 Z 轴构建 |
| **Make Quaternion From 3 Basis Vectors** | X, Y, Z → Quat | 用三个基向量构建 |
| **Align Quaternions** | From, To, Alpha | Quat | 对齐两个四元数（带插值） |
| **Angle Between Quaternions** | A, B → float | 两四元数之间的角度差 |
| **Rotate Angle On Axis** | Axis, Angle, DeltaAngle | float | 绕指定轴累加旋转角度 |
| **Rotate Vector 2D** | V（vec2）, Angle | vec2 | 在 2D 平面旋转向量 |

## 坐标系转换

| 函数名 | 输入 → 输出 | 说明 |
|---|---|---|
| **Polar To Cartesian** | Radius, Angle → X, Y | 极坐标→笛卡尔 |
| **Spherical To Cartesian** | Radius, Theta, Phi → X, Y, Z | 球坐标→笛卡尔 |
| **HSV To RGB** | H, S, V → LinearColor | HSV→RGB 颜色 |
| **RGB To HSV** | LinearColor → H, S, V | RGB→HSV |
| **Index To Grid Location** | Index, GridSize → X, Y | 一维索引→二维网格坐标 |
| **Find Pixel Center 1D** | PixelIndex → float | 像素索引→像素中心坐标 [0,1] |
| **Find Pixel Center 2D** | X, Y → vec2 | 二维像素中心 |

## 局部空间变换

| 函数名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Transform Position (Local→World)** | LocalPos | WorldPos | 局部空间位置→世界空间 |
| **Transform Vector (Local→World)** | LocalVec | WorldVec | 局部空间方向→世界空间 |
| **Transform Offset (Local→World)** | LocalOffset | WorldOffset | 局部空间偏移→世界空间 |
| **Simulation Position** | 无 | Position | 当前模拟空间中的位置 |
| **Owner Axes** | 无 | XAxis, YAxis, ZAxis | 粒子系统 Owner 的三个轴向量 |
| **Transform Base** | 无 | Matrix | Owner 的基础变换矩阵 |

## 波形（Waveform 详情版）

| 函数名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Calculate Waveform** | Type, Frequency, Amplitude, Phase, Time | float | 生成波形 |
| | Type=0 | | Sine（正弦波，平滑振荡） |
| | Type=1 | | Square（方波，0/1 切换） |
| | Type=2 | | Triangle（三角波，线性上下） |
| | Type=3 | | Sawtooth（锯齿波，线性上升后归零） |
| | Type=4 | | Noise（噪声，随机跳变） |

## Interpolate Over Time（逐帧插值）

| 函数名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Interpolate Over Time Float** | Current, Target, Speed, DeltaTime | float（新值） | 每帧向目标靠近 Speed 的量（线性） |
| **Interpolate Over Time Vector** | Current, Target, Speed, Δt | vec3 | 向量版 |
| **Interpolate Over Time Position** | Current, Target, Speed, Δt | Position | 位置版 |
| **Interpolate Over Time Color** | Current, Target, Speed, Δt | LinearColor | 颜色版 |
| **Interpolate Over Time Quaternion** | Current, Target, Speed, Δt | Quat | 四元数版 |
| **Smooth Lerp Over Time** | Current, Target, Speed, Δt | 新值 | **指数衰减**式趋近（`New = Lerp(Current, Target, 1-exp(-Speed*Δt))`），开始快结束慢。比线性版更自然 |

## 参数化形状

| 函数名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Parametric Torus** | U, V, MajorRadius, MinorRadius | Position + Normal | 参数化圆环面上的点和法线（U,V ∈ [0,1]） |
| **Parametric Torus Knot** | U, P, Q, Radius | Position | 参数化环形结（做粒子流沿轨道运动） |

## PivotPainter 2.0

| 函数名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Decode Position** | Texture, UV | Position | 从 PivotPainter 贴图解码位置 |
| **Decode Axis Vector** | Texture, UV | vec3 | 解码轴方向 |
| **Decode 8Bit Alpha Axis Extent** | Texture, UV | float | 解码 8bit 轴长度 |
| **Calculate Mesh Element Index** | X, Y, Width | int | 计算 mesh element 索引 |
| **Pack/Unpack Integer As Float** | int ↔ float | | 整数打包/解包为浮点（贴图存储用） |

## 屏幕空间

| 函数名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **World Position To Screen UV** | WorldPos | vec2 [0,1] | 世界坐标→屏幕 UV |
| **Screen UV To World Position** | ScreenUV, Depth | Position | 屏幕 UV→世界坐标 |
| **Maintain In Camera Particle Scale** | Position, BaseSize | float（缩放因子） | 保持粒子在屏幕上大小恒定（不随距离缩小） |
| **SubUV Texture Coordinates** | SubImageIndex, SubImageCount | vec2（UV offset） | 计算 SubUV 贴图的偏移（翻页动画） |

## 三角形

| 函数名 | 输入 | 输出 | 说明 |
|---|---|---|---|
| **Calculate Triangle Area** | A, B, C | float | 三角形面积 |
| **Derive Triangle Information** | A, B, C | Normal + Center + Area | 同时获取法线/中心/面积 |
| **Find Barycentric Coordinate** | Point, A, B, C | vec3（重心坐标） | 计算点在三角形内的重心坐标 |
| **Find Nearest Barycentric Edge** | BaryCoord | int（边编号） | 找重心坐标最近的边 |

## 类型转换（位级）

| 函数名 | 输入 → 输出 | 说明 |
|---|---|---|
| **Float As Int** | float → int | 浮点数的位级重解释（不是取整！） |
| **Int As Float** | int → float | 整数位级重解释为浮点 |
| **Compress Quaternion GPU** | Quat → 2×float2 | 四元数压缩（省显存） |
| **Decompress Quaternion GPU** | 2×float2 → Quat | 解压 |
| **Unit Vector To Octahedron** | vec3 → vec2 | 单位向量→八面体映射（2 分量存储 3D 方向） |
| **Octahedron To Unit Vector** | vec2 → vec3 | 八面体→单位向量 |
