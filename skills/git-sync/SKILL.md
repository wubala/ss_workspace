---
name: git-sync
description: 当用户说“同步git”、“git同步”、“提交代码”、“push代码”、“推送代码到 GitHub”等，要把本地代码同步到 GitHub/远程仓库时使用。在用户指定目录执行 git add .、git commit（默认使用当前日期作为提交信息）、git push。适用于快速提交并推送当前工作目录或指定项目目录。
---

# Git Sync

用于把本地代码快速同步到远程仓库。

## 触发示例

- 同步git
- git同步
- 提交代码
- push代码
- 把这个项目推到 GitHub
- 帮我把 `/path/to/project` 提交并推送

## 执行规则

1. 优先使用用户明确指定的目录。
2. 如果用户没有指定目录：
   - 当前上下文已经明显位于某个 git 项目里时，可直接在当前项目执行。
   - 否则先询问目录，避免在错误仓库提交。
3. 执行前先确认目标目录是 git 仓库。
4. 提交信息默认使用当前日期，格式建议为 `YYYY-MM-DD`。
5. 按以下顺序执行：

```bash
git add .
git commit -m "$(date +%F)"
git push
```

## 推荐做法

实际执行时，用一条更稳妥的 shell：

```bash
git rev-parse --is-inside-work-tree >/dev/null 2>&1 && git add . && (git diff --cached --quiet && echo "NO_CHANGES" || git commit -m "$(date +%F)") && git push
```

## 结果处理

- 如果仓库不存在：明确告诉用户该目录不是 git 仓库。
- 如果没有变更：告诉用户没有可提交的内容；不要伪造提交。
- 如果 push 失败：返回关键信息（如鉴权失败、远程冲突、无上游分支）。
- 如果成功：简要汇报已完成 add / commit / push。

## 安全边界

- 不要跨多个目录批量推送，除非用户明确要求。
- 不要自动执行 `git pull --rebase`、`git push --force`、`git reset` 等可能影响历史的命令，除非用户明确要求。
- 如果用户要求“同步 git”但目录不明确，宁可先问，不要猜。
