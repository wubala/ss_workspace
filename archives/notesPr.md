
---

# 格式验证

## 基本信息

- 时间：2026-03-28 23:29
- 来源：与珊珊的对话
- 类型：指定内容记录

## 内容

### 1、主题

powerlevel10k，冷色调蓝灰风。

### 2、已安装工具

fzf、eza、bat、fd、zoxide。

### 3、常用快捷键

Ctrl + R、Ctrl + T、Alt + C。

---

# item日常操作（插件）

## 基本信息

- 时间：2026-03-28 23:31
- 来源：与珊珊的对话
- 类型：指定内容记录

## 内容

### 1、主题

powerlevel10k，冷色调蓝灰风。作用是显示当前目录、git 状态、命令执行耗时、时间等信息，界面更清爽直观。如需进一步个性化，可运行 p10k configure。

### 2、已安装工具

fzf：模糊搜索工具，用于历史命令、文件、目录快速选择。
eza：更好看的 ls，用于彩色列表、图标、树状展示。
bat：更好看的 cat，带语法高亮。
fd：更快的 find 替代品。
zoxide：智能目录跳转工具。

### 3、已启用插件

git：提供 git 常用别名与补全。
macos：提供 macOS 常用命令支持。
zsh-autosuggestions：根据历史命令给出灰色自动建议。
zsh-syntax-highlighting：命令行语法高亮，错误命令会显示异常颜色。
fzf-tab：增强 Tab 补全效果，支持候选项模糊选择。
zoxide：配合 z 命令进行智能跳目录。
colored-man-pages：man 手册带颜色显示。
extract：统一解压常见压缩文件。

### 4、常用快捷键

Ctrl + R：搜索历史命令。
Ctrl + T：搜索文件并插入当前命令行。
Alt + C：搜索目录并直接进入。
Tab：增强补全。
Shift + Tab：反向切换补全项。
右方向键：接受 zsh-autosuggestions 的灰色建议。
Ctrl + A：跳到行首。
Ctrl + E：跳到行尾。
Ctrl + W：删除前一个单词。
Option + 左/右方向键：按单词移动。

### 5、常用别名

ls：替换为 eza，美化目录显示。
ll：详细列表显示。
la：显示包含隐藏文件的完整列表。
lt：树状显示目录。
c：清屏。
reload：重新加载 ~/.zshrc。
zshrc：快速打开 ~/.zshrc。
g：git。
ga：git add。
gc：git commit -m。
gst：git status -sb。
gl：git log --oneline --graph --decorate -20。
gp：git push。
gpl：git pull --rebase。
gd：git diff。
z 关键词：通过 zoxide 快速跳转到常去目录。

### 6、日常建议

修改配置后执行 source ~/.zshrc。打开新终端后可优先试 ll、gst、Ctrl + R、Ctrl + T、Alt + C。如果主要是记录和查找命令，fzf、zoxide、git 插件是最常用的核心组合。

---

# 头像定位过程

## 基本信息

- 时间：2026-03-28 23:34
- 来源：与珊珊的对话
- 类型：指定内容记录

## 内容

### 1、现象

Control UI 中头像一直没有显示，刷新后仍无变化。

### 2、初步排查

检查了工作区中的身份文件 IDENTITY.md，确认里面已经写了头像字段 avatars/2.png。检查了头像文件本身，确认文件存在。

### 3、网关接口排查

直接检查头像接口 /avatar/main?meta=1，发现接口返回的是 avatarUrl: null，说明不是前端渲染问题，而是 Gateway 根本没有提供可用头像。

### 4、配置同步排查

检查后发现，Control UI 实际依赖的是 agent identity 配置，而不只是工作区里的 IDENTITY.md。于是把 IDENTITY.md 的内容同步进 agent 配置。但同步后头像接口依然返回空。

### 5、重启验证

重启了当前 Gateway 进程，再次检查头像接口，结果仍然是 avatarUrl: null。说明不是单纯因为配置未重载。

### 6、根因定位

继续检查头像文件大小，发现 avatars/2.png 大小为 2,535,558 bytes。OpenClaw 对本地头像文件有限制：最大 2 MB。因为超过大小限制，Gateway 会拒绝提供该头像，所以前端一直拿不到。

### 7、解决办法

将头像图片缩小到更小尺寸（如 512x512）。处理后重新让 Gateway 使用缩小后的头像文件，随后头像恢复正常显示。

### 8、结论

这次问题的真正原因不是前端，也不是单纯的缓存或身份文件未读取。真正原因是：本地头像文件超过 2 MB 限制，Gateway 拒绝提供头像。后续更换头像时建议：路径正确、文件存在、大小不超过 2 MB、尽量使用较小尺寸。

---

# 2026-03-30

## 基本信息

- 时间：2026-03-30 23:02
- 来源：与珊珊的对话
- 类型：指定内容记录

## 内容

### 1、内容

标题：OpenClaw 补全配置记录

### 2、内容

类型：对话整理

### 3、内容

时间：2026-03-30 23:02（Asia/Shanghai）

### 4、内容

内容：

### 5、内容

- 用户反馈 openclaw 在命令行里联想不出来命令。

### 6、内容

- 初步判断与 Oh My Zsh 配置有关，尤其是 shell completion 没加载或 compinit / 插件链路受影响。

### 7、内容

- 检查了 `~/.zshrc`，发现原配置里没有显式加载 OpenClaw 的补全脚本。

### 8、内容

- 已通过 `openclaw completion --shell zsh --write-state` 生成补全脚本到 `~/.openclaw/completions/openclaw.zsh`。

### 9、内容

- 已在 `~/.zshrc` 中仅新增一段条件加载：若该补全脚本存在则 source 它；未改动其他插件、别名或 p10k 配置。

### 10、内容

- 已确认补全脚本内包含 `compdef _openclaw_root_completion openclaw`，且现在应可正常联想 `openclaw` 子命令。
