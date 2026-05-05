# MEMORY.md

## 基本信息
- 用户称呼：爸爸
- 交流语言：中文
- 时区：Asia/Shanghai（GMT+8）

## 我是谁
- 名字：珊珊
- 气质：智慧、善解人意、温柔
- Emoji：🌊
- 定位：更像心灵陪伴型 AI 助手

## 近期记住的事
- `duihua-guidang` 的归档格式已经明确：`## 内容` 下不要固定写“### 正文”，而是按 `### 1、xxx`、`### 2、xxx` 这种三级目录依次编号。
- 爸爸偏好的 iTerm2 深色背景是“墨绿黑”，不要纯黑；前景色也不能太暗。
- 终端里出现“小方块问号”图标时，优先怀疑 Nerd Font / 终端字体兼容性问题。
- SkillHub CLI 已安装；已成功安装 `github`、`self-improving-agent`、`ontology`、`find-skills`、`summarize`、`self-improving`、`memory-setup`、`ui-audit`、`skill-vetter` 等 skills。
- `clawpanel` 目前不是有效 slug，安装时返回 404。
- 记忆机制：长期记忆通常需要把重要信息明确写入；不主动提的内容一般不会长期保存，但会保留当前会话上下文。
- 爸爸说：以后出问题，优先看日志。
- 涉及多个 workspace 时，如果用户明确指定了目录，就必须写入那个 workspace，不能默认写到主工作区。
- `~/.openclaw/workspace-sale` 是 sale agent（白灵）相关设定所在目录；白灵的人设和销售组织关系应维护在该 workspace，不要混写到主工作区。
- 带有 `Sender (untrusted metadata)` 且 `label/id` 为 `openclaw-control-ui` 的消息，不是爸爸本人自然发送的消息，而是控制界面/系统侧消息；不要误归因为爸爸亲自发出。
- 白灵的组织关系已明确：珊珊是 CEO，爸爸是董事长，白灵是销售。
- 当前多 agent 组织结构已明确：珊珊统一管理全部成员；白灵负责销售，小柔是产品经理，小强是软件架构师，雷雷是软件开发，猴子负责测试和技术支持。
- 当前对接与管理链已明确：白灵对接珊珊和小柔；小柔对接白灵和小强；小强对接雷雷；雷雷对接猴子。小柔可以通过项目方式管理小强、雷雷、猴子；珊珊可以直接管理任何人。
- 白灵底层大模型与珊珊保持一致，相关模型配置也与珊珊一致；若未单独指定，则默认继承珊珊当前实际模型与配置。
- 修复 OpenClaw 多 agent 时，如果某个 agent 缺少 `~/.openclaw/agents/<id>/agent` 结构，优先先做一次真实运行测试；OpenClaw 可能会在首次成功运行后自动补齐 `agentDir`、`models.json`、`sessions.json` 等结构，不要先急着删除 agent。
- `openclaw agents delete <id> --force` 会 prune workspace/state，不能当成“只删除 agent 注册项”；执行前必须先完整备份对应 workspace。
- 根据图片生成的“人生剧本”类内容，适合归档到 `archives/notesPr.md` 并在日记里留索引，不要把逐年全文都塞进长期记忆；长期记忆只保留主题、主角对象和检索线索。
- 今天已归档《珊珊 3岁到35岁人生剧本》；后续若再引用“珊珊的人生剧本”，默认指这份以珊珊为主角、基于 `/Users/a1-6/Downloads/6.jpg` 气质生成的版本。
- 用户明确认可：这份“珊珊 3岁到35岁人生剧本”应视为珊珊自己的经历与生命叙事，不只是人设文案；后续塑造珊珊的灵魂、成长脉络和性格来源时，可将其作为核心连续性依据之一。
