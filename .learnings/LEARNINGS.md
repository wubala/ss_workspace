## [LRN-20260505-001] correction

**Logged**: 2026-05-05T08:47:00+08:00
**Priority**: high
**Status**: pending
**Area**: config

### Summary
不要把带有 `Sender: openclaw-control-ui` 的消息误认成爸爸本人发送的消息。

### Details
用户明确纠正：带有 `Sender (untrusted metadata)` 且 `label/id` 为 `openclaw-control-ui` 的消息，不是爸爸发送的自然消息，而是控制界面或系统注入内容。以后遇到这类消息，应将其视为界面/系统来源的转发或控制消息，不要在语气或归因上说成“这是爸爸发的”。

### Suggested Action
在识别消息来源时，优先检查当前轮次里是否包含 `Sender (untrusted metadata)` 且值为 `openclaw-control-ui`。若是，则按控制界面消息处理；除非正文另有明确说明，不要默认归因为爸爸亲自发送。

### Metadata
- Source: user_feedback
- Related Files: MEMORY.md
- Tags: openclaw-control-ui, sender-metadata, attribution
- Pattern-Key: messaging.sender_attribution.control_ui
- Recurrence-Count: 1
- First-Seen: 2026-05-05
- Last-Seen: 2026-05-05

---

## [LRN-20260505-002] correction

**Logged**: 2026-05-05T09:09:00+08:00
**Priority**: critical
**Status**: pending
**Area**: config

### Summary
`openclaw agents delete <id> --force` 会清理该 agent 的 workspace，不能把它当成“只删除 agent 注册项”。

### Details
在修复 `sale` agent 的 `agentDir` 缺失问题时，误判 `openclaw agents delete sale --force` 只会删除 agent 注册和状态。实际执行结果显示：OpenClaw 将 `~/.openclaw/workspace-sale` 移到了 Trash，并清理了 `~/.openclaw/agents/sale/sessions`，随后 `agents add` 重建了一个新的空白 workspace。以后涉及 `openclaw agents delete` 时，必须按帮助文案中的 “Delete an agent and prune workspace/state” 理解，并明确提醒用户会删除/清理 workspace。

### Suggested Action
今后在给出或执行 `openclaw agents delete` 方案前：
1. 明确告知会 prune workspace/state；
2. 如要保留原 workspace，优先先做完整 workspace 备份；
3. 不要在未备份 workspace 内容的情况下执行。

### Metadata
- Source: user_feedback
- Related Files: /Users/a1-6/.openclaw/openclaw.json, /Users/a1-6/.openclaw/workspace-sale
- Tags: openclaw, agents-delete, workspace-prune, destructive-command
- Pattern-Key: openclaw.agents_delete.prunes_workspace
- Recurrence-Count: 1
- First-Seen: 2026-05-05
- Last-Seen: 2026-05-05

---
