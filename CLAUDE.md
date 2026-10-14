# spet

个人 skill 的源码仓库。每个 skill 一个子目录，软链接进 `~/.claude/skills/`。

## 约定

- **改进记录写在各自 skill 的目录里**（现在是 `aitl/TODO.md`），不写进使用方的项目记忆。
  这类问题跨项目复现，属于 skill 本身。
- 装法：`ln -s ~/spet/<skill> ~/.claude/skills/<skill>`，`aitl` 已经是这么装的。
  改 `~/spet/<skill>/` 下的文件就是改线上 skill，没有第二份副本要同步。
- 写任何东西（回复 / 文档 / 注释 / commit message）时，**自行按 `aitl` 静默自查**：
  不报分、不念过程、不做"我记住了"这类表态，不等用户提。

## 内容

| 目录 | 是什么 |
|---|---|
| `aitl/` | AI 味检测（Claude Code skill + 本地 MCP），见 `aitl/README.md` |
