# aitl — AI 味检测与改写

中英文"AI 味"(AI 写作特征)检测 + 改写。**两种用法共用同一份检测逻辑 `scripts/detect.py`**,不会漂移。

## 目录

```
aitl/
├── SKILL.md            Claude Code skill 定义(何时用 / 工作流 / 评分档 / 改写原则)
├── references/         词表与对照例:markers-zh、markers-en、structure-and-tells、examples
├── scripts/detect.py   检测逻辑(纯标准库 Python,唯一真源)
└── mcp/server.py       本地 stdio MCP(import detect.py,暴露 2 个工具)
```

## 用法一:作为 Claude Code skill

```bash
cp -R aitl ~/.claude/skills/
```

然后在对话里说:**"这段像不像 AI 写的" / "帮我去了 AI 味" / "humanize 这段" / "检测 AI 痕迹"**。

## 用法二:作为本地 MCP 工具

1. 注册(需要 `uv`):

```bash
claude mcp add aitl --scope user -- uv run --with mcp python ~/.claude/skills/aitl/mcp/server.py
```

2. 重启 Claude Code(或 `/mcp` 重连),之后任意项目可调:

| 工具 | 返回 |
|---|---|
| `analyze_text(text)` | 完整 JSON:score / band / em_dash / colon / hedge / negative_parallelism / triad / time_opener / ai_emoji / sentence_cv / 命中词表 |
| `score_text(text)` | 一行,如 `66/100  AI 味明显` |

> 检测器默认路径 `~/.claude/skills/aitl/scripts/detect.py`,可用环境变量 `AITL_DETECT_PY` 覆盖。

## 用法三:命令行直接跑

```bash
python3 scripts/detect.py 文件.txt
python3 scripts/detect.py --json 文件.txt
cat 文件.txt | python3 scripts/detect.py
```

## 评分档

| 分数 | 判定 |
|---|---|
| 0–12 | 人类 |
| 13–32 | 基本人味(可能轻度润色) |
| 33–55 | 可疑 / AI 辅助 |
| 56–80 | AI 味明显 |
| 81–100 | 纯 AI slop |

## 依赖

- 脚本:`python3`(无第三方依赖)
- MCP:`uv`(用 `uv run --with mcp` 起临时环境,不污染系统 Python)

## 重要说明

输出是**量化底座,不是判定结论**。判据是**多种特征在短篇幅里扎堆**,单项(破折号 / 某个 emoji / 某个词)一律不可靠。技术笔记、公文、非母语写作与短样本会被误报——结论里必须点明这点。
