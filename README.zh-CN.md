# All-Skills 中文入口

**完成！** 你现在可以使用 68 个代理、492 个技能和 94 个命令（含 113 个 MCP 连接器）。

本页是中文速查入口，完整的中文文档在 [docs/zh-CN/README.md](docs/zh-CN/README.md)，英文主文档在 [README.md](README.md)。

---

## 1. 三分钟安装

```bash
# 方式一：pip
pip install all-skills

# 方式二：npm / npx（需要 Python >= 3.10）
npx @mr-nobody-anonymous/all-skills --help

# 方式三：从源码
git clone https://github.com/Mr-Nobody-Anonymous/All-skills.git
cd All-skills && python -m venv .venv && source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## 2. 接入你的编码代理（一条命令）

```bash
# 把技能库链接进所有检测到的代理工具，并校验链接
allskills setup            # 工作区级别
allskills setup --global   # 同时链接 ~/.claude/skills 等用户级目录

# 查看每个目标的状态
python scripts/setup_tools.py --status
```

支持 Claude Code、Cursor、Codex CLI、Gemini CLI / Antigravity、GitHub Copilot、VS Code、Windsurf、OpenCode、Cline、Roo Code、Block Goose 等 11 个本地目标，以及 Hermes、OpenClaw、Kimi、Trae、CodeBuddy、Continue 等 MCP 目标。

## 3. 安装 MCP 连接器（让代理访问一切）

```bash
# 先体检：看看有哪些服务器、缺哪些密钥
allskills mcp doctor

# 预览并安装标准集合（幂等、可回滚、写入前自动备份）
allskills mcp install --harness claude --profile standard --dry-run
allskills mcp install --harness claude --profile standard

# 想一次拿到全部 64 个连接器
allskills mcp install --harness cursor --profile full --scope user
```

| 配置文件 | 说明 |
| :--- | :--- |
| [`mcps/catalog.json`](mcps/catalog.json) | 113 个 MCP 服务器的唯一事实来源（含风险等级、所需环境变量） |
| [`docs/MCP-CATALOG.md`](docs/MCP-CATALOG.md) | 自动生成的连接器总表 |
| [`mcps/generated/`](mcps/generated/) | 各 harness 的原生配置片段（JSON / TOML / YAML） |

## 4. 日常使用

```bash
allskills search "构建 REST API"          # 在 15,146 条目录条目中检索
allskills explain development.code-review --query "审查这个 PR"
allskills run development.code-review --safe --dry-run
allskills doctor --full                    # 11 层健康检查
```

## 5. 贡献与约定

- 新增技能请阅读 [docs/adding_skills.md](docs/adding_skills.md)，并运行
  `python scripts/validate_schema.py --catalog --max-catalog-errors 0`。
- 新增 MCP 连接器请修改 `mcps/catalog.json`，然后运行
  `python scripts/mcp_catalog.py generate && allskills mcp verify`。
- 安全策略见 [docs/MCP-CONNECTOR-POLICY.md](docs/MCP-CONNECTOR-POLICY.md) 与 [SECURITY.md](SECURITY.md)。
