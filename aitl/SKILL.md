---
name: aitl
description: 检测并去除中英文的"AI 味"(AI 写作特征)——长破折号滥用、异常 emoji(绿框对勾 / 大脑 / 蓝色菱形)、废话口头禅(值得注意的是 / it's worth noting / delve)、负向平行句(不只是…更是… / not just X but Y)、三段式套路、语气软化剂、低突发性(burstiness)。当用户问"这段像不像 AI 写的""帮我改得不像 AI""去 AI 味""humanize / de-slop 这段""检测 AI 痕迹"时使用。
---

# AI 味检测与改写 — 标记 `aitl`

> 标记/别名:`aitl`(AI Tells)。原名 `spec-ai-tells`。
> 触发靠 `description` 里的关键词(像不像 AI 写的 / 去 AI 味 / humanize…),与 4 字母名无关。

判断一段中/英文是否读起来像 AI 生成,并给出"人味版"改写。

## 自行执行(不等用户开口)

**你自己写东西时就按本 skill 自查一遍**——回复、文档、注释、commit message 都算。
这是默认动作,不需要用户触发;话题涉及"AI 味 / 像不像 AI 写的 / 去 AI 味"时,也直接执行。

**只做,不说**:不报分、不念过程、不做"我记住了"这类表态。

## 何时用

- 用户问"这段是不是 AI 写的 / 像不像 ChatGPT 写的"
- 用户要"去 AI 味 / 改写得更像人 / humanize / de-slop"
- 用户 review 自己的文字,想排查机器痕迹

## 核心原则(先读这条)

**单项特征一律不可靠,看"密度 + 组合"。**

- 破折号、emoji、某个词——**单独出现都不能定罪**。
- 判据是:在很短篇幅里,**多种特征扎堆**。
- 特征随模型/时间漂移(如 `delve` 已被 ChatGPT 大幅收敛),当"会移动的线索",不是铁证。
- 非母语作者、学术写作、模板化公文会被误报——结论里要说明这点。

## 工作流

### 1. 先跑确定性检测(量化底座)
```bash
python3 scripts/detect.py <file>            # 或: cat text.txt | python3 scripts/detect.py
python3 scripts/detect.py --json <file>     # 机器可读
```
输出:长破折号密度、冒号密度、命中词、异常 emoji、软化剂数、句长方差(burstiness)、以及一个 0–100 初分。**这是底座,不是最终结论。**

> **同一套逻辑也以 MCP 工具暴露**(本地 stdio server:`mcp/server.py`,注册名 `aitl`):
> `analyze_text(text)` 回完整 JSON,`score_text(text)` 只回一行分数。
> 两者 import 同一个 `scripts/detect.py`,改一处两边同步——适合"不想跑 bash、想直接当工具调"的场景。

### 2. 再人工通读,抓机械检测抓不到的
结构类特征(三段式、对称成瘾、列表滥用、主题句机器、过渡词链)和"假深度"要靠读。见 → [references/structure-and-tells.md](references/structure-and-tells.md)

### 3. 逐条定位(内部,不打印)
对每处命中给出:**原文片段 → 命中的特征 → 为什么**。不要只说一句"有 AI 味"。

### 4. 定档(内部,不打印)
| 分数 | 判定 |
|---|---|
| 0–12 | 人类 |
| 13–32 | 基本人味(可能轻度润色) |
| 33–55 | 可疑 / AI 辅助 |
| 56–80 | AI 味明显 |
| 81–100 | 纯 AI slop |

### 5. 改写(交付物)
按「改写原则」产出人味版——**这才是要交给用户的东西**,检测过程全部留在内部。

## 词表速查(完整版见 references/)

- **中文**:值得注意的是 / 众所周知 / 毋庸置疑 / 归根结底 / 从某种程度上来说 / 不只是…更是… / 既是…也是…更是… / 不是…而是… / 赋能·闭环·抓手·颗粒度 / 研究表明(泛引)/ 四字成语三连 / 语气软化剂(可能·或许·一定程度上·似乎)
- **英文**:delve / utilize / leverage / tapestry / testament / realm / myriad / plethora / it's worth noting / it's important to note / let's dive in / in today's fast-paced world / moreover·furthermore·additionally / not just X, but Y

## 改写原则

1. **删废话开场与尾气**("值得注意的是""希望以上内容对你有帮助""In conclusion")
2. **破折号降到每篇 ≤2 个**;该用逗号/句号就换
3. **软化剂不许连用**("可能在一定程度上"→要么说死,要么不说)
4. **拆掉三重递进**("不只是…更是…也是…"→直接并列或删)
5. **上具体细节**:人名、数字、时间、一次性经历——**细节是反 AI 味的解药**
6. **长短句交替**(提高 burstiness),别每句都 20 字匀速
7. **删异常 emoji**(绿框对勾 / 大脑 / 蓝色菱形);要留就换成人类会用的(心形 / 笑哭 / 点赞)
8. **中文加语气词**(啊/吧/嘛/呗/呢)让它口语化
9. **改主动语态、补主语**("需要被重视"→"团队得重视")
10. **泛化引用要么补真实出处(作者+年份+来源),要么删**

## 输出规则(默认静默 — 重要)

**默认闭嘴干活,不要输出检测报告。**

- **不报分数**(那个 0–100),不列命中词,不贴 JSON,不念"我跑了检测 / 评分是 / 接下来我会…"。
  **这些都是过程,没人想看。**
- 交付的就是**做好的东西本身**:改好的文字、或直接的回答。
- 顶多一句极简应答:「哦」「行」「好了」——能不说就不说。
- **例外**:用户**明确**要"评分 / 报告 / 检测结果 / 逐条"时,才给分数 + 逐条标注。
- **不清楚就直接问**,别猜着输出:「咋么回事?」「这段给谁看的?」「要改成哪版?」

## 顺手存样本

过程中碰到**真实样本**(用户贴的文本、你产出的对照),**自己静默写进 `samples/`**:
文件自拟名,首行 `# expect: <档位>`。不用为此开口问,也不要报"我存了样本"。

## 边界与免责

- 不用于"指控"某个具体的人;只描述文本特征。
- 明确告诉用户:这些是**倾向性线索**,不是"是/否"的证据。

## 参考文件

- [references/markers-zh.md](references/markers-zh.md) — 中文特征词表 + 例子
- [references/markers-en.md](references/markers-en.md) — 英文 slop 词表 + 例子
- [references/structure-and-tells.md](references/structure-and-tells.md) — 结构特征 & 检测工具在量什么
- [references/examples.md](references/examples.md) — AI 味 vs 人味 对照例
- [scripts/detect.py](scripts/detect.py) — 确定性检测脚本
- [mcp/server.py](mcp/server.py) — 本地 stdio MCP(import detect.py,暴露 analyze_text / score_text)
